#TODO restrcture and make this a run.py maybe
from flask import Flask, render_template, url_for
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.secret_key = "RickyDickyDooDahGrimes"

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm()

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)