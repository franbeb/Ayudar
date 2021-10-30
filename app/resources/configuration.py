from flask import redirect, render_template, request, url_for,flash
from app.resources import site
from app.models.config import Config
from app.helpers.auth import user_has

@site.route("/configuration", methods=['GET'])
@user_has("configuration_show")
def show():
    """ Muestra la configuracion actual de la pagina """
    config = Config().first()

    return render_template("configuration.html", config=config)


@site.route("/configuration", methods=['POST'])
@user_has("configuration_update")
def update():
    """ Permite la actualizacion de ciertas caracteristicas de la pagina """
    # PARA HACER: ACTUALIZAR LA CONFIGURACION CON VALIDACIONES
    config = Config.first()
    dictionary = dict(request.form)
    if "habilitar_sitio" in dictionary:
        dictionary['habilitar_sitio'] = True
    else:
        dictionary['habilitar_sitio'] = False

    config.update(dictionary)
    flash("Configuracion exitosa","success")
    return render_template("configuration.html",  config=config)

