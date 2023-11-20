from models import *

def seed_user():
    if User.query.count()==0:
        print('Adding users')
        users = [
            User(username='user1', password='Pass2357'),
            User(username='user2', password='Rupp2357')
        ]
        db.session.add_all(users)
        db.session.commit()

def seed_gender():
    if Gender.query.count()==0:
        print('Insert gender')
        genders = [
            Gender(name_latin='Female', acronym='F'),
            Gender(name_latin='Male', acronym='M')
        ]
        db.session.add_all(genders)
        db.session.commit()