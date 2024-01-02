from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "nsakjdhakjsndank12n2n123nj12bnb41sd@!&@#$JBN*!!MSMMAKLL@@!@312d"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/eflight" % quote("Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)