"""
    Defines the role class:
        Administrator: Has every permission.
"""
from app.db import database as db

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    users = db.relationship("User", secondary="user_has_roles")
    permissions = db.relationship("Permission", secondary="role_has_permissions")

    def allTuples():
        return Role.query.all()

    @classmethod
    def all(cls):
        """ Returns all users """
        return Role.query.all()
    @classmethod
    def find(self, name):
        return Role.query.filter_by(name=name).one()

    @classmethod
    def find_by(cls, **args):
        return Role.query.filter_by(**args).first()

    @classmethod
    def create(cls, name):
        """ Create role in database """
        new_role = Role(name=name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    @classmethod
    def seed(cls, name, permissions):
        """ Used in seed.py to populate database """
        existing_role = Role.find_by(name=name)
        if existing_role:
            return existing_role
        else:
            role = Role.create(name=name)
            for permission in permissions:
                role.permissions.append(permission)
                db.session.commit()
            return role
