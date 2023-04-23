from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import json
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

@app.route("/update/<int:todo_id>", methods=['GET', 'POST'])
def update(todo_id):
    todos = Todo.query.all()
    for todo in todos:
        if(todo.id == todo_id):
            todo.completed = not todo.completed
            db.session.commit()
            break
    return redirect(url_for("home_route"))


@app.route('/delete/<int:todo_id>', methods=['GET', 'POST'])
def delete_route(todo_id):
    todos = Todo.query.all()
    for todo in todos:
        if(todo.id == todo_id):
            db.session.delete(todo)
            db.session.commit()
            break
    return redirect(url_for('home_route'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)