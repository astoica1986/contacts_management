from flask import Flask,jsonify
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import validates
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
db = SQLAlchemy(app)


class Contacts(db.Model):
    id = Column(Integer, primary_key=True)
    firstName = Column(Text(20), unique=False)
    lastName = Column(Text(20), unique=False)
    phone = Column(Integer, unique=True)
    email = Column(Text, unique=True)

    @validates('email')
    def validate_email(self, key, address):
        try:
            assert '@' in address
        except AssertionError:
            return jsonify(error="Invalid JSON Provided")
        return address


db.create_all()


api_manager = APIManager(app, flask_sqlalchemy_db=db)


def get_many_postprocessor(result=None, **kw):
    #result = dict((key, value) for key, value in result.items() if key == 'objects')
    #print(result)
     # Grab the list of objects so we can wipe the result dict
    temp = result['objects']
    # Remove all key/value pairs from the result dict
    result.clear()
    # Add the 'persons' key and set it equal to the list
    # of objects from the original result dict
    result['objects'] = temp


api_manager.create_api(Contacts,
                       methods=['GET', 'POST', 'DELETE', 'PUT'],
                       postprocessors={'GET_MANY': [get_many_postprocessor]})


@app.route('/')
def index():
    return app.send_static_file("index.html")


app.debug = True

if __name__ == '__main__':
    app.run()
