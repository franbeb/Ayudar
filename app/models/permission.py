"""
    Define permissions.
    All the permissions are visible in "db/seed.py"
"""
from app.db import database as db

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    permissions = db.relationship("Permission", secondary="role_has_permissions")

    @classmethod
    def find_by(cls, **args):
        return Permission.query.filter_by(**args).first()

    @classmethod
    def create(cls, name):
        """ Create permission in database """
        new_permission = Permission(name=name)
        db.session.add(new_permission)
        db.session.commit()
        return new_permission

    @classmethod
    def seed(cls, name):
        """ Used in seed.py to populate database """
        existing_permission = Permission.find_by(name=name)
        if existing_permission:
            return existing_permission
        else:
            return Permission.create(name=name)
