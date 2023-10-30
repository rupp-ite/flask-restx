Endpoints
===
Many times in an API, your resource will have multiple URLs. You can pass multiple URLs to the route() decorator, on the Api object. Each one will be routed to your Resource

    import json
    from flask import Flask, request
    from flask_restx import Resource,Api

    app = Flask(__name__)

    api = Api(app)

    todos = {}

    @api.route('/<string:todo_id>','/tasks/<string:todo_id>')
    class TodoSimple(Resource):
        
        def put(self, todo_id):
            todos[todo_id] = request.form['data']
            return {todo_id: todos[todo_id]}
        
        def get(self, todo_id):
            return todos if todo_id=='0' else {todo_id: todos[todo_id]}
        
    if __name__ == '__main__':
        app.run(debug=True)