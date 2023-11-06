from flask import Flask, request, json
from flask_restx import Api, Resource, fields, reqparse
from config import Config
from models import db, Student, Gender
config = Config()

app = Flask(__name__)

api = Api(app)
api_ns = api.namespace("api", path='/' , description="API")

app.config.from_object(config)

db.init_app(app)

with app.app_context():
    db.create_all()
    from seed import seed_gender
    seed_gender()

gender_fields = api.model('Gender',{
        'name_latin': fields.String,
        'acronym':fields.String
    }
)

gender_parser = reqparse.RequestParser()
gender_parser.add_argument('name_latin', type=str, required=False, help='Enter gender')
gender_parser.add_argument('acronym', type=str, required=False, help='Short of Gender')

@api_ns.route('/gender')
class ManageGender(Resource):
    @api_ns.marshal_list_with(gender_fields)
    def get(self):
        args = gender_parser.parse_args()
        name_latin = args['name_latin']
        acronym = args['acronym']
        q = Gender.query
        if name_latin:
            q = q.filter(Gender.name_latin.like(f'%{name_latin}%'))
        if acronym:
            q = q.filter(Gender.acronym.like(f'%{acronym}%'))
        result = q.all()
        return result
    
    @api_ns.expect(gender_fields)
    @api_ns.marshal_with(gender_fields)
    def post(self):
        args = api.payload
        item = Gender(**args)
        db.session.add(item)
        db.session.commit()
        return item

@api_ns.route('/gender/<int:id>')
class ManageGender(Resource):
    @api_ns.marshal_with(gender_fields)
    def get(self,id):
        gender = Gender.query.get(id)
        if gender:
            return gender
        api.abort(404, f"Gender {id} is not found")

    @api_ns.expect(gender_fields)
    @api_ns.marshal_with(gender_fields)
    def put(self,id):
        gender = Gender.query.get(id)
        if gender:
            args = api.payload
            gender.name_latin = args['name_latin']
            gender.acronym = args['acronym']
            db.session.commit()
            return gender
    
    def delete(self, id):
        gender = Gender.query.get(id)
        if gender:
            db.session.delete(gender)
            db.session.commit()
            return 'Not workding'

if __name__=='__main__':
    app.run()
