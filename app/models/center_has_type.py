""" Defines the relationship between Centers and Types of centers """
from app.db import database as db

class CenterHasType(db.Model):
    __tablename__ = "center_has_type"

    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'))
    tipo_centro_id = db.Column(db.Integer, db.ForeignKey('tipo_centro.id'))

    center = db.relationship("Center", backref=db.backref("centers", cascade="all, delete-orphan"))
    tipo_centro = db.relationship("Tipo_Centro", backref=db.backref("tipo_centro", cascade="all, delete-orphan"))

    @classmethod
    def center_has_this_type(cls,id_center,id_tipo):
        return bool(CenterHasType.filter_by(center_id=id_center,tipo_centro_id=id_tipo))