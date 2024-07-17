from flask import Flask, render_template
import random as rand
app=Flask(__name__, template_folder="templates" ,static_folder="static")

fortunes=["Your cat secretly hates you.","A burrito will change your life today.","You will find a sock that’s been missing for months.","Beware of the yogurt, it’s not as fresh as it seems.","You will eat something today that you’ll regret tomorrow.","Your Wi-Fi will work when you need it least.","An awkward moment will lead to a hilarious story.","You will step on a Lego, but you will survive.","The fortune you seek is in another cookie.","You will win an argument with a toddler."]
@app.route("/home")
def home():
	return render_template("home.html")
@app.route("/fortune")
def fortune():
	thefort=rand.choice(fortunes)
	return render_template("fortune.html",fortune=thefort)

if __name__ == '__main__':
    app.run(debug=True)
