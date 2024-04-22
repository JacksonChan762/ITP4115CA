from flask import Flask
#Import necessary extensions
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

#Initialize the Flask application
app = Flask(__name__)

#Define a basic route to test
@app.route("/")
def hello_world():
    return 'Hello,world!'

#Run app if the file is executed
if __name__ == '__main__':
    app.run(debug=True)

#Initialize extensions
db = SQLAlchemy(app)
         