from envvarconf import BaseSettings
from envvarconf.loaders import environ


class Settings(BaseSettings):
    SENTRY_DSN: str
    LOGGING_LEVEL: str = 'debug'

    HOST: str = "aaaakehgeiuhgiweurhiuerhf"*200
    PORT: int

    DEBUG: bool = False


def test_settings_invalid(monkeypatch):
    monkeypatch.setenv("DEBUG", "off")

    settings = Settings(appname="evc_tests")
    errors = settings.load([environ.Loader()], failfast=False)
    assert len(errors) == 3
    assert errors == ["Bad value for boolean field: 'off'", 'SENTRY_DSN is not defined', 'PORT is not defined']


def test_settings_valid(monkeypatch):
    monkeypatch.setenv("SENTRY_DSN", "123")
    monkeypatch.setenv("PORT", "123")

    settings = Settings(appname="evc_tests")
    errors = settings.load([environ.Loader()])

    assert len(errors) == 0
    assert settings.SENTRY_DSN == "123"
    assert settings.PORT == 123
