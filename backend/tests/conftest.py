import os
import pytest

from alexandria.factory import create_app
from flask.helpers import get_debug_flag
from alexandria.settings.config import ProdConfig, DevConfig
from alexandria.settings.extensions import db as _db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def app():
    """
    Setting Flask app for testing
    """
    config = DevConfig() if get_debug_flag() else ProdConfig()
    _app = create_app(config)
    ctx = _app.app_context()
    ctx.push()
    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session
    yield session
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='session')
def user_test(db):
    from alexandria.modules.security.models import User
    user = User(username='test')
    db.session.add(user)
    db.session.commit()

@pytest.fixture(scope='session')
def admin_user(db):
    from alexandria.modules.security.models import User
    admin_user = User(username = 'admin',email = 'admin@admin.com',role = u'admin')
    db.session.add(admin_user)
    db.session.commit()

@pytest.fixture(scope='session')
def resources_path():
    return os.path.join(BASE_DIR, 'resources')
