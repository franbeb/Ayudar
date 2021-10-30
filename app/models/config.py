from app.db import database as db

class Config(db.Model):
    __tablename__ = "configs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(255))
    mail = db.Column(db.String(30))
    cant_elem=db.Column(db.Integer)
    habilitado =  db.Column(db.Boolean)

    @classmethod
    def first(cls):
        return Config.query.first()

    @classmethod
    def update(cls,data):
        configuracion = Config.query.first()
        configuracion.title=  data['titulo']
        configuracion.description =data['descripcion']
        configuracion.mail =data['mail_contacto']
        configuracion.habilitado =data['habilitar_sitio']
        if int(data['cant_elementos']) < 1:
            data["cant_elementos"]= "1"
        configuracion.cant_elem = data['cant_elementos']
        # configuracion.update().values(data=datatitle=title, description=description, mail = mail,cant_elem=cant_elem,habilitado=habilitado)
        db.session.commit()

    @classmethod
    def count(cls):
        return Config.query.count()

    @classmethod
    def create(cls, title, description, mail, cant_elem, habilitado):
        config = Config(
            title = title,
            description = description,
            mail = mail,
            cant_elem = cant_elem,
            habilitado = habilitado
        )
        db.session.add(config)
        db.session.commit()
        return config


    @classmethod
    def seed(cls, title, description, mail, cant_elem, habilitado):
        # TODO: Chequear si existe (si en algun momento tenemos mas de una configuracion)
        if Config.count() == 0:
            return Config.create(title, description, mail, cant_elem, habilitado)
