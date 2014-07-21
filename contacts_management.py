from flask import Flask
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
db = SQLAlchemy(app)


class Contacts(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(Text, unique=False)
    last_name = Column(Text, unique=False)
    phone = Column(Integer, unique=True)
    email = Column(Text, unique=True)


db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Contacts, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/')
def index():
    return app.send_static_file("index.html")


app.debug = True

if __name__ == '__main__':
    app.run()
