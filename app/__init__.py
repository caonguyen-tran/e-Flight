from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "nsakj@!@&#&!@$*@12351bnb41sd@!&@#$JBN*!!MSMMAKLL@@!@312d"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/eflight" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(
    cloud_name="dndakokcz",
    api_key="654943155445479",
    api_secret="Orf7PiRmpS7T3HPdEUl36nQUraU"
)