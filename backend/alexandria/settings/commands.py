import os
import shutil
import click
from datetime import datetime, timedelta
from flask import current_app as app
from sqlalchemy.sql.expression import false
from alexandria.settings.extensions import db

__author__ = 'oclay'



@click.command()
@click.option('--username', prompt=True, help='The username for the admin')
@click.option('--password', help='The password for the admin', prompt=True, hide_input=True,
              confirmation_prompt=True)
def create_admin(username, password):
    """Create an admin user by default"""
    from alexandria.modules.security.models import User
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, password=password, role=u'admin', active=True)
        db.session.add(user)
        db.session.commit()
        click.echo('Success create user')
    else:
        click.echo('User with username %s already exist' % username)


def __remove_files():
    shutil.rmtree(app.config['DOCUMENTS_ROOT'])
    os.mkdir(app.config['DOCUMENTS_ROOT'])
    shutil.rmtree(app.config['THUMBNAILS_ROOT'])
    os.mkdir(app.config['THUMBNAILS_ROOT'])


def __delete_users_and_documents():
    from alexandria.modules.core.models import Document
    from alexandria.modules.security.models import User
    Document.query.delete()
    User.query.delete()
    db.session.commit()


@click.command()
def clean():
    """Remove all docs,indexes ,and files"""

    app.engine.rebuild_index()
    __remove_files()
    __delete_users_and_documents()
    click.echo('Zero km, done!')

@click.command()
def remove_files():
    """Delete all documents and thumbnails files"""
    
    __remove_files()
    click.echo('Success delete files')


@click.command()
def rebuild_index():
    """Clear the index """
    
    app.engine.rebuild_index()
    click.echo('Success clearing index')


def remove_activation():
    from alexandria.modules.security.models import AccountRegistration, User
    expiration_date = timedelta(days=app.config['ACCOUNT_ACTIVATION_DAYS'])
    sq = AccountRegistration.query.with_entities(AccountRegistration.user_id.label('id')).join(User).filter(
        User.joined_date < datetime.now() - expiration_date).filter(User.active == False).subquery()
    User.query.filter(User.id.in_(sq)).delete(synchronize_session=False)
    db.session.commit()


@click.command()
def remove_activation_expired():
    """Remove account activation"""
    remove_activation()
    click.echo("All expired registrations were deleted")
