import click

from Auth.db.models import Permission, Role, User
from Auth.extensions import db


@click.command()
@click.argument("email")
@click.argument("password")
def create_super_user(email, password):
    base_permissions = ["comment", "manage_users", "watch_new_movies"]
    base_roles = {"registered": ["comment"], "super_user": base_permissions}
    for role_name, permissions in base_roles.items():
        permissions_objects = []
        for permission_name in base_permissions:
            permission = Permission.query.filter_by(name=permission_name).first()
            if not permission:
                permission = Permission(name=permission_name)
                db.session.add(permission)
                db.session.commit()
                permissions_objects.append(permission)
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, permissions=permissions_objects)
            db.session.add(role)
            db.session.commit()

    user = User.query.filter_by(email="email").first()
    if not user:
        super_role = Role.query.filter_by(name="super_user").first()
        user = User(email=email, password=password, role=super_role)
        db.session.add(user)
        db.session.commit()
