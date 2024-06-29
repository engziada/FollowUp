from datetime import datetime
from genericpath import isfile
from os import listdir, makedirs, path
import random
from flask import current_app, url_for
from icecream import ic
import json
import requests
from werkzeug.utils import secure_filename

from apps.actions.models import Action
from apps.authentication.models import Users
from apps.globals.models import Profile_Actions
from apps.profiles.models import Profile


def get_summerized_report()->dict:
    report = {
        "total_users": Users.query.count(),
        "total_profiles": Profile.query.count(),
        "total_actions": Action.query.count(),
        # "action_profiles": {
        #     profile.id: [
        #         {"action_id": profile_action.action_id, "action_name": profile_action.action.name}
        #         for profile_action in Profile_Actions.query.filter_by(profile_id=profile.id).all()
        #     ]
        #     for profile in Profile.query.all()
        # },
        # "last_action_profiles": {action.name: Profile.query.filter_by(action_id=action.id).count() for action in Action.query.all()}
    }

    return report

# ////////////////////////////////////////////////////////////////////////////////////////

