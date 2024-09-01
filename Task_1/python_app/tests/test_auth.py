import pytest
from flask import g, session
from flaskExample.db import get_db


# Testing if app:
# 1) Correctly responses to the GET requests of the register page
# 2) Correctly redirects to the Login page after posting registration data
# 3) Newly registered user exists in the database
# ...
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None
# ...
# 4) If app correctly notifies user if something is wrong with registration
# ...
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data
# ...
# 5) Correctly responses to the GET requests of the login page
# 6) Correctly redirects to the index page after posting login data
# 7) Logged in user data is in the user's cookies and session data
# ...
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'
# ...
# 8) If app correctly notifies user if something is wrong with
#    information provided during process of logging in
# ...
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
# ...
# 9) Session is cleared out after user logs out of the system
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session