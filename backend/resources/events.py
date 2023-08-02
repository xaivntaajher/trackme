from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Event
from database.schemas import events_schema, event_schema


class EventTableResource(Resource):
    @jwt_required()
    def get(self):
        type = request.args.get('type')
        events = Event.query
        # Check params key value 'type', which can be either class or tournament
        if type:
            events = events.filter_by(type=type)
        
        events = events.all()

        return events_schema.dump(events), 200
    
    @jwt_required()
    def post(self):
        # if not user_id.is_coach:
        #     return {'message': 'Unauthorized access'}, 401
        
        user_id = get_jwt_identity()
        form_data = request.get_json()
        new_event = event_schema.load(form_data)
        new_event.user_id = user_id
        db.session.add(new_event)
        db.session.commit()
        return event_schema.dump(new_event), 201
    

class EventResource(Resource):
    @jwt_required()
    def put(self, event_id):
        user_id = get_jwt_identity()
        edit_event = Event.query.get_or_404(event_id)
        
        # if not user_id.is_coach:
        #     return {'message': 'Unauthorized access'}, 401

        if 'type' in request.json:
            edit_event.type = request.json['type']
        if 'points' in request.json:
            edit_event.points = request.json['points']
        if 'title' in request.json:
            edit_event.title = request.json['title']
        if 'date' in request.json:
            edit_event.date = request.json['date']
        if 'capacity' in request.json:
            edit_event.capacity = request.json['capacity']
        db.session.commit()
        return event_schema.dump(edit_event), 200
    
class EventInformationResource(Resource):
    @jwt_required()
    #get event information by id
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return event_schema.dump(event), 201