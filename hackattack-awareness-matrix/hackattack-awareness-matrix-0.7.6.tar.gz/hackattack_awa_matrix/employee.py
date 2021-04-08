from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app
)
import datetime
from werkzeug.exceptions import abort

from hackattack_awa_matrix.auth import login_required
from hackattack_awa_matrix.db import get_db

bp = Blueprint('employee', __name__, url_prefix='/project/<int:project_id>/employee_group')



def get_project(project_id):
    if project_id is None:
        return None

    db = get_db()

    query = 'SELECT id, name, description, start_date, end_date ' \
            'FROM project ' \
            'WHERE id = ?'
    current_app.logger.debug(
        "Getting the project by executing query '" + str(query) + "' with parameter: " + str(project_id))
    project = db.execute(query, (project_id,)).fetchone()

    if project is None:
        current_app.logger.error("Project id {0} doesn't exist.".format(project_id))
        abort(404, "Project id {0} doesn't exist.".format(project_id))

    return project

def get_employee(project_id, employee_id):
    db = get_db()
    project = db.execute(
        'SELECT id, name, description'
        ' FROM employee_group'
        ' WHERE id = ? AND project_id = ?', (employee_id, project_id)
    ).fetchone()

    if project is None:
        abort(404, "Employee id {0} doesn't exist.".format(employee_id))

    return project


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(project_id):
    if request.method == 'POST':
        do_employee_db_operation(project_id, None)
        return redirect(url_for('employee.index', project_id=project_id))

    return render_template('employee/create_or_edit.html', project=get_project(project_id))


@bp.route('/delete', methods=['POST'])
@login_required
def delete(project_id):
    if 'deletion_object_id' not in request.form:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('employee.index', project_id=project_id))

    emp_group_id = request.form['deletion_object_id']

    if emp_group_id is None or emp_group_id == "":
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('employee.index', project_id=project_id))

    emp_group = get_employee(project_id, emp_group_id)

    if emp_group is None:
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('employee.index', project_id=project_id))

    db = get_db()
    db.execute('DELETE FROM project_threat_affected_employee_group WHERE employee_group_id = ?', (emp_group['id'],))
    db.commit()

    db.execute('DELETE FROM employee_group WHERE id = ? AND project_id = ?', (emp_group['id'],project_id))
    db.commit()

    return redirect(url_for('employee.index', project_id=project_id))


def do_employee_db_operation(project_id, employee_id=None):
    name = request.form['name']
    description = request.form['description']
    db = get_db()
    error = None

    if not name:
        error = 'Employee-Group is required.'

    if error is None:

        if employee_id is not None:
            db.execute(
                'UPDATE employee_group SET name = ?, description = ? WHERE id = ? AND project_id = ?',
                (name, description, employee_id, project_id)
            )
        else:
            db.execute(
                'INSERT INTO employee_group (name, description, project_id) VALUES (?, ?, ?)',
                (name, description, project_id)
            )
        db.commit()
        return

    flash(error)


@bp.route('/<int:employee_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(project_id, employee_id):
    if request.method == 'POST':
        do_employee_db_operation(project_id, employee_id)
        return redirect(url_for('employee.index', project_id=project_id))

    return render_template('employee/create_or_edit.html', employee=get_employee(project_id, employee_id), project=get_project(project_id))


@bp.route('/', methods=['GET'])
@login_required
def index(project_id):
    db = get_db()
    employees = db.execute(
        'SELECT id, name, description'
        ' FROM employee_group'
        ' WHERE project_id = ?', (project_id, )
    ).fetchall()


    return render_template('employee/index.html', employees=employees, project=get_project(project_id))


def get_threats_of_employee_group(project_id, emp_group_id):
    db = get_db()
    threats = db.execute(
        'SELECT t.id, t.name, t.description, t.priority, t.project_id, t.created_at, t.due_date'
        ' FROM project_threat t, project_threat_affected_employee_group ptaeg, employee_group eg'
        ' WHERE eg.id = ? AND t.project_id = ? AND eg.id = ptaeg.employee_group_id AND t.id = ptaeg.threat_id', (emp_group_id, project_id)
    ).fetchall()

    return threats

@bp.route('/<int:employee_id>', methods=['GET'])
@login_required
def details(project_id, employee_id):
    return render_template('employee/details.html', employee=get_employee(project_id, employee_id), project=get_project(project_id), assigned_threats=get_threats_of_employee_group(project_id, employee_id))
