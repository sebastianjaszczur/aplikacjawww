from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from wwwapp.models import UserProfile, UserInfo, Article, ArticleContentHistory, Workshop, WorkshopCategory, WorkshopType, WorkshopParticipant
from faker import Faker
from faker.providers import profile, person, date_time
import random

"""
Command implementing database population. 
Useful for making test fixtures. 
"""
class Command(BaseCommand):
    args = ''
    help = 'Populate the database with data for development'
    LOCALE = 'pl_PL'

    """
    Constructor of the command
    """
    def __init__(self) -> None:
        fake = Faker(self.LOCALE)
        fake.add_provider(profile)
        fake.add_provider(person)
        fake.add_provider(date_time)
        self.fake = fake

        super().__init__()

    """
    Create and returns a fake random user.
    """
    def fake_user(self) -> UserProfile:
        profile_data = self.fake.profile()
        u = User.objects.create_user(profile_data['username'], profile_data['mail'], 'password')
        u.save()

        info = UserInfo(pesel=profile_data['ssn'],
                        address=profile_data['address'],
                        comments=self.fake.text(100))
        info.save()

        profile = UserProfile(user=u,
                              user_info=info,
                              gender=profile['sex'],
                              school="TEST",
                              matura_exam_year=self.fake.date_this_year().year,
                              how_do_you_know_about=self.fake.text(),
                              profile_page=self.fake.text(),
                              cover_letter=self.fake.text())

        profile.save()
        return u

    """
    Creates and returns a fake random article with a random edit history
    """
    def fake_article(self, users) -> Article:
        article = Article(name=self.fake.text(),
                          title=self.fake.text(),
                          content=self.fake.paragraph(),
                          modified_by=random.choice(users),
                          on_menubar=random.choice([False, True]))

        article.save()

        for i in range(2, 4):
            ArticleContentHistory(version=i,
                                  article=article,
                                  content=self.fake.paragraph(),
                                  modified_by=random.choice(users),
                                  time=self.fake.date_time_this_year()).save()

        return article

    """
    Creates and returns a random category
    """
    def fake_category(self) -> WorkshopCategory:
        c = WorkshopCategory(year=2019, name=self.fake.text())
        c.save()
        return c

    """
    Creates and returns a random type
    """
    def fake_type(self) -> WorkshopType:
        c = WorkshopType(year=2019, name=self.fake.text())
        c.save()
        return c

    """
    Creates a fake random workshops with 5 random participants
    """
    def fake_workshop(self, users, types, categories) -> Workshop:
        participants = random.choices(users, k=5)
        workshop = Workshop(name=self.fake.text(),
                            title=self.fake.title(),
                            proposition_description=self.fake.paragraph(),
                            type=random.choice(types),
                            category=random.choice(categories),
                            lecturer=random.choice(users),
                            status='Z',
                            page_content=self.fake.paragraph(),
                            page_content_is_public=True,
                            is_qualifying=True,
                            participants=participants
                            )
        workshop.save()

        for participant in participants:
            info = WorkshopParticipant(workshop=workshop,
                                       participant=participant,
                                       comment=self.fake.paragraph())
            info.save()

        return workshop

    """
    Handles the command
    """
    def handle(self, *args, **options) -> None:
        User.objects.create_superuser("admin", "admin@admin.admin", "admin")

        users = []
        for i in range(50):
            users.append(self.fake_user())

        articles = []
        for i in range(2):
            articles.append(self.fake_article(users))

        types = []
        for i in range(2):
            types.append(self.fake_type())

        categories = []
        for i in range(2):
            categories.append(self.fake_category())

        workshops = []
        for i in range(5):
            workshops.append(self.fake_workshop(users, types, categories))
