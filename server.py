from flask import Flask, render_template, request, Response, jsonify
import json

app = Flask(__name__)

todolist = ["hello world", "world", "hello"]

@app.route('/')
def home_route():
    return render_template('index.html', todos=todolist)


@app.route('/add-todo', methods=['POST'])
def add_todo_route():
    if(request.method != 'POST'):
        return Response("Method not allowed", status=405)
    else:
        text = request.form['todo']
        todolist.append(text)
        
        
@app.route('/todos', methods=['GET'])
def get_todos():
    if(request.method != 'GET'):
        return Response("Method not allowed", status=405)
    else:
        return jsonify(todolist)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)