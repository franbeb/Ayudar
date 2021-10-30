""" Authorization controller """
from flask import redirect, render_template, request, url_for, session, flash
from app.models.user import User
from app.models.config import Config
from app.models.role import Role
from app.resources import site
from app.helpers.auth import authenticated
from authlib.integrations.flask_client import OAuth

oauth = OAuth()
def init_oauth(app):
    # OAUTH
    app.secret_key='random'
    oauth.init_app(app)
    google = oauth.register(
        name='google',
        client_id='143621212298-hsqr4pcg7g8rv56ttig8pi9ngvsmibd2.apps.googleusercontent.com',
        client_secret='2JPDB_KH5vYlsnTte8jkwUqp',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid profile email'}
    )


@site.route('/login-oauth')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('site.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@site.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    userInfo = resp.json()
    user = User.find_by(email= userInfo["email"])
    config = Config()

    if not user:
        flash("El usuario no existe","warning")
        return redirect(url_for("site.auth_login"))
    # esto tiene que descomentarse cuando el modelo de usuario tenga active
    elif not user.active:
        flash("Usuario esta bloqueado","warning")
        return redirect(url_for("site.auth_login"))
    elif not config.habilitado and not user.is_admin():
        flash("Sitio esta deshabilitado","warning")
        return redirect(url_for("site.auth_login"))

    session["user"] = user.id
    session["user_email"] = user.email
    flash("La sesión se inició correctamente.","success")

    return redirect('/')


@site.route("/iniciar_sesion")
def auth_login():
    """ Login form """
    if not authenticated():
        return render_template("auth/login.html")
    else:
        return render_template("auth/logout.html")

@site.route("/autenticacion", methods=["POST"])
def auth_authenticate():
    """ Authenticates """
    params = request.form
    user = User.find_by_email_and_pass( params["email"], params["password"])
    config = Config.first()

    if not user:
        flash("Usuario o clave incorrecto.","warning")
        return redirect(url_for("site.auth_login"))
    # esto tiene que descomentarse cuando el modelo de usuario tenga active
    elif not user.active:
        flash("Usuario esta bloqueado","warning")
        return redirect(url_for("site.auth_login"))
    elif not config.habilitado and not user.is_admin():
        flash("Sitio esta deshabilitado","warning")
        return redirect(url_for("site.auth_login"))

    session["user"] = user.id
    session["user_email"] = user.email
    flash("La sesión se inició correctamente.","success")
    return redirect("/")

@site.route("/cerrar_sesion")
def auth_logout():
    """ Logouts """
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.","success")

    return redirect(url_for("site.auth_login"))
