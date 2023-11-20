from flask import Flask, request, json
from flask_restx import Api, Resource, fields, reqparse
from config import Config
from models import db, Student, Gender, User
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity 
config = Config()

app = Flask(__name__)

api = Api(app)
api_ns = api.namespace("api", path='/' , description="API")

app.config.from_object(config)

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    from seed import seed_gender, seed_user
    seed_gender()
    seed_user()

# User payload for input validation
user_payload = api.model(
    'UserPayload',{
        'username':fields.String(required=True),
        'password':fields.String(required=True)
    }
)

@api_ns.route('/register')
class ManageUser(Resource):
    @api_ns.expect(user_payload)
    def post(self):
        data = api.payload
        username = data.get('username')
        password = data.get('password')
        if User.query.filter_by(username=username).first():
            return {
                'message':'User already exists'
            }, 400
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return {
            'message':'User registered successfully'
        }, 201

@api_ns.route('/login')
class UserLogin(Resource):
    @api_ns.expect(user_payload)
    def post(self):
        data = api.payload
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password'}, 401
    
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
    @jwt_required()
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
            return {"message": f"Item {id} has been deleted"}, 204
        api.abort(404, f"Item {id} not found")

if __name__=='__main__':
    app.run()
