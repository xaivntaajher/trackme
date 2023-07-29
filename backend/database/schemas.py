from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields
from database.models import User, Car

ma = Marshmallow()

class RankSchema(ma.Schema):
 
    id = fields.Integer(primary_key=True)
    points_required = fields.Integer()
    title = fields.String(required=True)
    is_child_rank = fields.Boolean()

    class Meta:
        fields = ("id", "points_required", "title", "is_child_rank")

    @post_load
    def create_userevent(self, data, **kwargs):
        return Rank(**data)
    
rank_schema = RankSchema()
ranks_schema = RankSchema(many=True)

class PromotionSchema(ma.Schema):
    date = fields.Date()
    user_id = fields.Integer()
    rank_id = fields.Integer()
    rank = ma.Nested(RankSchema)

    @post_load
    def create_promotion(self, data, **kwargs):
        return Promotion(**data)

    class Meta:
        fields = ("date", "id", "user_id", "rank_id", "rank")
        load_instance = True

promotion_schema = PromotionSchema()
promotions_schema = PromotionSchema(many=True)

# Auth Schemas
class RegisterSchema(ma.Schema):
    """
    Schema used for registration, includes password
    """
    id = fields.Integer(primary_key=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    pin = fields.String(required=True)
    class Meta:
        fields = ("id", "username",  "password", "first_name", "last_name", "email", "pin")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
    
class UserSchema(ma.Schema):
    """
    Schema used for displaying users, does NOT include password
    """
    id = fields.Integer(primary_key=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    is_coach = fields.Boolean()
    pin = fields.String(required=True)
    start_date = fields.Date()
    last_promotion = fields.Date()
    point_total = fields.Integer()
    rank_id = fields.Integer()
    rank = ma.Nested(RankSchema, many=False)
    events = ma.Nested("EventSchema", many=True, exclude=("users",))
    promotions = ma.Nested(PromotionSchema, many=True)

    class Meta:
        fields = ("id", "username", "first_name", "last_name", "is_coach", "start_date", "last_promotion", "point_total", "rank_id", "rank", "events", "promotions")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)

register_schema = RegisterSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Car Schemas
class CarSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    make = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Integer()
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)
    class Meta:
        fields = ("id", "make", "model", "year", "user_id", "user")
    
    @post_load
    def create_car(self, data, **kwargs):
        return Car(**data)

car_schema = CarSchema()
cars_schema = CarSchema(many=True)


# TODO: Add your schemas below

class EventSchema(ma.Schema):

    id = fields.Integer(primary_key=True)
    type = fields.String()
    points = fields.Integer(required=True)
    title = fields.String()
    date = fields.Date()
    capacity = fields.Integer()
    users = ma.Nested(UserSchema, many=True, exclude=("events",))

    class Meta:
        fields = ("id", "type", "points", "title", "date", "capacity", "users")

    @post_load
    def create_event(self, data, **kwargs):
        return Event(**data)

event_schema = EventSchema()
events_schema = EventSchema(many=True)

class UserEventSchema(ma.Schema):
 
    id = fields.Integer(primary_key=True)
    user_id = fields.Integer()
    event_id = fields.Integer()

    @post_load
    def create_userevent(self, data, **kwargs):
        return User(**data)
    class Meta:
        fields = ("id", "user_id", "event_id",)
        load_instance = True

userevent_schema = UserEventSchema()
userevents_schema = UserEventSchema(many=True)

    
