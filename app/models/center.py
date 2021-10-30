""" Centers """
from sqlalchemy.orm.exc import NoResultFound
from app.db import database as db
from flask import jsonify, request, flash
import datetime
from sqlalchemy.dialects.mysql import TIME
from app.models.tipo_centro import Tipo_Centro
from datetime import date, datetime, timedelta

class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, unique=True, primary_key=True,
                   autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, index=True)
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    hora_apertura = db.Column(TIME(), nullable=False)
    hora_cierre = db.Column(TIME(), nullable=False)
    web = db.Column(db.String(30))
    estado = db.Column(db.Boolean, default=None,nullable=True)#importante que este en None
    longitud = db.Column(db.Float())
    latitud = db.Column(db.Float())
    protocolo_vista = db.Column(db.String())
    municipio = db.Column(db.Integer())
    tipo_centro = db.relationship("Tipo_Centro", secondary="center_has_type")
    turns = db.relationship('Turn', backref="center")

    def __repr__(self):
        """ String representation of center """
        return "<nombre %r>" % self.nombre

    def __init__(self, nombre,  direccion, telefono, hora_apertura, hora_cierre,longitud,latitud, municipio,web=None, estado=None, protocolo_vista=None, email=None):
        """ Center initialization """
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.hora_apertura = hora_apertura
        self.hora_cierre = hora_cierre
        self.web = web
        self.estado = estado
        self.protocolo_vista = protocolo_vista
        self.longitud = longitud
        self.latitud = latitud

        self.email = email
        self.municipio = municipio

    def turns_by(self, day):
        return  [turn for turn in sorted(self.turns, key=lambda x: (x.date,x.starting_time)) if 0 <= (turn.date.date() - date.today()).days < 3 ]

    @classmethod
    def all(cls):
        """ Returns all centers """
        return Center.query.all()
    @classmethod
    def all_activos(cls):
        """ Returns all active centers """
        return Center.query.filter_by(estado=True)

    @classmethod
    def all_activos_paginado(cls,pag,per_pag):
        return (cls.all_activos()).paginate(page=pag, per_page=per_pag)

    @classmethod
    def find(self, id):
        return Center.query.filter_by(id=id).one()

    @classmethod
    def create(cls, form,tipos_centros):
        """ Creates a new center """
        nombre = form.nombre.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        hora_apertura = form.hora_apertura.data
        hora_cierre = form.hora_cierre.data
        web = form.web.data
        protocolo_vista = form.protocolo_vista.data
        longitud = form.longitud.data
        latitud = form.latitud.data
        email = form.email.data
        municipio = form.municipio.data

        center = Center(nombre=nombre,  direccion=direccion, telefono=telefono, hora_apertura=hora_apertura,
                        hora_cierre=hora_cierre, web=web,  protocolo_vista=protocolo_vista, longitud=longitud,latitud=latitud, email=email,municipio=municipio)



        db.session.add(center)
        db.session.commit()

        for types in list(tipos_centros):
                center.tipo_centro.append(Tipo_Centro.find_by(id=int(types)))
                db.session.commit()
        return center
    @classmethod
    def update(cls, form,tipos_centros):
        center = Center.query.filter_by(id=form.id.data).first()

        center.nombre = form.nombre.data
        center.direccion = form.direccion.data
        center.telefono = form.telefono.data
        center.hora_apertura = form.hora_apertura.data
        center.hora_cierre = form.hora_cierre.data
        center.web = form.web.data
        estado = form.estado.data
        center.protocolo_vista = form.protocolo_vista.data
        center.longitud = form.longitud.data
        center.latitud = form.latitud.data
        center.email = form.email.data
        center.municipio = form.municipio.data


        db.session.commit()
        for tipo_centro in list(center.tipo_centro):
                if not tipo_centro in tipos_centros:
                    center.tipo_centro.remove(tipo_centro)
                    db.session.commit()

        for tipos_centros_add in tipos_centros:
            if not tipos_centros_add in center.tipo_centro:
                center.tipo_centro.append(Tipo_Centro.find_by(id=int(tipos_centros_add)))
                db.session.commit()

    @classmethod
    def remove(cls, id):
        center = Center.query.filter_by(id=id).first()
        db.session.delete(center)
        db.session.commit()

    @classmethod
    def find_by(cls, **args):
        return Center.query.filter_by(**args).first()
    @classmethod
    def last(cls, **args):
        return Center.query.order_by(Center.id.desc()).first()
    @classmethod
    def seed(cls,  nombre,  direccion, telefono, hora_apertura, hora_cierre, web, estado, protocolo_vista, longitud,latitud, email, types,municipio):
        """ Used in seed.py to populate database """
        # TODO: El create recibe parametros sanatizados del controller?
        existing_center = Center.find_by(email=email)
        if existing_center:
            return existing_center
        else:
            center = Center(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                hora_apertura=hora_apertura,
                hora_cierre=hora_cierre,
                web=web,
                estado=estado,
                protocolo_vista=protocolo_vista,
                longitud=longitud,
                latitud=latitud,
                email=email,
                municipio=municipio
            )
            db.session.add(center)
            db.session.commit()

            for types in list(types):
                center.tipo_centro.append(types)
                db.session.commit()
            return center

    @classmethod
    def approve(cls,id):
        center = Center.query.filter_by(id=id).first()
        center.estado = True

        db.session.commit()
    
    @classmethod
    def disapprove(cls,id):
        center = Center.query.filter_by(id=id).first()
        center.estado = False

        db.session.commit()

    def addFileName(self,file):
        self.protocolo_vista= file
        db.session.commit()

    @classmethod
    def buscar_centro_parcial_nombre(cls,nombre):
        search = "%{}%".format(nombre)
        return Center.query.filter(Center.nombre.like(search)).all()
    
    @classmethod
    def buscar_centro_parcial_filtro(cls,nombre,filtro):
        search = "%{}%".format(nombre)
        return Center.query.filter(Center.nombre.like(search),Center.estado  == filtro).all()


    @classmethod
    def turns_stats_all(cls, date):
        return [(centro, self.turns_by(centro,date)) for centro in self.all_activos()]
