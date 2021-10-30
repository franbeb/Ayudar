from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs), 401


def disabled_site(e):
    kwargs = {
        "error_name": "503 Service Unavailable Error",
        "error_description": "El sitio esta temporalmente deshabilitado.",
    }
    return render_template("error.html",**kwargs), 503

def server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_descripcion": "Something went wrong",
    }
    return render_template("error.html",**kwargs), 500