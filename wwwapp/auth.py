import base64
import hashlib
import logging
import re

from allaccess.models import AccountAccess
from allaccess.views import OAuthRedirect, OAuthCallback
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import smart_bytes, force_text

from .models import UserProfile
from .views import get_context


def login_view(request):
    # Forget AccountAccesses to merge if user goes somewhere then back to login.
    if 'merge_access' in request.session:
        del request.session['merge_access']
    if 'merge_access_info' in request.session:
        del request.session['merge_access_info']

    if request.user.is_authenticated:
        # This should never happen if the login flow worked correctly but I'm leaving this here just in case there are any broken users in the database already
        # (aka I'm too afraid to remove it)
        user_profile, just_created = UserProfile.objects.get_or_create(user=request.user)
        if just_created:
            # TODO: untested - this should trigger the Django admin email thing?
            logging.getLogger('django').error('User profile was missing for {}. This should have never happened.')

    # Make sure to call get_context after UserInfo and UserProfile get created, since they are required
    # to figure out what to show on the menu bar
    context = get_context(request)
    return render(request, 'login.html', context)


def standarize_user_info(user_info):
    if 'id' not in user_info and 'sub' in user_info:
        user_info['id'] = user_info['sub']
    if 'first_name' not in user_info:
        if 'given_name' in user_info:
            user_info['first_name'] = user_info['given_name']
        elif 'name' in user_info and 'givenName' in user_info['name']:
            user_info['first_name'] = user_info['name']['givenName']
    if 'last_name' not in user_info:
        if 'family_name' in user_info:
            user_info['last_name'] = user_info['family_name']
        elif 'name' in user_info and 'familyName' in user_info['name']:
            user_info['last_name'] = user_info['name']['familyName']
    if 'gender' in user_info:
        if user_info['gender'].lower() == 'm' or user_info['gender'].lower() == 'male':
            user_info['gender'] = 'M'
        elif user_info['gender'].lower() == 'f' or user_info['gender'].lower() == 'female':
            user_info['gender'] = 'F'
    if 'email' not in user_info:
        if 'emails' in user_info and user_info['emails'] and 'value' in user_info['emails'][0]:
            user_info['email'] = user_info['emails'][0]['value']


# Extend django-all-access' OAuthRedirect to make G+ and emails work.
class ScopedOAuthRedirect(OAuthRedirect):
    def get_callback_url(self, provider):
        return reverse('scopedallaccess-callback', kwargs={'provider': provider.name})

    def get_additional_parameters(self, provider):
        if provider.name == 'facebook':
            return {'scope': 'public_profile email'}
        if provider.name == 'google':
            return {'scope': 'openid profile email'}
        return super(ScopedOAuthRedirect, self).get_additional_parameters(provider)


# Extend django-all-access' OAuthCallback to detect and merge duplicates.
class ScopedOAuthCallback(OAuthCallback):
    def handle_new_user(self, provider, access, info):
        context = get_context(self.request)
        # Check for users with the same emails or names.
        standarize_user_info(info)
        match_users = []
        context['allow_account_creation'] = True
        context['new_provider'] = provider

        if 'email' in info and info['email']:
            context['email'] = info['email']
            match_users = list(User.objects.filter(email=info['email']))
            if match_users:
                context['allow_account_creation'] = False
        else:
            context['email'] = None

        if not match_users and 'last_name' in info:
            context['name'] = info['last_name']
            query = User.objects.filter(last_name=info['last_name'])
            if 'first_name' in info:
                context['name'] = info['first_name'] + ' ' + info['last_name']
                query = query.filter(first_name=info['first_name'])
            match_users = match_users + list(query.all())
        else:
            context['name'] = None

        # If there are matches, suggest loging in with previous provider (and
        # remember access to connect accounts)
        if match_users:
            context['matches'] = []
            for matchUser in match_users:
                match = {'name': matchUser.first_name + ' ' + matchUser.last_name,
                         'email': matchUser.email,
                         'providers': []}
                for matchAccess in AccountAccess.objects.filter(user=matchUser).all():
                    match['providers'].append(matchAccess.provider)
                context['matches'].append(match)
            self.request.session['merge_access'] = access.pk
            self.request.session['merge_access_info'] = info
            return render(self.request, 'loginMerge.html', context)
        # No matches, create a new user
        else:
            user = self.get_or_create_user(provider, access, info)
            access.user = user
            AccountAccess.objects.filter(pk=access.pk).update(user=user)
            user = authenticate(provider=access.provider, identifier=access.identifier)
            login(self.request, user)
            return redirect(self.get_login_redirect(provider, user, access, True))

    def handle_existing_user(self, provider, user, access, info):
        # If using a new provider and logining after suggestion to use
        # previous provider, connect the new provider.
        if 'merge_access' in self.request.session:
            pk = self.request.session['merge_access']
            AccountAccess.objects.filter(pk=pk).update(user=user)
            del self.request.session['merge_access']
            del self.request.session['merge_access_info']
        login(self.request, user)
        return redirect(self.get_login_redirect(provider, user, access))

    def get_or_create_user(self, provider, access, info):
        return create_user(access, info)


# Creates a django User with a nice username from info.
def create_user(access, info):
    username = ''
    if 'last_name' in info:
        name = re.sub(r'[^a-zA-Z0-9]', '', info['last_name'])
        username = name[:18]
    if 'first_name' in info:
        name = re.sub(r'[^a-zA-Z0-9]', '', info['first_name'])
        l = 22 - len(username)
        username = name[:l] + username
    if len(username) < 5 and 'email' in info:
        name = re.sub(r'@.*$', '', info['email'])
        name = re.sub(r'[^a-zA-Z0-9]', '', name)
        l = 22 - len(username)
        username = name[:l] + username

    digest = hashlib.sha1(smart_bytes(access)).digest()
    digest = force_text(base64.urlsafe_b64encode(digest)).replace('=', '')
    username = username + '-' + digest[-7:]

    kwargs = {
        User.USERNAME_FIELD: username,
        'email': '',
        'password': None
    }
    if 'email' in info:
        kwargs['email'] = info['email']
    if 'first_name' in info:
        kwargs['first_name'] = info['first_name']
    if 'last_name' in info:
        kwargs['last_name'] = info['last_name']

    user = User.objects.create_user(**kwargs)

    user_profile = UserProfile.objects.get_or_create(user=user)
    if 'gender' in info:
        user_profile.gender = info['gender']

    return user


# The view called when a user decides not to merge into any suggested accounts.
def create_user_from_unmerged_access_view(request):
    if 'merge_access' not in request.session:
        raise ValidationError('No AccountAccess to create User from.')
    pk = request.session['merge_access']
    info = request.session['merge_access_info']
    access = AccountAccess.objects.get(pk=pk)
    user = create_user(access, info)
    access.user = user
    AccountAccess.objects.filter(pk=pk).update(user=user)
    del request.session['merge_access']
    del request.session['merge_access_info']
    user = authenticate(provider=access.provider, identifier=access.identifier)
    login(request, user)
    return redirect(settings.LOGIN_REDIRECT_URL)


# Register a receiver called whenever a User object is saved.
# Add all created Users to group allUsers.
@receiver(post_save, sender=User, dispatch_uid='user_post_save_handler')
def user_post_save(sender, instance, created, **kwargs):
    if created:
        group, group_created = Group.objects.get_or_create(name='allUsers')
        group.user_set.add(instance)
