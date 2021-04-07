from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
import datetime
from werkzeug.exceptions import abort

from hackattack_awa_matrix.auth import login_required
from hackattack_awa_matrix.db import get_db

bp = Blueprint('threat', __name__, url_prefix='/project/<int:project_id>/threat')


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

def get_threat(project_id, threat_id):
    db = get_db()
    threat = db.execute(
        'SELECT id, name, description, priority, project_id, created_at, due_date'
        ' FROM project_threat'
        ' WHERE id = ? AND project_id = ?', (threat_id, project_id)
    ).fetchone()

    if threat is None:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))

    return threat


def do_threat_db_operation(project_id, threat_id=None):
    name = request.form['name']
    description = request.form['description']
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priority = request.form['priority']
    due_date = request.form['due_date']
    db = get_db()
    error = None

    if not name:
        error = 'Name der Bedrohung wird benötigt.'

    if due_date == "":
        due_date = None
    else:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")

    if priority is None or priority == "":
        priority = 1
        highest_prio = db.execute(
            'SELECT max(priority) as highest_prio'
            ' FROM project_threat'
            ' WHERE project_id = ?', (project_id, )
        ).fetchone()
        if highest_prio is not None and highest_prio['highest_prio'] is not None:
            priority = int(highest_prio['highest_prio']) + 1

    if error is None:
        if threat_id is not None:
            db.execute(
                'UPDATE project_threat SET name = ?, description = ?, priority = ?, due_date = ? WHERE id = ? AND project_id = ?',
                (name, description, priority, due_date, threat_id, project_id)
            )
        else:
            db.execute(
                'INSERT INTO project_threat (name, description, priority, project_id, created_at, due_date) VALUES (?, ?, ?, ?, ?, ?)',
                (name, description, priority, project_id, created_at, due_date)
            )
        db.commit()
        return

    flash(error)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(project_id):
    if request.method == 'POST':
        do_threat_db_operation(project_id, None)
        return redirect(url_for('threat.index', project_id=project_id))

    return render_template('threat/create_or_edit.html', project=get_project(project_id))



@bp.route('/<int:threat_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(project_id, threat_id):
    if request.method == 'POST':
        do_threat_db_operation(project_id, threat_id)
        return redirect(url_for('threat.index', project_id=project_id))

    return render_template('threat/create_or_edit.html', project=get_project(project_id), threat=get_threat(project_id, threat_id))


@bp.route('/', methods=['GET'])
@login_required
def index(project_id):
    db = get_db()
    threats = db.execute(
        'SELECT id, name, description, priority, project_id, created_at, due_date'
        ' FROM project_threat'
        ' WHERE project_id = ? ORDER BY priority', (project_id, )
    ).fetchall()

    threats = [dict(row) for row in threats]
    for threat in threats:
        countermeasures = db.execute(
            'SELECT pc.name'
            ' FROM project_countermeasure pc, project_threat_countermeasure ptc'
            ' WHERE pc.project_id = ? AND ptc.threat_id = ? AND ptc.countermeasure_id = pc.id', (project_id, threat['id'])
        ).fetchall()

        threat['countermeasure_names'] = [x['name'] for x in countermeasures]

        awarenessmeasures = db.execute(
            'SELECT pa.name'
            ' FROM project_awarenessmeasure pa, project_threat_awarenessmeasure pta'
            ' WHERE pa.project_id = ? AND pta.threat_id = ? AND pta.awarenessmeasure_id = pa.id', (project_id, threat['id'])
        ).fetchall()

        threat['awarenessmeasure_names'] = [x['name'] for x in awarenessmeasures]

        emp_groups = db.execute(
            'SELECT eg.name'
            ' FROM employee_group eg, project_threat_affected_employee_group ptaeg, project_threat t'
            ' WHERE t.project_id = ? AND t.id = ptaeg.threat_id AND ptaeg.threat_id = ? AND ptaeg.employee_group_id = eg.id AND eg.project_id = t.project_id', (project_id, threat['id'])
        ).fetchall()

        threat['employee_names'] = [x['name'] for x in emp_groups]


    return render_template('threat/index.html', threats=threats, project=get_project(project_id))


@bp.route('/<int:threat_id>', methods=['GET'])
@login_required
def details(project_id, threat_id):
    already_assigned_countermeasures = get_assigned_countermeasures(project_id, threat_id)
    already_assigned_awarenessmeasures = get_assigned_awarenessmeasures(project_id, threat_id)
    affected_employees = get_assigned_employee_groups(project_id, threat_id)

    return render_template('threat/details.html', project=get_project(project_id), threat=get_threat(project_id, threat_id), already_assigned_countermeasures=already_assigned_countermeasures, already_assigned_awarenessmeasures=already_assigned_awarenessmeasures, affected_employees=affected_employees)


@bp.route('/delete', methods=['POST'])
@login_required
def delete(project_id):
    if 'deletion_object_id' not in request.form:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('threat.index', project_id=project_id))

    threat_id = request.form['deletion_object_id']

    if threat_id is None or threat_id == "":
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('threat.index', project_id=project_id))

    threat = get_threat(project_id, threat_id)

    if threat is None:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('threat.index', project_id=project_id))

    db = get_db()
    db.execute('DELETE FROM project_threat_countermeasure WHERE threat_id = ?', (threat['id'], ))
    db.commit()

    db.execute('DELETE FROM project_threat_awarenessmeasure WHERE threat_id = ?', (threat['id'], ))
    db.commit()

    db.execute('DELETE FROM project_threat_affected_employee_group WHERE threat_id = ?', (threat['id'], ))
    db.commit()

    db.execute('DELETE FROM project_threat WHERE id = ?', (threat['id'], ))
    db.commit()

    return redirect(url_for('threat.index', project_id=project_id))

################# Countermeasures assigned to threat #####################

def get_assigned_countermeasures(project_id, threat_id):
    db = get_db()
    countermeasures = db.execute(
        'SELECT pc.id, pc.name, pc.description, pc.percentage_executed, pc.project_id, pc.created_at, pc.due_date'
        ' FROM project_countermeasure pc, project_threat_countermeasure ptc'
        ' WHERE pc.project_id = ? AND ptc.countermeasure_id = pc.id AND ptc.threat_id = ?', (project_id, threat_id, )
    ).fetchall()

    return countermeasures


def get_still_available_countermeasures(project_id, threat_id):
    db = get_db()
    countermeasures = db.execute(
        'SELECT id, name, description, percentage_executed, project_id, created_at, due_date'
        ' FROM project_countermeasure'
        ' WHERE project_id = ? AND id NOT IN (SELECT DISTINCT countermeasure_id FROM project_threat_countermeasure WHERE threat_id = ? )', (project_id, threat_id, )
    ).fetchall()

    return countermeasures


@bp.route('/<int:threat_id>/manage_countermeasures', methods=['GET'])
@login_required
def manage_countermeasures(project_id, threat_id):
    assigned_countermeasures = get_assigned_countermeasures(project_id, threat_id)
    still_available_countermeasures = get_still_available_countermeasures(project_id, threat_id)

    return render_template('threat/manage_countermeasure_assignments.html', project=get_project(project_id), threat=get_threat(project_id, threat_id), assigned_countermeasures=assigned_countermeasures, still_available_countermeasures=still_available_countermeasures)


def clear_countermeasures_of_threat(project_id, threat_id):
    db = get_db()
    threat = get_threat(project_id, threat_id)

    if threat is not None:
        db.execute(
            'DELETE FROM project_threat_countermeasure WHERE threat_id = ?',
            (threat_id,)
        )
        db.commit()
    else:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))

def save_countermeasure_to_threat(project_id, threat_id, cm_id_to_save):
    db = get_db()
    threat = get_threat(project_id, threat_id)

    if threat is not None:
        db.execute(
            'INSERT INTO project_threat_countermeasure (threat_id, countermeasure_id) VALUES (?, ?)',
            (threat_id, cm_id_to_save)
        )
        db.commit()
    else:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))


@bp.route('/<int:threat_id>/save_countermeasures', methods=['POST'])
@login_required
def save_countermeasures(project_id, threat_id):
    countermeasure_ids_to_save = request.values.getlist('countermeasure_ids_to_save[]')

    clear_countermeasures_of_threat(project_id, threat_id)

    for cm_id_to_save in countermeasure_ids_to_save:
        save_countermeasure_to_threat(project_id, threat_id, cm_id_to_save)

    return "success"


################# Awarenessmeasures assigned to threat #####################

def get_assigned_awarenessmeasures(project_id, threat_id):
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT pa.id, pa.name, pa.description, pa.percentage_executed, pa.needs_legal_attention, pa.legal_description, pa.project_id, pa.created_at, pa.due_date'
        ' FROM project_awarenessmeasure pa, project_threat_awarenessmeasure pta'
        ' WHERE pa.project_id = ? AND pta.awarenessmeasure_id = pa.id AND pta.threat_id = ?', (project_id, threat_id, )
    ).fetchall()

    return awarenessmeasures


def get_still_available_awarenessmeasures(project_id, threat_id):
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT id, name, description, percentage_executed, needs_legal_attention, legal_description, project_id, created_at, due_date'
        ' FROM project_awarenessmeasure'
        ' WHERE project_id = ? AND id NOT IN (SELECT DISTINCT awarenessmeasure_id FROM project_threat_awarenessmeasure WHERE threat_id = ? )', (project_id, threat_id, )
    ).fetchall()

    return awarenessmeasures


@bp.route('/<int:threat_id>/manage_awarenessmeasures', methods=['GET'])
@login_required
def manage_awarenessmeasures(project_id, threat_id):
    assigned_awarenessmeasures = get_assigned_awarenessmeasures(project_id, threat_id)
    still_available_awarenessmeasures = get_still_available_awarenessmeasures(project_id, threat_id)

    return render_template('threat/manage_awarenessmeasure_assignments.html', project=get_project(project_id), threat=get_threat(project_id, threat_id), assigned_awarenessmeasures=assigned_awarenessmeasures, still_available_awarenessmeasures=still_available_awarenessmeasures)


def clear_awarenessmeasures_of_threat(project_id, threat_id):
    db = get_db()
    threat = get_threat(project_id, threat_id)

    if threat is not None:
        db.execute(
            'DELETE FROM project_threat_awarenessmeasure WHERE threat_id = ?',
            (threat_id,)
        )
        db.commit()
    else:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))

def save_awarenessmeasure_to_threat(project_id, threat_id, am_id_to_save):
    db = get_db()
    threat = get_threat(project_id, threat_id)

    if threat is not None:
        db.execute(
            'INSERT INTO project_threat_awarenessmeasure (threat_id, awarenessmeasure_id) VALUES (?, ?)',
            (threat_id, am_id_to_save)
        )
        db.commit()
    else:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))


@bp.route('/<int:threat_id>/save_awarenessmeasures', methods=['POST'])
@login_required
def save_awarenessmeasures(project_id, threat_id):
    awarenessmeasure_ids_to_save = request.values.getlist('awarenessmeasure_ids_to_save[]')

    clear_awarenessmeasures_of_threat(project_id, threat_id)

    for am_id_to_save in awarenessmeasure_ids_to_save:
        save_awarenessmeasure_to_threat(project_id, threat_id, am_id_to_save)

    return "success"




################# Employee-Groups assigned to threat #####################

def get_assigned_employee_groups(project_id, threat_id):
    db = get_db()
    employee_groups = db.execute(
        'SELECT emp.id, emp.name, emp.description, emp.project_id'
        ' FROM employee_group emp, project_threat_affected_employee_group ptaeg'
        ' WHERE emp.id = ptaeg.employee_group_id AND ptaeg.threat_id = ? AND emp.project_id = ?', (threat_id, project_id)
    ).fetchall()

    return employee_groups


def get_still_available_employee_groups(project_id, threat_id):
    db = get_db()
    employee_groups = db.execute(
        'SELECT id, name, description, project_id'
        ' FROM employee_group'
        ' WHERE id NOT IN (SELECT DISTINCT employee_group_id FROM project_threat_affected_employee_group WHERE threat_id = ? )'
        ' AND project_id = ?', (threat_id, project_id)
    ).fetchall()

    return employee_groups


@bp.route('/<int:threat_id>/manage_employee_groups', methods=['GET'])
@login_required
def manage_employee_groups(project_id, threat_id):
    assigned_employee_groups = get_assigned_employee_groups(project_id, threat_id)
    still_available_employee_groups = get_still_available_employee_groups(project_id, threat_id)

    return render_template('threat/manage_employee_assignments.html', project=get_project(project_id), threat=get_threat(project_id, threat_id), assigned_employee_groups=assigned_employee_groups, still_available_employee_groups=still_available_employee_groups)


def clear_employee_groups_of_threat(project_id, threat_id):
    db = get_db()
    threat = get_threat(project_id, threat_id)

    if threat is not None:
        db.execute(
            'DELETE FROM project_threat_affected_employee_group WHERE threat_id = ?',
            (threat_id,)
        )
        db.commit()
    else:
        abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))


def get_employee_group(project_id, employee_id):
    db = get_db()
    emp_group = db.execute(
        'SELECT id, name, description, project_id'
        ' FROM employee_group'
        ' WHERE id = ? AND project_id = ?', (employee_id, project_id)
    ).fetchone()

    return emp_group


def save_employee_groups_to_threat(project_id, threat_id, empg_id_to_save):
    db = get_db()
    threat = get_threat(project_id, threat_id)


    emp_group = get_employee_group(project_id, empg_id_to_save)

    if emp_group is not None and emp_group["project_id"] == project_id:
        if threat is not None:
            db.execute(
                'INSERT INTO project_threat_affected_employee_group (threat_id, employee_group_id) VALUES (?, ?)',
                (threat_id, empg_id_to_save)
            )
            db.commit()
        else:
            abort(404, "´Threat id {0} doesn't exist in project {1}.".format(threat_id, project_id))
    else:
        abort(403, "You are not allowed to assign an employee group from a different project!")


@bp.route('/<int:threat_id>/save_employee_groups', methods=['POST'])
@login_required
def save_employee_groups(project_id, threat_id):
    emp_group_ids_to_save = request.values.getlist('employee_group_ids_to_save[]')

    clear_employee_groups_of_threat(project_id, threat_id)

    for empg_id_to_save in emp_group_ids_to_save:
        save_employee_groups_to_threat(project_id, threat_id, empg_id_to_save)

    return "success"
