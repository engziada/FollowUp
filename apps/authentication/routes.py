from flask import flash, render_template, redirect, request, session, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint

from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass,create_default_admin

from apps.home.models import Log
from icecream import ic

@blueprint.route('/')
def route_default():
    # ic(session.get("original_url", url_for("authentication_blueprint.login")))
    original_url=session.pop("original_url", url_for("authentication_blueprint.login")) 
    return redirect(original_url)


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
@Log.add_log("تسجيل دخول")  # Pass the message as an argument
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # Check if admin user exists, if not create it
        create_default_admin(Users=Users,db=db)
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg=' بيانات الحساب خطأ, من فضلك تأكد من إسم المستخدم و كلمة المرور',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
@Log.add_log("إضافة مستخدم")
@login_required
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='إسم المستخدم موجود بالفعل',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='البريد الإلكتروني موجود بالفعل',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template('accounts/register.html',
                               msg='تم إضافة الحساب,  <a href="/login">تسجيل دخول</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
@Log.add_log_early("تسجيل خروج")
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/users', methods=['GET'])
@Log.add_log("عرض جميع المستخدمين")
@login_required
def users():
    users = Users.query.all()  # Assuming User is your user model
    return render_template('accounts/users.html', users=users)


@blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
@Log.add_log("حذف المستخدم")
@login_required
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        flash('المستخدم غير موجود', 'danger')
        return redirect(url_for("authentication_blueprint.users"))
    db.session.delete(user)  # Assuming db is your SQLAlchemy instance
    db.session.commit()
    flash('تم حذف المستخدم', 'success')
    return redirect(url_for("authentication_blueprint.users"))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    session['original_url'] = request.url
    return render_template("home/page-403.html"), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    session['original_url'] = request.url
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
