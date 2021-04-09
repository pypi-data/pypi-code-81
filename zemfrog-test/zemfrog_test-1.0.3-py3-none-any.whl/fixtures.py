from zemfrog.helper import db_commit, get_object_model, db_add
from zemfrog_test.helper import generate_random_string
from werkzeug.security import generate_password_hash
from pytest import fixture

## Fixtures


@fixture(scope="session")
def client(app, req_ctx):
    with app.test_client() as c:
        yield c


@fixture(scope="session")
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@fixture(scope="session")
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx


@fixture(scope="session")
def user(app_ctx):
    model = get_object_model("user")
    first_name = generate_random_string(5)
    last_name = generate_random_string(5)
    name = first_name + " " + last_name
    email = first_name.lower() + "@" + last_name.lower() + ".com"
    password = generate_random_string(8)
    user = model(
        first_name=first_name,
        last_name=last_name,
        name=name,
        email=email,
        password=generate_password_hash(password),
        confirmed=True,
    )
    db_add(user)
    return {"email": email, "password": password}


## Finalizer


@fixture(scope="session", autouse=True)
def cleanup(request, app_ctx):
    def drop_users():
        model = get_object_model("user")
        model.query.delete()
        db_commit()

    request.addfinalizer(drop_users)
