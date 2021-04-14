from io import StringIO

from django.core.management import call_command


def test_generate_fernet_key_command():
    out = StringIO()
    call_command("generate_fernet_key", stdout=out)
    assert len(out.getvalue()) == 45
