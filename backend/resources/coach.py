from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, User
from database.schemas import users_schema, user_schema

class CoachResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_info = User.query.all()
        return users_schema.dump(user_info), 200
     
class CoachReviewResource(Resource):
    @jwt_required()
    def put(self, user_id):
        coach_id = get_jwt_identity()
        coach = User.query.get_or_404(coach_id)

        if not coach.is_coach:
            return {'message': 'Unauthorized access'}, 401
        
        edit_user = User.query.get_or_404(user_id)

        if 'first_name' in request.json:
            edit_user.first_name = request.json['first_name']
        if 'last_name' in request.json:
            edit_user.last_name = request.json['last_name']
        if 'start_date' in request.json:
            edit_user.start_date = request.json['start_date']
        if 'last_promotion' in request.json:
            edit_user.last_promotion = request.json['last_promotion']
        if 'point_total' in request.json:
            edit_user.point_total = request.json['point_total']
        if 'pin' in request.json:
            edit_user.pin = request.json['pin']
        db.session.commit()
        return user_schema.dump(edit_user), 200

    
    @jwt_required()
    def patch(self, user_id):
        coach_id = get_jwt_identity()
        coach = User.query.get_or_404(coach_id)

        if not coach.is_coach:
            return {'message': 'Unauthorized access'}, 401

        user = User.query.get_or_404(user_id)

        if user.is_coach:
            user.is_coach = False
        else:
            user.is_coach = True
        db.session.commit()

        return {'message': 'User profile updated successfully'}, 200
    
    @jwt_required()
    def delete(self, coach_id):
        user_id = get_jwt_identity()
        delete_info = User.query.get_or_404(coach_id)
        db.session.delete(delete_info)
        db.session.commit()
        return '', 204