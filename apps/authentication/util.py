import os
import hashlib
import binascii
from icecream import ic

def hash_pass(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


# Create the default admin user (you can modify this data as needed)
def create_default_admin(Users,db):
    try:
        username = "admin"
        password = "admin"
        email = "admin@email.com"
        admin_user = Users.query.filter_by(username=username).first()
        if admin_user is None:
            # If the admin user doesn't exist, create it
            admin_user = Users(username=username, password=password, email=email)
            db.session.add(admin_user)
            db.session.commit()
            ic("Admin user created")
        else:
            ic("Admin user already exists")
    except Exception as e:
        msg=f"Error creating admin user, error:{e}"
        ic(msg)