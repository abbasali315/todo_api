from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

todos = {
    1: {'task': 'Write APIs', 'summary': 'Write APIs using flask restful'},
    2: {'task': 'To do APIs', 'summary': 'Write APIs using flask restful'},
    3: {'task': 'Authentication APIs', 'summary': 'Write APIs using flask restful'},
    4: {'task': 'Email verification APIs', 'summary': 'Write APIs using flask restful'}
}

task_args = reqparse.RequestParser()
task_args.add_argument('task', type=str, help='Task title required', required=True)
task_args.add_argument('summary', type=str, help='Kindly give some summary', required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument('task', type=str)
task_put_args.add_argument('summary', type=str)


class Todos(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        task = task_args.parse_args()
        if todo_id in todos:
            abort(409, message='Task Id already exist')
        else:
            todos[todo_id] = task
        return todos[todo_id]

    def delete(self, todo_id):
        del todos[todo_id]
        return todos

    def put(self, todo_id):
        args = task_put_args.parse_args()
        if todo_id not in todos:
            abort(404, message='Task not found with requested ID')
        if args['task']:
            todos[todo_id]['task'] = args['task']
        if args['summary']:
            todos[todo_id]['summary'] = args['summary']
        return todos[todo_id]


class TodoList(Resource):
    def get(self):
        return todos


api.add_resource(Todos, '/todo/<int:todo_id>')
api.add_resource(TodoList, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
