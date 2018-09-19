"""
Django settings for Mxshop project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0,BASE_DIR)
sys.path.insert(0,os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0,os.path.join(BASE_DIR, 'extra_apps'))

AUTH_USER_MODEL = 'users.UserProfile'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')0aj-k13f)5$7go34dc0b%u%#l0x(8&)vguui&b(8wn-bn-2^0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users.apps.UsersConfig',
    'apps.goods.apps.GoodsConfig',
    'apps.trade.apps.TradeConfig',
    'apps.user_operation.apps.UserOperationConfig',
    'xadmin',
    'crispy_forms',
    'DjangoUeditor',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'rest_framework.authtoken',
    'social_django',
    # 'goods',
    # 'trade',
    # 'user_operation',
    # 'users'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Mxshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 第三方登录
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Mxshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxshop',        #数据库名字
        'USER': 'root',          #账号
        'PASSWORD': '0315',    #密码
        'HOST': '127.0.0.1',     #IP
        'PORT': '3306',          #端口
        #这里引擎用innodb（默认myisam）
        #因为后面第三方登录时，要求引擎为INNODB
        # 'OPTIONS':{'init_command': 'SET storage_engine=INNODB'}, #这样设置会报错，改为
        "OPTIONS":{"init_command":"SET default_storage_engine=INNODB;"}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# 语言改为中文
LANGUAGE_CODE = 'zh-hans'

# 时区改为上海
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


# 设置上传文件，图片访问路径
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# 数据存放
MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# REST framework 分页
REST_FRAMEWORK = { #drf 的全局配置
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE':10,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication', #drf 自带token验证

        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
#限速设置
    'DEFAULT_THROTTLE_CLASSES': (
            'rest_framework.throttling.AnonRateThrottle',   #未登陆用户
            'rest_framework.throttling.UserRateThrottle'    #登陆用户
        ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',         #每分钟可以请求18次
        'user': '10/minute'          #每分钟可以请求30次
    }

}

CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = ( #用户认证
    'users.views.CustomBackend', # 用户认证的path路径（users/vlews下的CustomBackend）
    # 第三方登录
    'social_core.backends.weibo.WeiboOAuth2',  # 微博登录
    'social_core.backends.qq.QQOAuth2',  # qq登录
    'social_core.backends.weixin.WeixinOAuth2',   # 微信登录
    'django.contrib.auth.backends.ModelBackend',
)

import datetime
JWT_AUTH = { # JWT 全局配置
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),    #有效期7天，也可以设置seconds=20（20秒）等
    # 'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=20),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',                       #JWT跟前端保持一致，比如“token”，这里默认JWT
}

#缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 5   # 5秒过期
    # 'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 *5   #5分钟过期
}

# 第三方登录，里面的值是你的开放平台对应的值
SOCIAL_AUTH_WEIBO_KEY = '1810880521'  # 微博 APP key
SOCIAL_AUTH_WEIBO_SECRET = '3005fd853a6e4f015973e656db911119'  # 微博 APP secret

SOCIAL_AUTH_QQ_KEY = 'dhdhj'   # QQ
SOCIAL_AUTH_QQ_SECRET = 'dfhfjfjf'

SOCIAL_AUTH_WEIXIN_KEY = 'hkjgkjyf'  # 微信
SOCIAL_AUTH_WEIXIN_SECRET = 'tjhftjfjf'

#登录成功后跳转到首页
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

#云片网APIKEY
APIKEY = "293a3ef67**********16ffaeca"