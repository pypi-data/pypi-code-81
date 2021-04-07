from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import datetime
from werkzeug.exceptions import abort

from hackattack_awa_matrix.auth import login_required
from hackattack_awa_matrix.db import get_db

bp = Blueprint('awarenessmeasure', __name__, url_prefix='/project/<int:project_id>/awarenessmeasure')


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


def get_awarenessmeasure(project_id, awarenessmeasure_id):
    db = get_db()
    awarenessmeasure = db.execute(
        'SELECT id, name, description, percentage_executed, needs_legal_attention, legal_description, created_at, due_date, project_id'
        ' FROM project_awarenessmeasure'
        ' WHERE id = ? AND project_id = ?', (awarenessmeasure_id, project_id)
    ).fetchone()

    if awarenessmeasure is None:
        abort(404, "Awarenessmeasure id {0} doesn't exist for project {1}.".format(awarenessmeasure_id, project_id))

    return awarenessmeasure


def do_awa_measure_db_operation(project_id, awarenessmeasure_id=None):
    name = request.form['name']
    description = request.form['description']
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'percentage_executed' in request.form:
        percentage_executed = request.form['percentage_executed']
    else:
        percentage_executed = 0

    if 'needs_legal_attention' in request.form:
        needs_legal_attention = request.form['needs_legal_attention']
    else:
        needs_legal_attention = 0

    legal_description = request.form['legal_description']

    due_date = request.form['due_date']

    db = get_db()
    error = None

    if not name:
        error = 'Name der Awarenessmaßnahme wird benötigt!'

    if due_date == "":
        due_date = None
    else:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")

    if error is None:
        if awarenessmeasure_id is not None:
            db.execute(
                'UPDATE project_awarenessmeasure SET name = ?, description = ?, percentage_executed = ?, needs_legal_attention = ?, legal_description = ?, due_date = ? WHERE id = ? AND project_id = ?',
                (name, description, percentage_executed, needs_legal_attention, legal_description, due_date, awarenessmeasure_id, project_id)
            )
        else:
            db.execute(
                'INSERT INTO project_awarenessmeasure (name, description, percentage_executed, needs_legal_attention, legal_description, created_at, due_date, project_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (name, description, percentage_executed, needs_legal_attention, legal_description, created_at, due_date,
                 project_id)
            )
        db.commit()
        return

    flash(error)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(project_id):
    if request.method == 'POST':
        do_awa_measure_db_operation(project_id, None)
        return redirect(url_for('awarenessmeasure.index', project_id=project_id))

    return render_template('awarenessmeasure/create_or_edit.html', project=get_project(project_id))


@bp.route('/<int:awarenessmeasure_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(project_id, awarenessmeasure_id):
    if request.method == 'POST':
        do_awa_measure_db_operation(project_id, awarenessmeasure_id)
        return redirect(url_for('awarenessmeasure.index', project_id=project_id))

    return render_template('awarenessmeasure/create_or_edit.html', project=get_project(project_id), awarenessmeasure=get_awarenessmeasure(project_id, awarenessmeasure_id))


@bp.route('/', methods=['GET'])
@login_required
def index(project_id):
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT id, name, description, percentage_executed, needs_legal_attention, legal_description, project_id, created_at, due_date'
        ' FROM project_awarenessmeasure'
        ' WHERE project_id = ?', (project_id, )
    ).fetchall()

    return render_template('awarenessmeasure/index.html', awarenessmeasures=awarenessmeasures, project=get_project(project_id))


@bp.route('/delete', methods=['POST'])
@login_required
def delete(project_id):
    if 'deletion_object_id' not in request.form:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('awarenessmeasure.index', project_id=project_id))

    awameasure_id = request.form['deletion_object_id']

    if awameasure_id is None or awameasure_id == "":
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('awarenessmeasure.index', project_id=project_id))

    awarenessmeasure = get_awarenessmeasure(project_id, awameasure_id)

    if awarenessmeasure is None:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('awarenessmeasure.index', project_id=project_id))

    db = get_db()
    db.execute('DELETE FROM project_threat_awarenessmeasure WHERE awarenessmeasure_id = ?', (awarenessmeasure['id'], ))
    db.commit()


    db.execute('DELETE FROM project_awarenessmeasure WHERE id = ?', (awarenessmeasure['id'], ))
    db.commit()

    return redirect(url_for('awarenessmeasure.index', project_id=project_id))


def get_threats_of_awarenessmeasure(project_id, awarenessmeasure_id):
    db = get_db()
    threats = db.execute(
        'SELECT t.id, t.name, t.description, t.priority, t.project_id, t.created_at, t.due_date'
        ' FROM project_threat t, project_threat_awarenessmeasure pta, project_awarenessmeasure pa'
        ' WHERE pa.id = ? AND t.project_id = ? AND pa.id = pta.awarenessmeasure_id AND t.id = pta.threat_id', (awarenessmeasure_id, project_id)
    ).fetchall()

    return threats


@bp.route('/<int:awarenessmeasure_id>', methods=['GET'])
@login_required
def details(project_id, awarenessmeasure_id):
    return render_template('awarenessmeasure/details.html', project=get_project(project_id), awarenessmeasure=get_awarenessmeasure(project_id, awarenessmeasure_id), assigned_threats=get_threats_of_awarenessmeasure(project_id, awarenessmeasure_id))
