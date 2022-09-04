from apiflask import Schema
from apiflask.fields import String, List, Integer


class CreateRoleRequest(Schema):
    role_name = String(required=True)
    permissions = List(String(required=True))


class CreateRoleResponse(Schema):
    role_id = Integer(required=True)
    role_name = String(required=True)


class DeleteRoleRequest(Schema):
    role_name = String(required=True)


class DeleteRoleResponse(Schema):
    deleted_role_id = Integer(required=True)


class ChangeRoleRequest(Schema):
    old_role_name = String(required=True)
    new_role_name = String(required=True)
    new_role_permissions = List(String(required=True))
