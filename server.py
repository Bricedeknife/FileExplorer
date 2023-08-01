from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return "Logged in"
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)