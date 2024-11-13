from flask import Flask
from flask_restful import Api
from config import Config
from models import db
from resources.user_resources import Users, User, UserByName

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(UserByName, '/api/users/name/<string:name>')

@app.route('/')
def home():
    return '<h1>Welcome to the Flask REST API</h1>'

if __name__ == '__main__':
    app.run()
