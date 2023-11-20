Resourceful Routing
===

The main building block provided by Flask-RESTX are resources. Resources are built on top of Flask pluggable views, giving you easy access to multiple HTTP methods just by defining methods on your resource. A basic CRUD resource for a todo application (of course) looks like this:

    from flask import Flask, request
    from flask_restx import Resource, Api

    app = Flask(__name__)
    api = Api(app)

    todos = {}

    @api.route('/<string:todo_id>')
    class TodoSimple(Resource):
        def get(self, todo_id):
            return {todo_id: todos[todo_id]}

        def put(self, todo_id):
            todos[todo_id] = request.form['data']
            return {todo_id: todos[todo_id]}

    if __name__ == '__main__':
        app.run(debug=True)