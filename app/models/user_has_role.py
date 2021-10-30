""" Defines the relationship between roles and users """
from app.db import database as db
from app.models.role import Role
from sqlalchemy import or_, and_


class UserHasRole(db.Model):
    __tablename__ = "user_has_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    user = db.relationship("User", backref=db.backref("users", cascade="all, delete-orphan"))
    role = db.relationship("Role", backref=db.backref("roles", cascade="all, delete-orphan"))


    def tieneRolAdmin(idUser):
        for instance in UserHasRole.query.filter_by(user_id=idUser):
            if instance.role_id == 1:
                return True
        return False

    def from_user(idUser):
        roles=[]
        for user in UserHasRole.query.filter_by(user_id=idUser):
            role = Role.query.filter_by(id=user.role_id).first()
            roles.append(role)
        return roles

