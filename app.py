from flask import Flask, render_template, request, Response, jsonify
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
# todolist = ["hello world", "world", "hello"]

@app.before_first_request
def create_database():
     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home_route():
    if(request.method == 'GET'):
        return render_template('index.html', todos=Todo.query.all())
    else:
        text = request.form['todo']
        todo = Todo(todo=text)
        db.session.add(todo)
        db.session.commit()
        return render_template('index.html', todos=Todo.query.all())
               
@app.route('/todos', methods=['GET'])
def get_todos():
    if(request.method == 'GET'):
        print("Request received")
        todos = Todo.query.all()
        return todos


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)