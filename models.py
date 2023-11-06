from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Student(db.Model):
    #__tablename__='student'
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(100),nullable = False)
    last_name = db.Column(db.String(100),nullable = False)
    gender_id = db.Column(db.Integer,db.ForeignKey('gender.id'),nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    age = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer)
    
    gender = db.relationship('Gender', back_populates='students')
    
    def __repr__(self):
        return f'Student ({self.id},{self.first_name},{self.last_name},{self.email},{self.age})'

class Gender(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_latin = db.Column(db.String(10),nullable = False)
    acronym = db.Column(db.String(4),nullable = False)
    created_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer)
    
    students = db.relationship('Student', back_populates='gender')
    
    def __repr__(self):
        return f'Gender ({self.id},{self.name_latin},{self.acronym})'