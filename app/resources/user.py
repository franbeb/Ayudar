""" User controller """
from flask import Flask, redirect, render_template, request, url_for, session, abort, flash
from app.models.user import User
from app.models.user_has_role import UserHasRole
from app.models.role import Role
from app.helpers.auth import authenticated, user_has, logged_in
from app.resources import site
from app.helpers.validateUsers import CreateUserForm, EditUserForm,EditPassword
from sqlalchemy import literal



@site.route("/usuarios", methods=["POST", "GET"])
@user_has("user_index")
def user_index():
    """ I N D E X  &&  F E T C H """
    users = User.all()

    if request.method == 'POST':
        users = []
        #options = request.form.get("filter")
        if 'search-by-user' in request.form:
            print(request.form.get('username'))
            # users = User.query.filter_by(username=request.form.get('username')).all() old way, por si las moscas
            users = User.query.filter(User.username.contains(request.form.get('username'))).all()
        else:
            print(request.form.get('active'))
            if request.form.get('active')=='active':
                users = User.query.filter_by(active=1).all()
            else:
                users = User.query.filter_by(active=0).all()

        if not users:
            flash('No se encontró ningún resultado para su búsqueda',"warning")
            users = User.all()

    return render_template("user/index.html", users=users)


@site.route("/usuarios/nuevo")
@user_has("user_new")
def user_new():
    """ C R E A T E """
    form = CreateUserForm()
    roles = Role.allTuples()
    form.roles.choices=[(int(rol.id), rol.name) for rol in roles]
    return render_template("user/new.html", form=form)

@site.route("/usuarios/nuevo/post", methods=["POST"])
@user_has("user_new")
def user_create():
    """ Creates new user """
    form = CreateUserForm()
    roles = Role.allTuples()
    form.roles.choices=[(int(rol.id), rol.name) for rol in roles]
    print("ROLESSSSSS ELEGIDOSSSS", form.roles.data)
    if form.validate_on_submit():
        User.create(form)
        flash("Usuari@ cread@ con éxito!", "success")
        return redirect(url_for('site.user_index'))
    return redirect(url_for('site.user_new')) # se refreseha y se genera de neuvo el form

#@site.route("/usuarios/<id>")
@user_has("user_update")
def user_edit(id):
    """ U P D A T E """
    id = request.view_args['id']
    if request.method == "GET":
        user=User.find(id)
        form = EditUserForm()
        roles = Role.allTuples()
        form.roles.choices=[(int(rol.id), rol.name) for rol in roles]
        roles= [ur.id for ur in user.roles]
        return render_template("user/edit.html", user=user, form=form, roles=roles)
    else:
        form = EditUserForm()
        form.roles.choices=[(int(rol.id), rol.name) for rol in Role.allTuples()]
        print(form.roles.data)
        if form.validate_on_submit():
            User.update(form)
            flash("Usuari@ modificad@ con éxito!", "success")
            return redirect(url_for('site.user_index'))
        return redirect(url_for('site.user_edit',id=id))

#@site.route("/usuarios-delete/<id>")
@user_has("user_delete")
def user_delete(id):
    """ D E L E T E """
    id = request.view_args['id']
    if int(id) == session.get("user"):
        flash('Un usuari@ no puede autoeliminarse!',"warning")
        return redirect(url_for('site.user_index'))
    elif UserHasRole.tieneRolAdmin(id):
        flash('Un usuari@ administrador no puede ser elimind@!',"warning")
        return redirect(url_for('site.user_index'))
    else:
        User.remove(id)
        flash('Usuari@ eliminad@!',"success")
        return redirect(url_for('site.user_index'))

#@site.route("/usuarios-active/<id>")
@user_has("user_update")
def user_active(id):
    """ A C T I V E """
    idUser= request.view_args['id']

    if UserHasRole.tieneRolAdmin(idUser):
        flash('No puede desactivar un usuario admin',"warning")
    else:
        User.updateActive(id=idUser)


        flash('Usuario modificado',"success")

    return redirect(url_for('site.user_index'))


@site.route("/user/show")
@user_has("user_show")
def user_show():
    """ S H O W YOUR OWN PROFILE"""
    id = session['user']
    user=User.find(id)
    return render_template("user/show.html", user=user)

@site.route("/user/change_password",methods=["POST", "GET"])
@user_has("user_show")
def user_change_password( ):
    """ C H A N GE P A S S W O R D """
    
    form =EditPassword()
    if request.method == "POST":
        id = session['user']
        if form.validate_on_submit():
            if form.password_1.data == form.password_2.data:
                
               if User.change_password(id,new_pass=form.password_1.data,old_pass=form.password_0.data):
                   flash("La contraseña se cambio con exito","success")
                   return redirect(url_for('site.auth_logout'))

            flash("Datos ingresados incorrectos, pruebe de nuevo","warning")
        
    return render_template("user/change_password.html",form=form)