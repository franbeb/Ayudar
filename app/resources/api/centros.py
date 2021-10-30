from flask import abort,request
from flask_restful import Resource,reqparse
from app.models.config import Config
from app.models.center import Center
from app.models.turn import Turn
from app.models.tipo_centro import Tipo_Centro
from sqlalchemy.orm.exc import NoResultFound
from app.helpers.validateCenters import CreateCenterForm
import werkzeug
import os
from werkzeug.utils import secure_filename
import datetime

parser = reqparse.RequestParser()
parser.add_argument('page', required=False,type=int,help="La pagina debe ser un numero mayor a 0")

post_parser = reqparse.RequestParser()
post_parser.add_argument('tipo_centro', required=True, action='append')
post_parser.add_argument('file', type=werkzeug.datastructures.FileStorage)


class API_centros(Resource):
    def get(self):
        pag = parser.parse_args()["page"]
        if not pag or pag<1:
            pag= 1
        cant_config = Config.first().cant_elem
        centros= Center.all_activos_paginado(pag,cant_config)
        respuesta = {
            "centros": centros_a_lis(centros.items) ,
            "pagina" : pag,
            "total" :  (centros.pages) ,
        }
        return respuesta

    def post(self):
        form = CreateCenterForm(csrf_enabled=False)
        tipos = post_parser.parse_args()["tipo_centro"]
        if form.validate():
            center=Center.create(form,tipos_centros=tipos)

            if 'file' in request.files:
                file = request.files['file']
                if file :
                    filename = secure_filename(file.filename)
                    url_center= 'centro-pdf-'+str(center.id)+'-0.pdf'
                    file.save(os.path.join('app/static/uploads/'+url_center))
                    center.addFileName(url_center)
            return centro_a_dic(center)
        return form.errors
import time

class PDF(Resource):
     def post(self):
        time.sleep(4)
        nom= request["nombre"]
        center=Center.find_by(protocolo_vista=nombre)
        url_center= 'centro-pdf-'+str(center.id)+'-0.pdf'
        center.addFileName(url_center)
        file= request.files["protocolo_vista"]
        # url_center= 'centro-pdf-'+str(center.id)+'-0.pdf'
        file.save(os.path.join('app/static/uploads/'+url_center))
        # center.addFileName(url_center)

def centros_a_lis(centros):
    list= []
    for cen in centros:
        list.append(centro_a_dic(cen))
    return list

def lis_tipo(tipos):
    l=[]
    for tipo in tipos:
        l.append(tipo.nombre)
    return l

def centro_a_dic(centro):
    d={}
    d["nombre"]= centro.nombre
    d["id"]= centro.id
    d["direccions"]= centro.direccion
    d["telefono"]= centro.telefono
    d["hora_apertura"]= str(centro.hora_apertura)
    d["hora_cierre"]= str(centro.hora_cierre)
    d["tipo"]= lis_tipo(centro.tipo_centro)
    d["web"]= centro.web
    d["email"]= centro.email
    d["latlng"]= [centro.latitud , centro.longitud]

    return d


class API_centro_id(Resource):
    def get(self,id):
        try:
            centro = Center.find(id)
            if not centro.estado:
                return abort(404)
        except NoResultFound:
            return abort(404)

        return {"atributos":centro_a_dic(centro)}

class API_centros_statistics(Resource):
    def get(self, date):
        try:
            day = date.split('-')
            centros = Center.all_activos()
            if not centros:
                return abort(404)
        except NoResultFound:
            return abort(404)

        return {"centros" : turnos_centros_a_lis(centros,datetime.datetime(int(day[0]),int(day[1]),int(day[2]))) }


def turnos_centros_a_lis(centros, date):
    list= []
    for cen in centros:
        list.append(turnos_centro_a_dic(cen,date))
    return list

def turnos_centro_a_dic(centro, date):
    d={}
    d["nombre"]= centro.nombre
    d["id"]= centro.id
    d["total"]= get_turnos_total(centro.id,date)
    d["asignados"] = get_turnos_asignados(centro.id,date)
    return d

def get_turnos_total(id,date):
    return 14 - get_turnos_asignados(id,date)

def get_turnos_asignados(id,date):
    return Turn.hours_assigns_api(id, date)




class API_estadisticas_tipo_centro(Resource):
    def get(self):
        try:

            centros = Center.all_activos()
            if not centros:
                return abort(404)
        except NoResultFound:
            return abort(404)

        return estadistics_dict(centros)



def makeDictionary():
    d={}
    tipo_centros = Tipo_Centro.all()
    for tipo in tipo_centros:
        d[tipo.nombre] = 0

    return d

'''Metodo ineficiente pero trabajo honesto'''
def sort_dict(d):
    new_d = {}
    lista =sorted(d.items())
    lista.reverse()
    for elem in lista:
        new_d[elem[0]]=elem[1]
    
    return new_d

def estadistics_dict(centros):

    d = makeDictionary()
    for centro in centros:
        for tipo in  centro.tipo_centro:
            try:
                d[tipo.nombre]= d[tipo.nombre] +1
            except KeyError:
                return abort(404)


    return sort_dict(d)

