import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="tech-conf-server.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="saruadmin@tech-conf-server" #TODO: Update value
    POSTGRES_PW="Thesalman101"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://tech-conf-bus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=W/TlHHpFdZ4nmC07dUxGuMn9zWoz2nFVvtIS/wc3Ai4=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'realdormat@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False