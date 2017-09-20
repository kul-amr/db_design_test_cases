import os
import pytest
from ..app import create_app
from ..backend.models import db as loansdb

TESTDB_PATH = os.path.join(os.path.dirname(__file__), 'test.db')
TEST_DATABASE_URI = 'sqlite:///{}'.format(TESTDB_PATH)

@pytest.fixture(scope='session')
def app(request):
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TESTDB_PATH,
        'SQLALCHEMY_TRACK_MODIFICATIONS' : True
    }

    loans_app=create_app(config=settings_override)

    app_context = loans_app.app_context()
    app_context.push()

    return loans_app

@pytest.fixture(scope='session')
def db(app, request):
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    loansdb.app = app
    loansdb.create_all()

    return loansdb

@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session





