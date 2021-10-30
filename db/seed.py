"""
    Este archivo es la continuacion a 'seed.sql'.
    La idea es la misma que con las migraciones, este archivo se correrá con cada ejecucion del programa.
    A diferencia de seed.sql este script es resistente a la existencia previa de una fila en particular.
    TODO: Se podria agregar algun numero de versionado para no ejecutar todas las instrucciones siempre.
"""

from datetime import date, datetime, timedelta
from app.models.config import Config
from app.models.permission import Permission
from app.models.turn import Turn
from app.models.role import Role
from app.models.user import User
from app.models.center import Center
from app.models.tipo_centro import Tipo_Centro

def seed():
    
    """ Configuration """
    print("Seeding Configuration...")
    configuration = Config.seed(
        title = 'AYUDAR',
        description = 'Una forma de brindar bienes a los que mas lo necesitan',
        mail = 'ayudar@argentina.ar',
        cant_elem = 3,
        habilitado = True
    )

    """ Permissions """
    print("Seeding Permissions...")
    # Center
    permission_center_index = Permission.seed(name = 'center_index')
    permission_center_new = Permission.seed(name = 'center_new')
    permission_center_show = Permission.seed(name = 'center_show')
    permission_center_update = Permission.seed(name = 'center_update')
    permission_center_destroy = Permission.seed(name = 'center_destroy')
    permission_center_approve = Permission.seed(name = 'center_approve')
    # Role
    permission_role_new = Permission.seed(name = 'role_new')
    permission_role_index = Permission.seed(name = 'role_index')
    permission_role_destroy = Permission.seed(name = 'role_destroy')
    permission_role_show = Permission.seed(name = 'role_show')
    permission_role_update = Permission.seed(name = 'role_update')
    # Configuration
    permission_configuration_show = Permission.seed(name = 'configuration_show')
    permission_configuration_update = Permission.seed(name = 'configuration_update')
    # User
    permission_user_index = Permission.seed(name = 'user_index')
    permission_user_new = Permission.seed(name = 'user_new')
    permission_user_show = Permission.seed(name = 'user_show')
    permission_user_update = Permission.seed(name = 'user_update')
    permission_user_destroy = Permission.seed(name = 'user_destroy')
    permission_user_delete = Permission.seed(name = 'user_delete')
    # Turn
    permission_turn_index = Permission.seed(name = 'turn_index')
    permission_turn_new = Permission.seed(name = 'turn_new')
    permission_turn_show = Permission.seed(name = 'turn_show')
    permission_turn_update = Permission.seed(name = 'turn_update')
    permission_turn_destroy = Permission.seed(name = 'turn_destroy')


    """ Roles """
    print("Seeding Roles...")
    role_admin = Role.seed('admin', permissions=[
        permission_role_show,
        permission_role_update,
        permission_role_new,
        permission_role_index,
        permission_role_destroy,
        permission_configuration_show,
        permission_configuration_update,
        permission_user_index,
        permission_user_new,
        permission_user_destroy,
        permission_user_update,
        permission_center_approve,
        permission_user_show,
        permission_user_delete,
        permission_center_index,
        permission_center_new,
        permission_center_update,
        permission_center_show,
        permission_center_destroy,
        permission_turn_index,
        permission_turn_new,
        permission_turn_show,
        permission_turn_update,
        permission_turn_destroy
    ])
    role_operator = Role.seed('operator', permissions=[
        permission_user_show,
        permission_center_index,
        permission_center_new,
        permission_center_show,
        permission_center_update,
        permission_center_approve,
        permission_turn_index,
        permission_turn_new,
        permission_turn_show,
        permission_turn_update,
        permission_turn_destroy
    ])
    role_user = Role.seed('user', permissions=[
        # Tristeza nao tem fim
        permission_user_show,
    ])

    """ Users """
    print("Seeding Users...")
    user = User.seed(
        first_name = "Ada",
        last_name = "Lovelace",
        password = "admin123",
        email = "admin@admin.com",
        username="ada_admin",
        perfil = "adita",
        roles = [role_admin]
    )
    operator = User.seed(
        first_name = "Operador",
        last_name = "Valentin",
        password = "operator123",
        email = "operator@operator.com",
        username="operator",
        perfil = "operator",
        roles = [role_operator]
    )
    """ Types centers """
    print("Seeding Types Centers...")
    tipo_centro_1 = Tipo_Centro.seed(nombre='Alimentos')
    tipo_centro_2 = Tipo_Centro.seed(nombre='Plasma')
    tipo_centro_3 = Tipo_Centro.seed(nombre='Ropa')

    """ Centers """
    print("Seeding  Centers...")
    centro_1= Center.seed( nombre='Centro bolivar',
                direccion='Complejo Venezueela',
                telefono='221123',
                hora_apertura='8:00',
                hora_cierre='10:00',
                web='centro-bolivar.gob.ar',
                estado=None,
                protocolo_vista='',
                longitud=-57.97004699707032,
                latitud=-34.91437014491459,
                email='centro-bolivar@gob.com',types=[tipo_centro_1,tipo_centro_2,tipo_centro_3],
                municipio=17)
    centro_2= Center.seed( nombre='Centro Recoleta',
                direccion='CCR',
                telefono='1133',
                hora_apertura='9:00',
                hora_cierre='12:00',
                web='centro-recoleta.gob.ar',
                estado=True,
                protocolo_vista='',
                longitud=-34.58638889,
                latitud=-58.39222222,
                email='centro-recoleta@gob.com',types=[tipo_centro_2,tipo_centro_3],
                municipio=1)

    """ Turns """
    turn_1 = Turn.seed(email = "test@gmail.com", starting_time = "9:30", date = date.today() + timedelta(days=1), center = centro_1)
    turn_2 = Turn.seed(email = "test@gmail.com", starting_time = "10:30", date = date.today() + timedelta(days=1), center = centro_1 )
    turn_3 = Turn.seed(email = "test@gmail.com", starting_time = "11:30", date = date.today(), center = centro_1 )
    turn_4 = Turn.seed(email = "test@gmail.com", starting_time = "12:30", date = date.today(), center = centro_1 )

    print("Seed finished.")
