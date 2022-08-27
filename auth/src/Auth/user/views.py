from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from Auth.config import JWT_ACCESS_TOKEN_EXPIRES
from Auth.extensions import redis_client, jwt

blueprint = Blueprint("user", __name__, url_prefix="/users")


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


@blueprint.post("/register")
def register():
    pass


@blueprint.post("/login")
def login():
    username = request.json.get("email")
    password = request.json.get("password")
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token, access_expires=str(JWT_ACCESS_TOKEN_EXPIRES))


@blueprint.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@blueprint.delete("/logout")
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    redis_client.set(jti, "", ex=JWT_ACCESS_TOKEN_EXPIRES)

    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@blueprint.post("/change-password")
@jwt_required(fresh=True)
def change_password():
    pass


@blueprint.get("/login-history")
@jwt_required()
def login_history():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
