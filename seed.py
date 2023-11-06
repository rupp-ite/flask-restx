from models import *

def seed_gender():
    if Gender.query.count()==0:
        print('Insert gender')
        genders = [
            Gender(name_latin='Female', acronym='F'),
            Gender(name_latin='Male', acronym='M')
        ]
        db.session.add_all(genders)
        db.session.commit()