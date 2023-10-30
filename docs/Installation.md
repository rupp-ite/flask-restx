Installation
===
### Flask-restx installation
    
    flask==2.3.3
    flask-restx
    flask-sqlalchemy
    psycopg2
    psycopg2-binary

### A Minimal API

    from flask import Flask
    from flask_restx import Resource, Api

    app = Flask(__name__)
    api = Api(app)

    @api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}

    if __name__ == '__main__':
        app.run(debug=True)

