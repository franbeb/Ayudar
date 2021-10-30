from flask import redirect, session, abort
from app.models.user import User
from app.models.config import Config
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_has_role import UserHasRole
from app.models.role_has_permission import RoleHasPermission
from functools import wraps


def authenticated(session=session):
    return session.get("user")


def soy_admin():
    if session.get("user"):
        return User.find(id=session.get("user")).is_admin()
    else: 
        return False

def have_permissions():
    if session.get("user"):
        return User.find(id=session.get("user")).have_permissions()
    else:
        return False

def is_operator():
    if session.get("user"):
        return User.find(id=session.get("user")).is_operator()
    else:
        return False


def logged_in(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user = authenticated(session)
        if not user:
            result = abort(401)
        else:
            result = function(*args, **kwargs)
        return result
    return wrapper


def public(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        config = Config.first()
        cond=False
        if 'user'in session:
            cond=User.find(int(session.get("user"))).have_permissions()
        if config.habilitado or (cond):
            result = function(*args, **kwargs)
        else:
            result = abort(503)
        return result
    return wrapper


def user_has(permission):
    """decorador para checkear permisos"""
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            has = False
            # busca usuario
            user =_logged_in()   # usar autenticacion
            # busca los roles que tiene
            user_roles = UserHasRole.query.filter_by(user_id=user)
            # buscar todos los permisos que tiene hasta encontrar uno que se llame com el parametro
            for rol in user_roles:
                role_permissions = RoleHasPermission.query.filter_by(role_id=rol.role_id)
                permission_obj = Permission.query.filter_by(name=permission).first()
                for role_per in role_permissions:
                    if role_per.permission_id == permission_obj.id:
                        has = True
                        break
                if has:
                    break
            if has:
                result = function(*args, **kwargs)
            else:
                result = abort(401)
            return result
        return wrapper
    return decorator


def _logged_in():
    user = authenticated(session)
    if not user:
        abort(401)
    else:
        return user
# hacer decorator de pagina esta online y si tiene sesion iniciada
# page_online
