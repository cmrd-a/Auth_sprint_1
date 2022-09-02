from apiflask import Schema
from apiflask.fields import String, Email, DateTime, IP
from apiflask.validators import Length

password_validator = Length(8, 128)


class AccessToken(Schema):
    access_token = String()


class EmailPasswordIn(Schema):
    email = Email(required=True)
    password = String(required=True, validate=password_validator)


class LoginOut(AccessToken):
    refresh_token = String()
    user_role = String()
    access_expires = String()


class ChangePasswordIn(Schema):
    current_password = String(required=True, validate=password_validator)
    new_password = String(required=True, validate=password_validator)


class LoginHistoryOut(Schema):
    ip_address = IP()
    login_time = DateTime()
