from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, User, Event
from database.schemas import events_schema, user_schema

class StudentResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        available_classes = Event.query.all()
        available_classes_data = events_schema.dump(available_classes)

        return {'available_events': available_classes_data}, 200

class StudentCheckInResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        event_id = request.json.get('event_id')
        pin = request.json.get('pin')

        if not event_id or not pin:
            return {'message': 'Invalid request'}, 400

        enrolled_event = Event.query.get(event_id)
        if not enrolled_event:
            return {'message': 'Invalid event ID'}, 404

        if enrolled_event not in user.events:
            return {'message': 'You are not enrolled in this event'}, 400

        if user.pin != pin:
            return {'message': 'Invalid pin'}, 401
        # Checks event type and gives points according to type
        if enrolled_event.type == 'class':
            points_earned = enrolled_event.points
        elif enrolled_event.type == 'tournament':
            points_earned = enrolled_event.points
        else:
            return {'message': 'Invalid event type'}, 400

        # Update the user's point_total based on the event points
        user.point_total += points_earned
        db.session.commit()

        return {'message': 'Check-in successful', 'point_total': user.point_total,
        'points_earned': points_earned
        }, 200

class StudentEnrollmentResource(Resource):
    @jwt_required()
    def post(self, event_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        event = Event.query.get_or_404(event_id)

        # Check if the user is already enrolled in the event
        if event in user.events:
            return {'message': 'You are already enrolled in this event'}, 400

        # Enroll the user in the event
        user.events.append(event)
        db.session.commit()

        return {'message': 'Enrollment successful'}, 200
    
class StudentInformationResource(Resource):
    @jwt_required()
    #get student information by id
    def get(self, user_id):
        student = User.query.get_or_404(user_id)
        return user_schema.dump(student)
