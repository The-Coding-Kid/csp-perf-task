# Python packages not part of the Python interpreter being used: Flask and FLask-SQLAlchemy
# Database(data abstraction) being used: SQLite3
# citations:
# Flask(source code): https://github.com/pallets/flask/
# Flask(documentation): https://flask.palletsprojects.com/en/2.2.x/
# Flask-SQLAlchemy(source code): https://github.com/pallets-eco/flask-sqlalchemy/
# Flask-SQLAlchemy(documentation): https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/
# SQLite3(homepage): https://sqlite.org/index.html
# SQLite3(documentation): https://www.sqlite.org/docs.html
from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"id: {self.id}, todo: {self.todo}, completed: {self.completed}"


@app.before_first_request
def create_database():
     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home_route():
    if(request.method == 'GET'):
        return render_template('index.html', todos=Todo.query.all())
    else:
        if(request.form.get('add todo')):
            text = request.form['todo']
            todo = Todo(todo=text)
            db.session.add(todo)
            db.session.commit()
            return render_template('index.html', todos=Todo.query.all())
        elif(request.form.get('complete')):
            task = request.form.get('id')
            print(task)
            return render_template('index.html', todos=Todo.query.all())
               
@app.route('/todos', methods=['GET'])
def get_todos():
    if(request.method == 'GET'):
        print("Request received")
        todos = Todo.query.all()
        return todos

@app.route("/change/<int:todo_id>/<int:task>", methods=['GET', 'POST'])
def change(todo_id, task):
    todos = Todo.query.all()
    if(task == 0):
        for todo in todos:
            if(todo.id == todo_id):
                todo.completed = not todo.completed
                db.session.commit()
                break
    else:
        for todo in todos:
            if(todo.id == todo_id):
                db.session.delete(todo)
                db.session.commit()
                break   
    return redirect(url_for("home_route"))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)