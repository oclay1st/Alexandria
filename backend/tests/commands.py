from alexandria.settings.commands import remove_activation
from alexandria.settings.extensions import db
from datetime import datetime,timedelta

def test_remove_activation_expired(client):
    from alexandria.modules.security.models import User,AccountRegistration
    days_to_expire6,days_to_expire8 = timedelta(days=6),timedelta(days=8)    
    user1 = User(username='test_activation',joined_date=datetime.now()- days_to_expire6)
    user2 = User(username='test_activation2',joined_date=datetime.now()- days_to_expire8)
    activation1 = AccountRegistration(user=user1)
    activation2 = AccountRegistration(user=user2)
    db.session.add_all([activation1,activation2])
    remove_activation() # do commmit to the datebase
    assert db.session.query(User.query.filter(User.username == 'test_activation').exists()).scalar()
    assert not db.session.query(User.query.filter(User.username == 'test_activation2').exists()).scalar()
