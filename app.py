from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html.j2", title="Home")


@app.route("/location")
def location():
    return render_template('location.html.j2',title="location")

@app.route("/")
def shoppingbag():
    return render_template("shoppingbag.html.j2",title="shoppingbag")