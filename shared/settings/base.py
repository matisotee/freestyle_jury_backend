from shared.settings import get_env_variable, get_env_variable_or_none
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = get_env_variable('SECRET_KEY')

DB_USERNAME = get_env_variable_or_none('MONGO_USERNAME')
DB_PASSWORD = get_env_variable_or_none('MONGO_PASSWORD')
DB_NAME = get_env_variable_or_none('MONGO_DATABASE_NAME')

MONGO_URL = 'mongodb+srv://{}:{}@cluster0.zhs7q.mongodb.net/{}?retryWrites=true&w=majority'.format(
    DB_USERNAME,
    DB_PASSWORD,
    DB_NAME
)


# Firebase credentials
FIREBASE_AUTH = {
    "SERVICE_ACCOUNT_KEY_FILE": {
        "type": get_env_variable_or_none('FIREBASE_TYPE'),
        "project_id": get_env_variable_or_none('FIREBASE_PROJECT_ID'),
        "private_key_id": get_env_variable_or_none('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": get_env_variable_or_none('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": get_env_variable_or_none('FIREBASE_CLIENT_EMAIL'),
        "client_id": get_env_variable_or_none('FIREBASE_CLIENT_ID'),
        "auth_uri": get_env_variable_or_none('FIREBASE_AUTH_URI'),
        "token_uri": get_env_variable_or_none('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": get_env_variable_or_none('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": get_env_variable_or_none('FIREBASE_CLIENT_X509_CERT_URL')
    },
    "EMAIL_VERIFICATION": True
}
FIREBASE_API_KEY = get_env_variable_or_none('FIREBASE_API_KEY')

# Optimizely credential
OPTIMIZELY_SDK_KEY = get_env_variable_or_none('OPTIMIZELY_SDK_KEY')
