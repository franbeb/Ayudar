""" This initialize the routing system and it can disable the site based on the configuration """
from flask import Blueprint, render_template
from app.models.config import Config
from app.models.user import User
from app.helpers.auth import public,authenticated
from flask import redirect, session, abort

site = Blueprint("site", __name__)


@site.route("/")
@public
def home():
    if session.get("user"):
        #es re ineficiente pero pareciera ser la unica manera por ahora :)
        user =User.find(int(session.get("user")))
        if  authenticated() and user.have_permissions():
            return render_template("home_logueado.html")
    return render_template("home.html")

from app.resources import user
from app.resources import auth
from app.resources import configuration
from app.resources import center
from app.resources import turn

# Rutas temporales
site.add_url_rule("/usuarios/<id>", "user_edit", user.user_edit, methods=["POST","GET"])
site.add_url_rule("/usuarios-delete/<id>", "user_delete", user.user_delete)
site.add_url_rule("/usuarios-active/<id>", "user_active", user.user_active)
