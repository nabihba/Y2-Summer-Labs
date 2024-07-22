import pyrebase
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session

Config = {
    "apiKey": "AIzaSyCy8SltKlUFT5oi5JUEUJDTpq8ol9ixYo0",
    "authDomain": "authentication-lab-76c53.firebaseapp.com",
    "projectId": "authentication-lab-76c53",
    "storageBucket": "authentication-lab-76c53.appspot.com",
    "messagingSenderId": "355323432502",
    "appId": "1:355323432502:web:a87b3964c20ec3c997d297",
    "measurementId": "G-296NTRVJXC",
    "databaseURL": "https://authentication-lab-76c53-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'Your_secret_string'
firebase = pyrebase.initialize_app(Config)
db = firebase.database()
auth = firebase.auth()

@app.route("/home", methods=["GET", "POST"])
def home():
    if 'user' not in login_session:
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        text = request.form['quote']
        said_by = request.form['speaker']
        info = request.form['info']
        
        quote = {
            'text': text,
            'said_by': said_by,
            'info': info,
            'uid': login_session['user']['localId']
        }
        
        db.child("Quotes").push(quote)
        return redirect(url_for('thanks'))
    
    return render_template('home.html', email=login_session['user']['email'])

@app.route("/display")
def display():
    quotes_dict = db.child("Quotes").get().val()
    return render_template('display.html', quotes=quotes_dict)

@app.route("/thanks")
def thanks():
    return render_template('thanks.html')

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            login_session['user'] = user
            login_session['quotes'] = []

            user_data = {
                'full_name': full_name,
                'email': email,
                'username': username
            }
            
            uid = login_session['user']['localId']
            db.child("Users").child(uid).set(user_data)

            return redirect(url_for('home'))
        except:
            error_message = "Authentication failed"
            return render_template("error.html", error_message=error_message)
    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            if 'quotes' not in login_session:
                login_session['quotes'] = []
            return redirect(url_for('home'))
        except:
            error_message = "Authentication failed"
            return render_template("error.html", error_message=error_message)
    return render_template("signin.html")

@app.route("/signout", methods=["POST"])
def signout():
    login_session.pop('user', None)
    login_session.pop('quotes', None)
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
