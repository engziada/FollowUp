from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from apps.actions import blueprint

from apps import db

from apps.actions.forms import ActionForm
from apps.actions.models import Action

from icecream import ic

from apps.home.models import Log



@blueprint.route("/actions")
@login_required
def actions():
    actions = Action.query.all()  # Fetch all contents from the database
    return render_template("actions/actions.html", actions=actions)


@blueprint.route("/action_add", methods=["GET", "POST"])
@login_required
@Log.add_log("إضافة حدث")
def action_add():
    form = ActionForm()  # Create an instance of the form
    if form.validate_on_submit():
        new_action = Action(
            name=form.name.data,
            description=form.description.data,
            steps = form.steps.data,
            due_days = form.due_days.data,
            alert = form.alert.data,
            establishment=form.establishment.data,
        )

        db.session.add(new_action)
        db.session.commit()
        flash("تم إضافة الحدث", "success")

        return redirect(url_for("action_blueprint.actions"))
    return render_template("actions/action_add.html", form=form)


@blueprint.route("/action_delete/<int:action_id>", methods=["POST"])
@login_required
@Log.add_log("حذف حدث")
def action_delete(action_id):
    action = Action.query.get(action_id)
    if not action:
        flash("الحدث غير موجود", "danger")
        return redirect(url_for("action_blueprint.actions"))
    db.session.delete(action)
    db.session.commit()
    flash("تم حذف الحدث", "success")
    return redirect(url_for("action_blueprint.actions"))


@blueprint.route("/action_edit/<int:action_id>", methods=["GET", "POST"])
@login_required
@Log.add_log("تعديل حدث")
def action_edit(action_id):
    action = Action.query.get(action_id)
    if not action:
        flash("الحدث غير موجود", "danger")
        return redirect(url_for("action_blueprint.actions"))
                
    form = ActionForm(obj=action)  # Create an instance of the form
    if form.validate_on_submit():
                action.name = form.name.data
                action.description = form.description.data
                action.steps = form.steps.data
                action.due_days = form.due_days.data
                action.alert = form.alert.data
                action.establishment=form.establishment.data

                db.session.commit()
                flash("تم تعديل الحدث", "success")
                return redirect(url_for("action_blueprint.actions"))
    
    return render_template(
        "actions/action_edit.html", form=form, action=action)
