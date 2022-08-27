import uuid
from typing import Optional, Type, TypeVar

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import IPAddressType
from sqlalchemy_utils import PasswordType, force_auto_coercion

from Auth.extensions import db

T = TypeVar("T", bound="PkModel")
force_auto_coercion()
Base = db.declarative_base()


class PkModel(Base):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @classmethod
    def get_by_id(cls: Type[T], record_id: UUID) -> Optional[T]:
        return cls.query.get(record_id)


class CreatedUpdatedModel(PkModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


roles_permissions = db.Table(
    "roles_permissions",
    Base.metadata,
    db.Column("permission_id", db.ForeignKey("permissions.id"), primary_key=True),
    db.Column("role_id", db.ForeignKey("roles.id"), primary_key=True),
)


class Permission(CreatedUpdatedModel):
    __tablename__ = "permissions"

    name = db.Column(db.String(128), unique=True, index=True, nullable=False)


class Role(CreatedUpdatedModel):
    __tablename__ = "roles"

    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    permissions = db.relationship("Permission", secondary=roles_permissions, backref="roles")


class User(CreatedUpdatedModel):
    __tablename__ = "users"

    email = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password = db.Column(
        PasswordType(schemes=["pbkdf2_sha512"]),
        nullable=False,
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role_id = db.Column(UUID, db.ForeignKey("roles.id"), nullable=False)

    role = db.relationship("Role")


class Devices(CreatedUpdatedModel):
    __tablename__ = "devices"

    name = db.Column(db.String(64), index=True, nullable=False)
    fingerprint = db.Column(db.String(256))
    user_id = db.Column(UUID, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("Users")


class LoginHistory(CreatedUpdatedModel):
    __tablename__ = "login_history"

    user_id = db.Column(UUID, db.ForeignKey("users.id"), nullable=False)
    device_id = db.Column(UUID, db.ForeignKey("devices.id"))
    ip_address = db.Column(IPAddressType)

    user = db.relationship("Users")
    device = db.relationship("Devices")
