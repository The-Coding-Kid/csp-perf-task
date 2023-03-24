from flask import Flask, render_template, request, Response, jsonify
import json

app = Flask(__name__)

todolist = ["hello world", "world", "hello"]

@app.route('/', methods=['GET', 'POST'])
def home_route():
    if(request.method == 'GET'):
        return render_template('index.html', todos=todolist)
    else:
        text = request.form['todo']
        todolist.append(text)
        return render_template('index.html', todos=todolist)
               
@app.route('/todos', methods=['GET'])
def get_todos():
    if(request.method != 'GET'):
        return Response("Method not allowed", status=405)
    else:
        return jsonify(todolist)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)