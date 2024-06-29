from datetime import datetime
from apps import db

from flask import (
    jsonify,
    render_template,
    redirect,
    request,
    session,
    url_for,
    flash,
)
from flask_wtf.file import FileField
from flask_login import login_required

from sqlalchemy import desc
from icecream import ic
from sqlalchemy.exc import IntegrityError

from apps.actions.models import Action
from apps.globals.forms import ProfileActionForm
from apps.globals.models import Profile_Actions
from apps.home.models import Log
from apps.profiles import blueprint
from apps.profiles.forms import ProfileForm
from apps.profiles.models import Profile


@blueprint.route("/profiles")
@login_required
def profiles():
    page = request.args.get("page", 1, type=int)
    per_page = 50  # Number of logs per page

    # Get search term from query string (optional)
    search_terms = request.args.get("q", "")

    # filter influencers
    profiles = (
        Profile.query.filter(Profile.name.ilike(f"%{search_terms}%"))).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("profiles/profiles.html", profiles=profiles, search_terms=search_terms)


@blueprint.route("/profile_add", methods=["GET", "POST"])
@login_required
@Log.add_log("إضافة جهة")
def profile_add():
    form = ProfileForm()  # Create an instance of the form
    if form.validate_on_submit():
        # Check if a profile with the given name already exists
        existing_profile = Profile.query.filter_by(name=form.name.data).first()

        if existing_profile:
            flash("هذه الجهة موجودة بالفعل, تم تحويلك إلى صفحة تعديل الجهة", "danger")
            return redirect(url_for("profiles_blueprint.profile_edit", profile_id=existing_profile.id))
        else:
            try:
                new_profile = Profile(
                    name=form.name.data,
                    about=form.about.data,
                    est_date=form.est_date.data,
                    account_manager=form.account_manager.data,
                    account_manager_email=form.account_manager_email.data,
                    phones=form.phones.data,
                    address=form.address.data,
                )

                db.session.add(new_profile)
                db.session.commit()
                flash("تم إضافة الجهة", "success")
                return redirect(url_for("profiles_blueprint.profiles"))
            except IntegrityError as e:
                ic("IntegrityError in <profile_add>: ", e)
                db.session.rollback()
                flash(f"خطأ أثناء تسجيل البيانات:\n{e}","danger")
            except Exception as e:
                ic("Error in <profile_add>: ", e)
                db.session.rollback()
                flash(f"حدث خطأ أثناء إضافة الجهة\n{e}", "danger")
    return render_template("profiles/profile_add.html", form=form)


@blueprint.route("/profile_delete/<int:profile_id>", methods=["POST"])
@login_required
@Log.add_log("حذف جهة")
def profile_delete(profile_id):
    profile = Profile.query.get(profile_id)
    if not profile:
        flash("الجهة غير موجودة", "danger")
        return redirect(url_for("profiles_blueprint.profiles"))
    db.session.delete(profile)
    db.session.commit()
    flash("تم حذف الجهة", "success")
    return redirect(url_for("profiles_blueprint.profiles"))


@blueprint.route("/profile_edit/<int:profile_id>", methods=["GET", "POST"])
@login_required
@Log.add_log("تعديل جهة")
def profile_edit(profile_id):
    profile = Profile.query.get(profile_id)
    if not profile:
        flash("الجهة غير موجودة", "danger")
        return redirect(url_for("profiles_blueprint.profiles"))

    form = ProfileForm(obj=profile)  # Create an instance of the form
    if form.validate_on_submit():
        profile.name = form.name.data
        profile.about = form.about.data
        profile.est_date = form.est_date.data
        profile.account_manager = form.account_manager.data
        profile.account_manager_email = form.account_manager_email.data
        profile.phones = form.phones.data
        profile.address = form.address.data
        
        db.session.commit()
        flash("تم تعديل الجهة", "success")
        return redirect(url_for("profiles_blueprint.profiles"))

    return render_template(
        "profiles/profile_edit.html",
        form=form,
        profile=profile,
    )


# Modify the profile_actions function
@blueprint.route("/profile_actions/<int:profile_id>", methods=["GET", "POST"])
@login_required
@Log.add_log("تعديل أحداث جهة")
def profile_actions(profile_id):
    form = ProfileActionForm()
    form.action_id.choices = [(action.id, action.name) for action in Action.query.all()]

    profile = Profile.query.get_or_404(profile_id)    
    
    if request.method == "GET":
        profile_actions = (
            db.session.query(Profile_Actions)
            .filter(Profile_Actions.profile_id == profile.id)
            .order_by(Profile_Actions.creation_date)
            .all()
        )
        for i, profile_action in enumerate(profile_actions):
            if i < len(profile_actions) - 1:  # For all but the last action
                next_creation_date = profile_actions[i + 1].creation_date
                ic(profile_action.action)
                ic(next_creation_date)
                difference = (next_creation_date - profile_action.creation_date).days
                ic(difference)
            else:  # For the last action
                now = datetime.now().date()
                difference = (now - profile_action.creation_date).days
            rem_days = profile_action.action.due_days - difference
            ic(rem_days)
            profile_action.rem_days = rem_days

        for profile_action in profile_actions:
            ic(profile_action.creation_date)
            ic(profile_action.rem_days)
        
        #get last profile_action.action.alert if it's rem_days<=0 else 'لا يوجد'
        if profile_actions:
            last_profile_action = profile_actions[-1]
            if last_profile_action.rem_days <= 0:
                profile.alert = last_profile_action.action.alert
            else:
                profile.alert = "لا يوجد"
        return render_template("profiles/profile_actions.html", profile=profile, form=form, profile_actions=profile_actions)
     
    if form.validate_on_submit():
        action = Action.query.get(form.action_id.data)
        if action:
            try:
                new_profile_action = Profile_Actions(
                    profile_id=profile.id,
                    action_id=form.action_id.data,
                    notes=form.notes.data
                )
                db.session.add(new_profile_action)
                db.session.commit()
                flash("تمت إضافة الإجراء بنجاح.", "success")
            except Exception as e:
                ic("Error in <profile_actions>: ", e)
                db.session.rollback()
                flash(f"حدث خطأ أثناء إضافة الإجراء\n{e}", "danger")                
        else:
            flash("لم يتم العثور على الحدث", "danger")
        return redirect(url_for("profiles_blueprint.profile_actions", profile_id=profile_id))

    # return render_template("profiles/profile_actions.html", profile=profile, form=form, profile_actions=profile_actions)


@blueprint.route("/delete_profile_action/<profile_action_id>", methods=["POST"])
@login_required
@Log.add_log("حذف إجراء الملف الشخصي")
def delete_profile_action(profile_action_id):
    profile_action=Profile_Actions.query.get(profile_action_id)
    if not profile_action:
        flash("فشل عملية حذف الحدث", "danger")
        # return redirect(url_for("profiles_blueprint.profile_actions", profile_id=profile_id))
    profile_id=profile_action.profile_id
    db.session.delete(profile_action)
    db.session.commit()
    flash("تم حذف الإقتران", "success")
    return redirect(url_for("profiles_blueprint.profile_actions", profile_id=profile_id))