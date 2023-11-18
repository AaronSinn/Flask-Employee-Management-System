#TODO restrcture and make this a run.py maybe
from flask import Flask, render_template, url_for
from forms import LoginForm

app = Flask(__name__)
app.secret_key = "RickyDickyDooDahGrimes"

@app.route('/')
def Login():
    form = LoginForm()
    
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)