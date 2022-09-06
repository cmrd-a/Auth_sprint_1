from http import HTTPStatus

from apiflask import APIBlueprint, abort
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from Auth.db.models import Role, User, LoginHistory
from Auth.extensions import db, redis_client
from Auth.user.schemas import LoginOut, EmailPasswordIn, ChangePasswordIn, AccessToken, LoginHistoryOut, LoginHistoryIn

blueprint = APIBlueprint("user", __name__, url_prefix="/auth/users")


@blueprint.post("/v1/register")
@blueprint.input(EmailPasswordIn)
@blueprint.output({})
def register(body):
    email = body["email"]
    password = body["password"]
    if User.query.filter_by(email=email).first():
        return abort(HTTPStatus.BAD_REQUEST, message="Bad username or password")
    role = Role.query.filter_by(name="registered").first()
    new_user = User(email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()


@blueprint.post("/v1/login")
@blueprint.input(EmailPasswordIn)
@blueprint.output(LoginOut)
def login(body):
    email = body["email"]
    password = body["password"]
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        db.session.add(LoginHistory(user=user, ip_address=request.remote_addr))
        db.session.commit()
        access_token = create_access_token(
            identity=email, fresh=True, additional_claims={"permissions": [p.name for p in user.role.permissions]}
        )
        refresh_token = create_refresh_token(identity=email)
        return jsonify(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires=str(current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]),
            user_role=user.role.name,
        )

    return abort(HTTPStatus.UNAUTHORIZED, message="Bad username or password")


@blueprint.post("/v1/refresh")
@jwt_required(refresh=True)
@blueprint.output(AccessToken)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@blueprint.delete("/v1/logout")
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    redis_client.set(jti, "", ex=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])

    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@blueprint.post("/v1/change-password")
@jwt_required(fresh=True)
@blueprint.input(ChangePasswordIn)
@blueprint.output({})
def change_password(body):
    current_password = body["current_password"]
    new_password = body["new_password"]
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if user and user.password == current_password:
        user.password = new_password
        db.session.commit()
        return
    return abort(HTTPStatus.BAD_REQUEST)


@blueprint.get("/v1/login-history")
@jwt_required()
@blueprint.input(LoginHistoryIn, location="query")
@blueprint.output(LoginHistoryOut(many=True))
def login_history(query):
    email = get_jwt_identity()
    result = (
        LoginHistory.query.filter_by(user=User.query.filter_by(email=email).first())
        .paginate(query["page_number"], query["page_size"], False)
        .items
    )
    return jsonify([{"ip_address": str(r.ip_address), "login_time": str(r.login_time)} for r in result])
