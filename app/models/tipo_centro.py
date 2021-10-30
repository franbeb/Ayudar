""" Centers """
from sqlalchemy.orm.exc import NoResultFound
from app.db import database as db


class Tipo_Centro(db.Model):
    __tablename__ = "tipo_centro"

    id = db.Column(db.Integer, unique=True, primary_key=True,
                   autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False, index=True)
    center = db.relationship("Center", secondary="center_has_type")
    def __repr__(self):
        return "<nombre %r>" % self.nombre

    def __init__(self, nombre):
        """ Tipo centro initialization """
        self.nombre = nombre

    @classmethod
    def all(cls):
        """ Returns all users """
        return Tipo_Centro.query.all()

    @classmethod
    def find(self, id):
        return Tipo_Centro.query.filter_by(id=id).one()

    @classmethod
    def find_by(cls, **args):
        return Tipo_Centro.query.filter_by(**args).first()

    @classmethod
    def create(cls, name):
        """ Create role in database """
        new_type = Tipo_Centro(nombre=name)
        db.session.add(new_type)
        db.session.commit()
        return new_type

    @classmethod
    def update(cls, form):
        tipo_centro = Tipo_Centro.query.filter_by(id=form.id.data).first()

        tipo_centro.nombre = form.nombre.data

        db.session.commit()

    @classmethod
    def remove(cls, id):
        tipo_centro = Tipo_Centro.query.filter_by(id=id).first()
        db.session.delete(tipo_centro)
        db.session.commit()

    @classmethod
    def seed(cls, nombre):
        """ Used in seed.py to populate database """
        # TODO: El create recibe parametros sanatizados del controller?
        existing_tipo_centro = Tipo_Centro.find_by(nombre=nombre)
        if existing_tipo_centro:
            return existing_tipo_centro
        else:
            tipo_centro = Tipo_Centro(
                nombre=nombre
            )
            db.session.add(tipo_centro)
            db.session.commit()
     
            return tipo_centro
