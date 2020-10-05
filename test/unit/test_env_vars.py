from django.conf import settings


def test_env_vars(capsys):
    with capsys.disabled():
        print(settings.FIREBASE_AUTH)
        print(settings.FIREBASE_API_KEY)
