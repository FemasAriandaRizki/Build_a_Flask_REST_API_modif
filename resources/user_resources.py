from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import UserModel, db

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()

        if not args["name"].strip():
            abort(400, message="Name cannot be empty")
        if not args["email"].strip():
            abort(400, message="Email cannot be empty")

        if UserModel.query.filter_by(name=args["name"]).first():
            abort(400, message="User with this name already exists")
        if UserModel.query.filter_by(email=args["email"]).first():
            abort(400, message="User with this email already exists")
        
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")

        if args["name"]:
            if UserModel.query.filter_by(name=args["name"]).first():
                abort(400, message="User with this name already exists")
            user.name = args["name"]

        if args["email"]:
            if UserModel.query.filter_by(email=args["email"]).first():
                abort(400, message="User with this email already exists")
            user.email = args["email"]

        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserByName(Resource):
    @marshal_with(user_fields)
    def get(self, name):
        user = UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, message="User not found")
        return user
