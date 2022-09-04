from http import HTTPStatus

from apiflask import APIBlueprint
from flask import make_response, jsonify
from sqlalchemy.exc import IntegrityError

from Auth.admin.schemas import (
    CreateRoleRequest,
    CreateRoleResponse,
    DeleteRoleRequest,
    DeleteRoleResponse,
    ChangeRoleRequest,
)
from Auth.db.models import Role, Permission
from Auth.extensions import db

blueprint = APIBlueprint("admin", __name__, url_prefix="/admin")


@blueprint.post("/create_role")
@blueprint.input(CreateRoleRequest)
@blueprint.output(CreateRoleResponse)
def create_role(body):
    role_name = body["role_name"]
    role = Role(name=role_name)
    permissions = body["permissions"]

    try:
        for permission in permissions:
            role.permissions.append(db.session().query(Permission).filter(Permission.name == permission).first())
        db.session.add(role)
        db.session.commit()
    except IntegrityError:
        return make_response(f"Роль {role_name} уже существует.", HTTPStatus.BAD_REQUEST)

    return make_response(jsonify(role_id=role.id, role_name=role_name), HTTPStatus.CREATED)


@blueprint.delete("/delete_role")
@blueprint.input(DeleteRoleRequest)
@blueprint.output(DeleteRoleResponse)
def delete_role(body):
    role_name = body["role_name"]

    try:
        role = db.session().query(Role).filter(Role.name == role_name).first()

        if not role:
            return make_response(f"Роль {role_name} не найдена.", HTTPStatus.BAD_REQUEST)

        deleted_role_id = role.id
        db.session.delete(role)
        db.session.commit()
    except IntegrityError:
        return make_response(f"Ошибка при удалении роли {role_name}.", HTTPStatus.INTERNAL_SERVER_ERROR)

    return make_response(jsonify(deleted_role_id=deleted_role_id), HTTPStatus.OK)


@blueprint.post("/change_role")
@blueprint.input(ChangeRoleRequest)
def change_role(body):
    old_role_name = body["old_role_name"]
    new_role_name = body["new_role_name"]
    new_role_permissions = body["new_role_permissions"]

    try:
        old_role = db.session().query(Role).filter(Role.name == old_role_name).first()
        if not old_role:
            return make_response(f"Роль {old_role_name} не найдена.", HTTPStatus.BAD_REQUEST)

        old_role_id = old_role.id
        db.session.delete(old_role)
        changed_role = Role(name=new_role_name, id=old_role_id)

        for permission in new_role_permissions:
            changed_role.permissions.append(db.session().query(Permission).filter(Permission.name == permission).first())
        db.session.add(changed_role)
        db.session.commit()
    except IntegrityError:
        return make_response(f"Ошибка при изменении роли {old_role_name}.", HTTPStatus.INTERNAL_SERVER_ERROR)

    return make_response(HTTPStatus.OK)
