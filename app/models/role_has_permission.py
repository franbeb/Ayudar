""" Defines the relationship between Roles and Permissions """
from app.db import database as db

class RoleHasPermission(db.Model):
    __tablename__ = "role_has_permissions"

    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    permission = db.relationship("Permission", backref=db.backref("permission", cascade="all, delete-orphan"))
    role = db.relationship("Role", backref=db.backref("role", cascade="all, delete-orphan"))

    ##relacion = db.relationship("NombreDeLaRelacionUNO", backref=db.backref("nombredelarelacion_MUCHOS",cascade="all, delete-orphan"))
