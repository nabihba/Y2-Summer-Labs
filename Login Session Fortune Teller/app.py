from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'Your_secret_string'

fortunes = [
    "Your cat secretly hates you.",
    "A burrito will change your life today.",
    "You will find a sock that’s been missing for months.",
    "Beware of the yogurt, it’s not as fresh as it seems.",
    "You will eat something today that you’ll regret tomorrow.",
    "Your Wi-Fi will work when you need it least.",
    "An awkward moment will lead to a hilarious story.",
    "You will step on a Lego, but you will survive.",
    "The fortune you seek is in another cookie.",
    "You will win an argument with a toddler."
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        birth_month = request.form['birth_month']
        login_session['name'] = name
        login_session['birth_month'] = birth_month
        
        if len(birth_month) > len(fortunes):
            login_session['fortune'] = "Unavailable fortune"
        else:
            index = len(birth_month) % len(fortunes)
            login_session['fortune'] = fortunes[index]
            
        return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/home")
def home():
    name = login_session.get('name', '')
    birth_month = login_session.get('birth_month', '')
    return render_template("home.html", name=name, birth_month=birth_month)

@app.route("/fortune")
def fortune():
    fortune = login_session.get('fortune', 'No fortune available')
    return render_template("fortune.html", fortune=fortune)

if __name__ == '__main__':
    app.run(debug=True)
