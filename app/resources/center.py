""" Center controller """
from flask import Flask, redirect, render_template, request, url_for, session, abort, flash
from app.models.center import Center
from app.models.tipo_centro import Tipo_Centro
from app.resources import site
from app.helpers.validateCenters import CreateCenterForm, EditCenterForm
from app.helpers.auth import authenticated, user_has, logged_in
from werkzeug.utils import secure_filename
import os
import requests
import json

#hola
def allowed_file(filename):
    if filename != 'None':
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() == 'pdf'
    else:
        return False


def obtener_municipios():
    response = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
    municipios = response.json()
    municipios_format = []
    for municipio in municipios["data"]["Town"]:
        municipios_format.append(
            (municipio, municipios["data"]["Town"][municipio]['name']))

    return municipios_format


@site.route("/centers",methods=["GET","POST"])
@user_has("center_index")
def center_index():
    """ I N D E X  &&  F E T C H """
    centers = Center.all()
    if request.method =='POST':
        centers = []
        #hago las busquedas manualmente porque no entendi como modificar el componente de javascript :( y
        #tampoco queria usar otro
        if 'filter' in request.form:
            filtro= request.form.get('filter')
            if filtro =='Nombre':
                centers = Center.buscar_centro_parcial_nombre(request.form.get('search'))
            elif '0'==filtro or filtro=='1':
                centers = Center.buscar_centro_parcial_filtro(request.form.get('search'),int(filtro))
            else:
                centers = Center.buscar_centro_parcial_filtro(request.form.get('search'),None)



    return render_template("center/index.html", centers=centers)

@site.route("/centers/new", methods=["GET","POST"])
@user_has("center_new")
def center_new():
    """ Creates new center """
    form = CreateCenterForm()

    if request.method=="POST":
        form.municipio.data = int(request.form.get('municipios'))
        tipos_centros = request.form.getlist('tipos_centros')
        
        if form.validate_on_submit():
            center =Center.create(form, tipos_centros=tipos_centros)
            if 'file' in request.files:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    url_center= 'centro-pdf-'+str(center.id)+'-0.pdf'
                    file.save(os.path.join('app/static/uploads/'+url_center))
                    center.addFileName(url_center)

                elif file.filename != "":
                    flash("Protocolo de vista con formato invalido", "warning")
                    return redirect(url_for('site.center_new'))
        
            flash("Centro creado con éxito!", "success")
            return redirect(url_for('site.center_index'))

        flash("Datos ingresados incorrectos, pruebe de nuevo","warning")
    return render_template("center/new.html", form=form, municipios=obtener_municipios(), tipos_centros=Tipo_Centro.all())


@site.route("/centers/<int:id>/edit", methods=["GET", "POST"])
@user_has("center_update")
def center_edit(id):
    """ U P D A T E """
    center = Center.find(request.view_args['id'])
    if request.method == "GET":
        center = Center.find(request.view_args['id'])
        form = EditCenterForm()

        return render_template("center/edit.html", center=center, form=form, municipios=obtener_municipios(), tipos_centros=Tipo_Centro.all())
    elif request.method == "POST":
        form = EditCenterForm()
        form.municipio.data = int(request.form.get('municipios'))
        tipos_centros = request.form.getlist('tipos_centros')
        cant = 0
        if form.validate_on_submit():
            if request.form.get('borrar'):
                os.remove('app/static/uploads/'+center.protocolo_vista)
                form.protocolo_vista.data = None
            elif 'file' in request.files :
                if center.protocolo_vista  and center.protocolo_vista != request.files['file'].filename:
                    cant= int(center.protocolo_vista.split('.pdf')[0][-1]) + 1
                    os.remove('app/static/uploads/'+center.protocolo_vista)

                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    url_center= 'centro-pdf-'+str(center.id)+ '-'+str(cant)+'.pdf'
                    file.save(os.path.join('app/static/uploads/'+ url_center ))
                    form.protocolo_vista.data = url_center 
                elif file.filename != "":
                    flash("Protocolo de vista con formato invalido", "warning")
                    return redirect(url_for('site.center_edit', id=request.view_args['id']))
            

            Center.update(form, tipos_centros=tipos_centros)
            flash("Centro actualizado con éxito!", "success")
            return redirect(url_for('site.center_index'))

        flash("Datos ingresados incorrectos, pruebe de nuevo","warning")
        

    return redirect(url_for('site.center_edit', id=request.view_args['id']))


@site.route("/centers/<int:id>")
@user_has("center_show")
def center_show(id):
    """ S H O W """
    center = Center.find(id)
    return render_template("center/show.html", center=center, municipio=obtener_municipios()[center.municipio-1][1])


@site.route("/centers-delete/<int:id>")
@user_has("center_destroy")
def center_destroy(id):
    """ D E L E T E """
    id = request.view_args['id']
    center = Center.remove(id=id)
    flash('Centro eliminado con exito', "success")
    return redirect(url_for('site.center_index'))



##utilizo dos metodos para aprobar a desaprobar ya que los centros van a tener 3 estados, aprobado, 
#rechazado o pediente de aprobacion.
@site.route("/centers-approve/<int:id>")
@user_has("center_approve")
def center_approve(id):
    """ A P P R O V E"""
    id = request.view_args['id']
    Center.approve(id=id)
    flash('Centro aprobado con exito', "success")
    return redirect(url_for('site.center_index'))

@site.route("/centers-disapprove/<int:id>")
@user_has("center_approve")
def center_disapprove(id):
    """ D I S A P P R O V E"""
    id = request.view_args['id']
    Center.disapprove(id=id)
    flash('Centro desaprobado con exito', "success")
    return redirect(url_for('site.center_index'))
