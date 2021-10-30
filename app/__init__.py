""" App inicialization """
from os import path, environ
from dotenv import load_dotenv
from flask import Flask, render_template, g,url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, upgrade
from flask_session import Session
from config import config
from app import db
from db.seed import seed
from app.models.user_has_role import UserHasRole
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_has_permission import RoleHasPermission
from app.models.config import Config
from app.models.user import User
from app.models.turn import Turn
from app.models.center import Center
from app.models.center_has_type import CenterHasType
from app.resources import site
from app.helpers import handler
from app.helpers import auth as helper_auth
from app.helpers.auth import soy_admin,have_permissions,is_operator
from flask_cors import CORS
from flask_restful import Resource,Api
from app.resources.api.centros import API_centros, API_centro_id, PDF, API_centros_statistics,API_estadisticas_tipo_centro
from app.resources.api.turns import API_Turns, API_Turns_All, API_Book_a_Turn
from app.resources.auth import init_oauth


def create_app(environment="development"):
    """ Create and migrate app """

    # Loads env
    load_dotenv()

    # Configuración inicial de la app
    app = Flask(__name__)

    init_oauth(app)

    #para poder hacer post con apis
    CORS(app)
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    Bootstrap(app)

    #carga de API
    api = Api(app)
    api.add_resource(API_centro_id, '/centros/<id>')
    api.add_resource(API_centros, '/centros')
    api.add_resource(PDF, '/pdf')
    api.add_resource(API_centros_statistics, '/centros_statistics/<date>')
    api.add_resource(API_estadisticas_tipo_centro,'/api/estadisticas-tipo-centro')
    
    api.add_resource(API_Turns, '/centros/<center_id>/turnos_disponibles')
    api.add_resource(API_Turns_All, '/api/all_turns')
    api.add_resource(API_Book_a_Turn, '/centros/<center_id>/reserva')

    # Carga de los blueprint
    app.register_blueprint(site)

    # ORM CONNECTION
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://'+app.config["DB_USER"]+':'+app.config["DB_PASS"]+'@localhost/'+app.config["DB_NAME"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # PENSAR SI ES NECESARIO

    # Configure db
    db.init_app(app)

    # Migrations
    Migrate(app, db.database)
    if app.config["DB_MIGRATE"]:
        with app.app_context():
            upgrade()

    # Run seeds
    seed()

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(config_saved=(Config.first))
    app.jinja_env.globals.update(admin=(soy_admin))
    app.jinja_env.globals.update(operator=(is_operator))
    #app.jinja_env.globals.update(have_permissions=(have_permissions))


    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(503, handler.disabled_site)
    #app.register_error_handler(500, handler.server_error) comentado pa tiraba error)

    return app
