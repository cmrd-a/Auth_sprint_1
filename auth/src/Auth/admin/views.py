from http import HTTPStatus

from flask import Blueprint, request
from flask import abort
from sqlalchemy.exc import IntegrityError

from Auth.db.models import Role, Permission
from Auth.extensions import db

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.post("/create_role")
def create_role():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST)

    role_name = request.json.get("role")
    role = Role(name=role_name)
    permissions = request.json.get("permissions")
    try:
        for permission in permissions:
            role.permissions.append(db.session().query(Permission).filter(Permission.name == permission).first())
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        return f"Роль {role_name} уже существует.", HTTPStatus.BAD_REQUEST

    return role.id, HTTPStatus.CREATED


@blueprint.delete("/delete_role")
def delete_role():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST)

    role_name = request.json.get("role")

    try:
        role = db.session().query(Role).filter(Role.name == role_name).first()

        if not role:
            return f"Роль {role_name} не найдена.", HTTPStatus.BAD_REQUEST

        role_id = role.id
        db.session.delete(role)
        db.session.commit()
    except IntegrityError:
        return f"Ошибка при удалении роли {role_name}.", HTTPStatus.INTERNAL_SERVER_ERROR

    return role_id, HTTPStatus.OK
