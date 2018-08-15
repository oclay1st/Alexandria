from alexandria.modules.security.models import User
from alexandria.modules.security.utils import follow_user, unfollow_user

__author__ = 'oclay'


def test_password_setter(client,db):
    user = User(username='test')
    user.password = 'test'
    db.session.add(user_test)
    user = User.query.filter_by(username='test').first()
    assert user.check_password('test') == True
    db.session.delete(user)
    db.session.commit()


def test_follow(db):
    admin = User.query.filter_by(username='admin').first()
    test = User.query.filter_by(username='test').first()
    follow_user(test.id, admin)
    assert admin.followed.count() == 1
    unfollow_user(test.id, admin)
    assert admin.followed.count() == 0
