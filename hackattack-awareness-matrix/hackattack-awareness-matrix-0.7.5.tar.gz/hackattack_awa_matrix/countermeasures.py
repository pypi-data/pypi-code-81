from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
import datetime
from werkzeug.exceptions import abort

from hackattack_awa_matrix.auth import login_required
from hackattack_awa_matrix.db import get_db

bp = Blueprint('countermeasure', __name__, url_prefix='/project/<int:project_id>/countermeasure')


def get_project(project_id):
    db = get_db()
    project = db.execute(
        'SELECT id, name, description, start_date, end_date'
        ' FROM project'
        ' WHERE id = ?', (project_id,)
    ).fetchone()

    if project is None:
        abort(404, "Project id {0} doesn't exist.".format(project_id))

    return project


def get_countermeasure(project_id, countermeasure_id):
    db = get_db()
    countermeasure = db.execute(
        'SELECT id, name, description, percentage_executed, project_id, created_at, due_date'
        ' FROM project_countermeasure'
        ' WHERE id = ? AND project_id = ?', (countermeasure_id, project_id)
    ).fetchone()

    if countermeasure_id is None:
        abort(404, "Countermeasure id {0} doesn't exist in project {1}.".format(countermeasure_id, project_id))

    return countermeasure


def do_countermeasure_db_operation(project_id, countermeasure_id=None):
    name = request.form['name']
    description = request.form['description']
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'percentage_executed' in request.form:
        percentage_executed = request.form['percentage_executed']
    else:
        percentage_executed = 0
    due_date = request.form['due_date']
    db = get_db()
    error = None

    if not name:
        error = 'Name der tech./org. Gegenmaßnahme wird benötigt!'

    if due_date == "":
        due_date = None
    else:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")

    if error is None:
        if countermeasure_id is not None:
            db.execute(
                'UPDATE project_countermeasure SET name = ?, description = ?, percentage_executed = ?, due_date = ? WHERE id = ? AND project_id = ?',
                (name, description, percentage_executed, due_date, countermeasure_id, project_id)
            )
        else:
            db.execute(
                'INSERT INTO project_countermeasure (name, description, percentage_executed, created_at, due_date, project_id) VALUES (?, ?, ?, ?, ?, ?)',
                (name, description, percentage_executed, created_at, due_date, project_id)
            )
        db.commit()
        return

    flash(error)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(project_id):
    if request.method == 'POST':
        do_countermeasure_db_operation(project_id, None)
        return redirect(url_for('countermeasure.index', project_id=project_id))

    return render_template('countermeasure/create_or_edit.html', project=get_project(project_id))


@bp.route('/<int:countermeasure_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(project_id, countermeasure_id):
    if request.method == 'POST':
        do_countermeasure_db_operation(project_id, countermeasure_id)
        return redirect(url_for('countermeasure.index', project_id=project_id))

    return render_template('countermeasure/create_or_edit.html', project=get_project(project_id), countermeasure=get_countermeasure(project_id, countermeasure_id))


@bp.route('/', methods=['GET'])
@login_required
def index(project_id):
    db = get_db()
    countermeasures = db.execute(
        'SELECT id, name, description, percentage_executed, project_id, created_at, due_date'
        ' FROM project_countermeasure'
        ' WHERE project_id = ?', (project_id, )
    ).fetchall()

    session["current_day"] = datetime.datetime.today()

    return render_template('countermeasure/index.html', countermeasures=countermeasures, project=get_project(project_id))


@bp.route('/delete', methods=['POST'])
@login_required
def delete(project_id):
    if 'deletion_object_id' not in request.form:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('countermeasure.index', project_id=project_id))

    countermeasure_id = request.form['deletion_object_id']

    if countermeasure_id is None or countermeasure_id == "":
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('countermeasure.index', project_id=project_id))

    countermeasure = get_countermeasure(project_id, countermeasure_id)

    if countermeasure is None:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('countermeasure.index', project_id=project_id))

    db = get_db()
    db.execute('DELETE FROM project_threat_countermeasure WHERE countermeasure_id = ?', (countermeasure['id'], ))
    db.commit()


    db.execute('DELETE FROM project_countermeasure WHERE id = ?', (countermeasure['id'], ))
    db.commit()

    return redirect(url_for('countermeasure.index', project_id=project_id))


def get_threats_of_countermeasure(project_id, countermeasure_id):
    db = get_db()
    threats = db.execute(
        'SELECT t.id, t.name, t.description, t.priority, t.project_id, t.created_at, t.due_date'
        ' FROM project_threat t, project_threat_countermeasure ptc, project_countermeasure pc'
        ' WHERE pc.id = ? AND t.project_id = ? AND pc.id = ptc.countermeasure_id AND t.id = ptc.threat_id', (countermeasure_id, project_id)
    ).fetchall()

    return threats


@bp.route('/<int:countermeasure_id>', methods=['GET'])
@login_required
def details(project_id, countermeasure_id):
    assigned_threats = get_threats_of_countermeasure(project_id, countermeasure_id)

    return render_template('countermeasure/details.html', project=get_project(project_id), countermeasure=get_countermeasure(project_id, countermeasure_id), assigned_threats=assigned_threats)
