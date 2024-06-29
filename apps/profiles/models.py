from datetime import datetime
from flask_login import current_user
from apps import db
from werkzeug.utils import secure_filename
from os import path, makedirs
from flask import current_app, request
from icecream import ic
from sqlalchemy import event
from apps.globals.models import Profile_Actions


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False, unique=True)
    about = db.Column(db.Text)
    est_date = db.Column(db.Date)
    account_manager = db.Column(db.String(255))
    account_manager_email = db.Column(db.String(255))
    phones= db.Column(db.String(255))
    address= db.Column(db.String(255))
    actions = db.relationship("Action", secondary=Profile_Actions.__table__, backref=db.backref('profiles', lazy='dynamic'))
    creation_date = db.Column(db.Date, nullable=True, default=db.func.current_date())
    creation_time = db.Column(db.Time, nullable=True, default=db.func.current_time())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    creator = db.relationship("Users", backref=db.backref("profiles", lazy=True))

# def set_code(target, value, oldvalue, initiator):
#     """Event listener to automatically generate the code field."""
#     if not target.creation_date:
#         # If creation_date is not set, use the current year
#         current_year = datetime.now().year
#     else:
#         current_year = target.creation_date.year

#     # Assuming id is available; if not, this part needs adjustment
#     target.code = f"DMO{current_year}{target.id}"

# # Assuming YourModel is the name of your model
# event.listen(Profile.creation_date, 'set', set_code, retval=False)


@event.listens_for(Profile, "before_insert")
def before_insert_listener(mapper, connection, target):
    if current_user.is_authenticated:
        target.created_by = current_user.id


@event.listens_for(Profile, 'after_insert')
def after_insert_listener(mapper, connection, target):
    target.code = f"DMO{datetime.now().year}{target.id}"
    
    # Manually update the code field after insertion
    connection.execute(
        Profile.__table__
        .update()
        .where(Profile.id == target.id)
        .values(code=target.code)
    )