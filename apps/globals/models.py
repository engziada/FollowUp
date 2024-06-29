
from datetime import datetime
from flask_login import current_user

from apps import db
from sqlalchemy import event

class Profile_Actions(db.Model):
    __tablename__ = "profile_actions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key column
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'), nullable=False)
    notes= db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.Date, nullable=True, default=db.func.current_date())
    creation_time = db.Column(db.Time, nullable=True, default=db.func.current_time())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    # Relationships
    profile = db.relationship("Profile", backref=db.backref("profile_actions", lazy=True))
    action = db.relationship("Action", backref=db.backref("profile_actions", lazy=True))
    creator = db.relationship("Users", backref=db.backref("created_actions", lazy=True))
   # Composite unique constraint
    # __table_args__ = (UniqueConstraint('profile_id', 'action_id', name='_profile_action_uc'),)
        

@event.listens_for(Profile_Actions, "before_insert")
def before_insert_listener(mapper, connection, target):
    if current_user.is_authenticated:
        target.created_by = current_user.id
