# 1 -> traerme lo de la bd
# 2 -> ponerlo en un arreglo de turnos
# 3 -> devolverlo en json

# 4 -> reservar turno, guatdar en bd


# serialize sqlalchemy result to json
# -> OPCION NERD https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
# -> https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
# -> videito (usa marshmallow) https://www.youtube.com/watch?v=kRNXKzfYrPU

from flask import request, abort, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.orm.exc import NoResultFound
from app.models.turn import Turn
from app.models.center import Center
from app.helpers.validateTurns import CreateTurnFormForAPI
import werkzeug
from datetime import datetime, date
from email_validator import validate_email, EmailNotValidError

get_parser = reqparse.RequestParser()
get_parser.add_argument('fecha', required=False, help="Para las fechas enviarlas con el formato = DD/MM/AAAA")


post_parser = reqparse.RequestParser()
post_parser.add_argument('email', required=True)
post_parser.add_argument('fecha', required=True)
post_parser.add_argument('starting_time', required=True)
post_parser.add_argument('tel_donante', required=True)
post_parser.add_argument('name', required=True)
post_parser.add_argument('surname', required=True)

errors=[]


class API_Turns(Resource):
    def get(self,center_id):
        """ Returns a list of the available turns for a given center """
        center = Center.query.filter_by(id=center_id).first()
        fecha = get_parser.parse_args()['fecha']
        if fecha:
            fecha_str=fecha
        else:
            fecha_str = datetime.now().strftime("%d/%m/%Y")
        try:
            turns = Turn.free_hours_api(center_id, fecha_str)
            response = {
                "turnos": turns_a_list(turns,center_id,fecha_str),
            }
            return response
        except InternalServerError as e:
            return jsonify({"Status Code" : str(e)})

class API_Turns_All(Resource):
    def get(self):
        """ Returns a list of all the reserved turns"""
        turn_hash = Turn.group_by_date_and_hour()

        response = [[{ "weekday": day, "hour": hour, "reserved": reserved} for hour, reserved in hours.items()] for (day, hours) in turn_hash.items()]
        flatten_response = []
        for sublist in response:
            flatten_response = [ *flatten_response, *sublist ]
        return flatten_response

class API_Book_a_Turn(Resource):
    def post(self, center_id):
        """ Validates a turn and creates it """
        global errors
        errors = []
        if not odd_params():
            return jsonify(list_errors())
        email = post_parser.parse_args()['email']
        fecha = post_parser.parse_args()['fecha']
        name = post_parser.parse_args()['name']
        surname = post_parser.parse_args()['surname']
        starting_time = post_parser.parse_args()['starting_time']
        tel = post_parser.parse_args()['tel_donante']
        form = CreateTurnFormForAPI(csrf_enabled=False, center_id=center_id, email= email, date=fecha, starting_time= starting_time,name=name,surname=surname)
        if form.validate():
            center= Center.find(center_id)
            try:
                turn = Turn.create(email, starting_time, datetime.strptime(fecha, '%d/%m/%Y'), center, tel,name,surname)
                return turn_a_dic(turn), 201
            except InternalServerError as e:
                return jsonify({"Status Code" : str(e)})
        return jsonify({
            "Status Code": "404 Bad Request",
            "Error": "El turno esta en uso o por fuera del rango horario",
            })

        


def turn_a_dic(turn):
    turn = {
        "centro_id": turn.center_id,
        "email_donante": turn.email,
        "name": turn.name,
        "surname": turn.surname,
        "telefono_donante": turn.tel,
        "hora_inicio": turn.starting_time,
        "hora_fin": turn.ending_time(),
        "fecha": turn.date.strftime("%d/%m/%Y"),
        "name": turn.name,
        "surname":turn.surname,
        }
    return turn
def free_turn_a_dic(turn,center_id,fecha,name,surname):
    d={}
    d["center_id"]= center_id
    d["starting_time"]= turn
    d["ending_time"]= ending_time(turn)
    d["name"]= name
    d["surname"] = surname
    d["date"]= fecha
    return d
def turns_a_list(hours,center_id,fecha,name,surname):
    list = []
    for turn in hours:
        list.append(free_turn_a_dic(turn,center_id,fecha,name, surname))
    return list
def ending_time(starting_time):
    hour, minute = starting_time.split(":")
    if minute == "30":
        hour = str(int(hour)+1)
        minute = "00"
    else:
        minute= "30"
    return (":").join([hour, minute])

def list_errors():
    lista=[]
    lista.append({"Status Code" : "404 Bad Request"})
    for error in errors:
        e = {
            "msg" : error
        }
        lista.append(e)
    return lista
def odd_date():
    fecha = post_parser.parse_args()['fecha'].split("/")
    if len(fecha) < 3 :
        errors.append("La fecha ingresada está incompleta o no corresponde con el formato requerido: DD/MM/AAAA")
        return False
    elif not 0<len(fecha[0])<=2 or not len(fecha[1]) == 2 or not len(fecha[2]) == 4:
        errors.append("La fecha ingresada no corresponde con el formato requerido: DD/MM/AAAA")
        return False
    return True
def odd_starting_time():
    hora= post_parser.parse_args()['starting_time'].split(":")
    if len(hora) < 2:
        errors.append("La hora ingresada está incompleta o no corresponde con el formato requerido: HH:MM ")
        return False

    elif  not 0<len(hora[0])<=2 or not len(hora[1]) == 2:
        errors.append("La hora ingresada no corresponde con el formato requerido: HH:MM")
        return False
    return True
def odd_email():
    try:
        valid = validate_email(post_parser.parse_args()['email'])
        email = valid.email
    except EmailNotValidError as e:
        errors.append(str(e))
        return False
    return True
def odd_tel():
    tel = post_parser.parse_args()['tel_donante'].split("-")
    if len(tel) < 2 :
        errors.append("El telefono ingresado está incompleto o no corresponde con el formato requerido (Código_De_Área - Num): '221-677350' ")
        return False
    return True
def odd_params():
    if odd_date() and odd_email() and odd_starting_time() and odd_tel():
        return True
    return False
