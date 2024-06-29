from flask_login import current_user
from apps import db
from icecream import ic
from sqlalchemy import event


# Define Influencers Model
class Action(db.Model):
    __tablename__ = "actions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))
    steps = db.Column(db.String(255))
    due_days = db.Column(db.Integer)
    alert = db.Column(db.String(255))
    establishment = db.Column(db.String(255))
    creation_date = db.Column(db.Date, nullable=True, default=db.func.current_date())
    creation_time = db.Column(db.Time, nullable=True, default=db.func.current_time())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    creator = db.relationship("Users", backref=db.backref("actions", lazy=True))


@event.listens_for(Action, "before_insert")
def before_insert_listener(mapper, connection, target):
    if current_user.is_authenticated:
        target.created_by = current_user.id
