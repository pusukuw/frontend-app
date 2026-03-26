import os
import sys
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_input')
    if user_input:
        # Process user input
        return redirect(url_for('result', input=user_input))
    return redirect(url_for('index'))

@app.route('/result/<input>')
def result(input):
    return render_template('result.html', user_input=input)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)