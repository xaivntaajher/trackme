from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, User, Rank, Promotion
from database.schemas import promotions_schema, promotion_schema, ranks_schema


class PromoteStudentResource(Resource):
    @jwt_required()
    def post(self):
        coach_id = get_jwt_identity()
        coach = User.query.get(coach_id)
        if coach.is_coach:
            form_data = request.get_json()

            
            id = form_data.get("id")  
            date = form_data.get("date")  
            user_id = form_data.get("user_id")  
            rank_id = form_data.get("rank_id")  

            new_promotion = Promotion(id=id, date=date, user_id=user_id, rank_id=rank_id)
            db.session.add(new_promotion)
            db.session.commit()

            return promotion_schema.dump(new_promotion)

        return {"message": ""}, 401

class RankResource(Resource):
    @jwt_required()
    def get(self):
        all_rank = Rank.query.all()  
        return ranks_schema.dump(all_rank) 