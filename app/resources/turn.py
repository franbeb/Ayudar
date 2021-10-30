""" Turns controller """
import json
from datetime import datetime
from flask import redirect, render_template, request, url_for, flash
from app.helpers.auth import user_has
from app.resources import site
from app.models.center import Center
from app.models.config import Config
from app.models.turn import Turn
from app.helpers.validateTurns import CreateTurnForm, EditTurnForm
from app.helpers.auth import public

""" I N D E X """
@site.route("/turns")
@user_has("turn_index")
def turn_superindex():
    """ Shows a list of all turns"""
    return render_template(
        "turn/superindex.html",
        turns = Turn.all(),
        page_elem = Config.first().cant_elem
    )

@site.route("/centers/<int:center_id>/turns")
@user_has("turn_index")
def turn_index(center_id):
    """ Shows a list of the turns of the center """

    center = Center.find(center_id)
    return render_template(
        "turn/index.html",
        center = center,
        turns = center.turns_by(day = 3),
        page_elem = Config.first().cant_elem
    )


""" S H O W """
@site.route("/turns/<int:id>/", methods=["GET"])
@user_has("turn_show")
def turn_show(id):
    """ Shows the turn details """
    return render_template("turn/show.html", turn= Turn.find(id))


""" C R E A T E """
@site.route("/centers/<int:center_id>/turns/new", methods=["GET"])
@user_has("turn_new")
def turn_new(center_id):
    """ New turn """
    center = Center.find(center_id)
    form = CreateTurnForm()
    return render_template("turn/new.html", center = center, form = form)

@site.route("/centers/<int:center_id>/turns/new", methods=["POST"])
@public
def turn_create(center_id):
    """ New turn """
    post = request.form
    form = CreateTurnForm(center_id=center_id, email = post.get('email'), starting_time = post.get('starting_time'), date = post.get('date'))
    center = Center.find(center_id)
    if(form.validate_on_submit()):
        Turn.create(
            email = form.email.data,
            starting_time = form.starting_time.data,
            date = form.date.data,
            center = center,
            tel=None,
        )
        flash("Turno creado con éxito!", "success")
        return redirect(url_for("site.turn_index", center_id=center_id))
    else:
        flash("Error", "warn")
        return render_template("turn/new.html", center = center, form = form)


""" U P D A T E """
@site.route("/turns/<int:id>/edit", methods=["GET"])
@user_has("turn_update")
def turn_edit(id):
    """ Edit turn """
    turn = Turn.find(id)
    form = EditTurnForm(email = turn.email, starting_time = turn.starting_time, date = turn.date)
    return render_template("turn/edit.html", turn=turn, form=form)

@site.route("/turns/<int:id>/edit", methods=["POST"])
@user_has("turn_update")
def turn_update(id):
    """ Edit turn """
    turn = Turn.find(id)
    post = request.form
    form = EditTurnForm(center_id = turn.center.id , email = post.get('email'), starting_time = post.get('starting_time'), date = post.get('date'))
    if(form.validate_on_submit()):
        turn.update(
            email = post.get('email'),
            starting_time = post.get('starting_time'),
            date = post.get('date')
        )
        flash("Turno actualizado con éxito!", "success")
        return redirect(url_for("site.turn_index", center_id=turn.center.id))
    else:
        flash("Error", "warn")
        return render_template("turn/edit.html", turn=turn, form=form)


""" D E S T R O Y """
@site.route("/turns/<int:id>/destroy")
@user_has("turn_destroy")
def turn_destroy(id):
    """ Destroy turn """
    turn = Turn.find(id)
    center = turn.center
    turn.destroy()
    return redirect(url_for("site.turn_index", center_id = center.id))


""" H E L P E R S """
#TODO: Replace with call to api
@site.route("/turns/<string:date>/free_hours/<int:center_id>", methods=["GET"])
@public
def free_hours(date, center_id):
    """ Returns the free hours to a given date """
    date = ("").join(date.split("-"))
    date = datetime.strptime(date, '%Y%m%d').date()
    return json.dumps(Turn.free_hours(center_id, date))
