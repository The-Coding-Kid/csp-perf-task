from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home_route():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)