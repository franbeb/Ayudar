""" Users """
from sqlalchemy.orm.exc import NoResultFound
from app.db import database as db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, flash
from app.models.role import Role
from app.models.role import Role
from app.models.user_has_role import UserHasRole

import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True) ##mepa q unique y autoincrement no va
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False, index=True)
    last_name = db.Column(db.String(30), nullable=False, index=True)
    username = db.Column(db.String(30),unique=True, nullable=False)
    active = db.Column(db.Boolean , default=True)
    perfil = db.Column(db.String(40), index=True)
    date_created = db.Column(db.DateTime(timezone=True),default=db.func.current_timestamp())
    roles = db.relationship("Role", secondary="user_has_roles")

    def __repr__(self): ## CHECAR NO SE Q ES
        """ String representation of user """
        return "<email %r>" % self.email

    def __init__(self,password,  email, first_name, last_name, perfil, username):
        """ User initialization """
        self.email = email
        self.password = password
        self.first_name =  first_name
        self.last_name =  last_name
        self.username = username
        self.perfil = perfil
        self.active = True
        #self date_created = DateTime().now()

    def is_admin(self):
        return Role.find(name="admin") in list(self.roles)
    def is_operator(self):
        return Role.find(name="operator") in list(self.roles)

    def have_permissions(self):
        return self.is_admin() or self.is_operator()

    @classmethod
    def all(cls):
        """ Returns all users """
        return User.query.all()

    @classmethod
    def allByDate(self):
        return User.query.order_by(desc(User.date_created)).all()

    @classmethod
    def validate_username(self, key, username):
        return User.query.filter(User.username ==  username).first()

    @classmethod
    def validate_email(self,key,email):
        return User.query.filter(User.email ==  email).first()

    @classmethod
    def set_password(self, password):
        self.password = generate_password_hash(password)

    @classmethod
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email_and_pass(self, email, password):
        """ Finds a user by email and pass """

        # PARA HACER: METER LA CONTRASENIA HASHEADA
        #passwordHasheada = self.check_password(password)
        try:
            return User.query.filter_by(email=email,password=password).first()
        except NoResultFound:
            return None

    @classmethod
    def find(self, id):
        return User.query.filter_by(id=id).one()

    @classmethod
    def find_by(cls, **args):
        return User.query.filter_by(**args).first()

    @classmethod
    def findByUsername(self, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def findActives(self, id):
        return User.query.filter_by(active= '1').all()

    @classmethod
    def findInactives(self):
        return User.query.filter_by(active= '0').all()

    @classmethod
    def create(cls, form):

        username = form.username.data
        perfil = form.perfil.data
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User(password=password, email=email, first_name=first_name, last_name=last_name, perfil=perfil,username=username)
        # PARA HACER: METER HASH PASSWORD
        # user.set_password(form.password.data)
        db.session.add(user)
        for role_id in form.roles.data:
            role = Role.query.filter_by(id=role_id).first()
            user.roles.append(role)
        db.session.commit()



    @classmethod
    def seed(cls, first_name, last_name, password, email, username, perfil, roles):
        """ Used in seed.py to populate database """
        # TODO: El create recibe parametros sanatizados del controller?
        existing_user = User.find_by(email=email)
        if existing_user:
            return existing_user
        else:
            user = User(
                first_name = first_name,
                last_name = last_name,
                password = password,
                email = email,
                username =username,
                perfil = perfil
            )
            db.session.add(user)
            db.session.commit()
            for role in roles:
                user.roles.append(role)
                db.session.commit()
            return user


    @classmethod
    def update(cls,form):
        user = User.query.filter_by(id=form.id.data).first()

        user.username = form.username.data
        user.perfil = form.perfil.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        # ACTUALIZAR ROLES DE USUARIO:
        roles = [int(rol.id)for rol in  Role.all()]
        roles_user = [int(rol.id)for rol in  UserHasRole.from_user(form.id.data) ]

        new_roles_for_user = [rol for rol in roles if rol in form.roles.data and rol not in roles_user]
        for role_id in new_roles_for_user:
            role = Role.query.filter_by(id=role_id).first()
            user.roles.append(role)
        remove_roles_for_user = [rol for rol in roles if rol not in form.roles.data and rol in roles_user]
        for role_id in remove_roles_for_user:
            role = Role.query.filter_by(id=role_id).first()
            user.roles.remove(role)

        db.session.commit()

    @classmethod
    def delete(cls,id): # BAJA LOGICA
        user = User.query.filter_by(id=id).first()
        user.email='null'
        db.session.commit()

    @classmethod
    def remove(cls,id): # BAJA FISICA, el q estamos usando
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()


    @classmethod
    def updateActive(cls,id):
        user = User.query.filter_by(id=id).first()
        change = not user.active
        user.active = change
        #User.query.find_by_id(id).update(active = not active)
        db.session.commit()

    @classmethod
    def change_password(cls,id,old_pass,new_pass):
        ok=True
        user = User.query.filter_by(id=id).first()
        if user.password == str(old_pass):
            user.password = str(new_pass)
            db.session.commit()
        else:
            ok=False

        return ok

