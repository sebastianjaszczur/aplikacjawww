import os
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# E-mail settings

ADMINS = (('Sebastian Jaszczur', 'sebastian.jaszczur+aplikacjawww@gmail.com'),
          ('Marcin Wrochna', 'mwrochna+django@gmail.com'),
          ('Michał Zieliński', 'michal@zielinscy.org.pl'),
          )

MANAGERS = (('Sebastian Jaszczur', 'sebastian.jaszczur+aplikacjawww@gmail.com'),
            ('Marcin Wrochna', 'mwrochna+django@gmail.com'),
            ('Michał Zieliński', 'michal@zielinscy.org.pl'),
            )

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allaccess',
    'crispy_forms',
    'django_select2',
    'django_bleach',
    'tinymce',
    'compressor',
    'wwwapp',
    'django_cleanup',
    'imagekit',
    'gallery',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wwwapp.urls'

WSGI_APPLICATION = 'wwwapp.wsgi.application'

# Set cripsy forms template pack
CRISPY_TEMPLATE_PACK = 'bootstrap3'
SELECT2_BOOTSTRAP = True

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = [
    'p', 'b', 'i', 'u', 'em', 'strong', 'a', 'pre', 'div', 'strong', 'sup', 'sub', 'ol', 'ul', 'li', 'address',
    'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'table', 'tbody', 'tr', 'td', 'hr', 'img',
]

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = [
    'href', 'title', 'style', 'alt', 'src', 'dir', 'class', 'border', 'cellpadding', 'cellspacing', 'id',
    'name', 'align', 'width', 'height',
]

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant', 'float',
    'height', 'width', 'min-height', 'min-width', 'max-height', 'max-width',
    'margin', 'margin-top', 'margin-bottom', 'margin-right', 'margin-left',
    'padding', 'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
    'text-align', 'title', 'page-break-after', 'display', 'color', 'background-color',
    'font-size', 'line-height', 'border-collapse', 'border-spacing', 'empty-cells', 'border',
]

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False

# Logging and authentication

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/login/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allaccess.backends.AuthorizedServiceBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'allaccess.context_processors.available_providers',
            ],
        },
    },
]

TINYMCE_JS_URL = os.path.join(STATIC_URL, "tinymce/js/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "tinymce/js/tinymce")
TINYMCE_INCLUDE_JQUERY = False
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'silver',
    'plugins': 'preview paste searchreplace autolink code visualblocks visualchars image link media codesample table charmap hr nonbreaking anchor toc advlist lists wordcount textpattern emoticons',
    'removed_menuitems': 'newdocument',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | link',
    'content_css': [
        '/static/css/bootstrap.min.css',
        '/static/css/main.css',
    ],
    'content_style': 'body { margin: 2rem; }',
    'height': 500,
    'branding': False,
    'image_advtab': True,
    'paste_data_images': False,
    'relative_urls': False,
    'remove_script_host': True,
    'link_list': '/articleNameList/',
}
TINYMCE_DEFAULT_CONFIG_WITH_IMAGES = {  # Additional settings for editors where image upload is allowed
    'plugins': 'preview paste searchreplace autolink code visualblocks visualchars image link media codesample table charmap hr nonbreaking anchor toc advlist lists wordcount imagetools textpattern quickbars emoticons',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent | numlist bullist | image media link codesample',
    'paste_data_images': True,
    'file_picker_types': 'image',
    'file_picker_callback': 'tinymce_local_file_picker',
}

CURRENT_YEAR = 2020
WORKSHOPS_START_DATE = datetime.date(2020, 7, 3)
WORKSHOPS_END_DATE = datetime.date(2020, 7, 15)

COMPRESS_ENABLED = True

INTERNAL_IPS = [
    '127.0.0.1',
]

# Max amount of points that a participant can get during qualification (relative to configured max_points for a given workshop)
# This allows to give some people bonus points above 100%
# Note that this is not a hard limit for values that can be entered by lecturers, excessive values will just be clamped for percentage calculation
MAX_POINTS_PERCENT = 200

GALLERY_LOGO_PATH = 'images/logo_transparent.png'
GALLERY_TITLE = 'Galeria WWW'
GALLERY_FOOTER_INFO = 'Wakacyjne Warsztaty Wielodyscyplinarne'
GALLERY_FOOTER_EMAIL = ''

K8S_AUTH_URL = "https://auth-connector.wwwx.me/authorize"
K8S_AUTH_TOKEN = ""
K8S_DOMAIN = "wwwx.me"
