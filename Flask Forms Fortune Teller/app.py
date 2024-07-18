from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates", static_folder="static")

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

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        birth_month = request.form['birth_month']
        return redirect(url_for('fortune', birth_month=birth_month))
    return render_template("home.html")

@app.route("/fortune")
def fortune():
    birth_month = request.args.get('birth_month', '')
    if len(birth_month) > len(fortunes):
        thefort = "Unavailable fortune"
    else:
        index = len(birth_month) % len(fortunes)
        thefort = fortunes[index]
    return render_template("fortune.html", fortune=thefort, birth_month=birth_month)

if __name__ == '__main__':
    app.run(debug=True)
