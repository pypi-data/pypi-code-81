import inspect
import os

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, current_app, send_file, after_this_request
)
import datetime, uuid
from werkzeug.exceptions import abort
from dateutil.relativedelta import *

from hackattack_awa_matrix.auth import login_required
from hackattack_awa_matrix.db import get_db
import xlsxwriter

bp = Blueprint('project', __name__, url_prefix='/project')


def get_project(project_id):
    db = get_db()

    query = 'SELECT id, name, description, start_date, end_date ' \
            'FROM project ' \
            'WHERE id = ?'
    current_app.logger.debug("Getting the project by executing query '" + str(query) + "' with parameter: " + str(project_id))
    project = db.execute(query, (project_id,)).fetchone()

    if project is None:
        current_app.logger.error("Project id {0} doesn't exist.".format(project_id))
        abort(404, "Project id {0} doesn't exist.".format(project_id))

    return project


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

    if request.method == 'POST':
        current_app.logger.info("Creating a new Project!")
        do_proj_db_operation(None)
        return redirect(url_for('project.index'))

    current_app.logger.debug("Requesting the Project creation view via a GET Request")
    return render_template('project/create_or_edit.html')


def do_proj_db_operation(project_id=None):
    name = request.form['name']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    db = get_db()
    error = None

    if not name:
        current_app.logger.error("During project manipulation the name was not supplied. Showing error to user.")
        error = 'Projectname is required.'
    elif not start_date or start_date == "":
        current_app.logger.error("During project manipulation the Start-Date was not supplied. Showing error to user.")
        error = 'Start-Date is required.'

    if end_date == "":
        end_date = None
    else:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")

    if error is None:
        current_app.logger.info("Project with the name '" + str(name) + "' will be manipulated.")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")

        if project_id is not None:
            query ='UPDATE project SET name = ?, description = ?, start_date = ?, end_date = ? WHERE id = ?'
            current_app.logger.debug(
                "Sending project update query to DB: '" + str(query) + "', with parameters: (" + str(
                    name) + ", " + str(description) + ", " + str(start_date) + ", " + str(end_date) + ", " + str(
                    project_id) + ")")
            db.execute(query, (name, description, start_date, end_date, project_id))
        else:
            query = 'INSERT INTO project (name, description, start_date, end_date) VALUES (?, ?, ?, ?)'
            current_app.logger.debug(
                "Sending project creation query to DB: '" + str(query) + "', with parameters: (" + str(
                    name) + ", " + str(description) + ", " + str(start_date) + ", " + str(end_date) + ")")
            db.execute(query, (name, description, start_date, end_date))
        db.commit()
        return

    flash(error)


@bp.route('/<int:project_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(project_id):
    if request.method == 'POST':
        current_app.logger.info("Updating a Project!")
        do_proj_db_operation(project_id)
        return redirect(url_for('project.index'))

    current_app.logger.debug("Requesting the Project edit view via a GET Request")
    return render_template('project/create_or_edit.html', project=get_project(project_id))


@bp.route('/', methods=['GET'])
@login_required
def index():
    current_app.logger.info("Opening Project index")
    db = get_db()

    query = 'SELECT id, name, description, start_date, end_date ' \
            'FROM project'
    current_app.logger.debug("Executing Query '" + str(query) + "' on database.")
    projects = db.execute(query).fetchall()
    current_app.logger.debug("Got " + str(len(projects)) + " results.")
    return render_template('project/index.html', projects=projects)


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    if 'deletion_object_id' not in request.form:
        current_app.logger.error("The requested project deletion returned an error because the parameter 'deletion_object_id' was not set in the request")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('project.index'))

    project_id = request.form['deletion_object_id']

    if project_id is None or project_id == "":
        current_app.logger.error("The requested project deletion returned an error because the parameter 'deletion_object_id' contained an invalid value: '" + str(project_id) + "'")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('project.index'))

    current_app.logger.info("Project deletion requested for Project with id: " + str(project_id))
    project = get_project(project_id)


    if project is None:
        current_app.logger.error("The requested project with id '" + str(project_id) + "' was not found in the database")
        error = "Die zu löschende ID wurde nicht gefunden."
        flash(error)
        return redirect(url_for('project.index'))

    current_app.logger.info("Project was found and has the name '" + str(project['name']) + "'")
    current_app.logger.info("Deletion of Project '" + str(project['name']) + "' start now!")

    db = get_db()

    current_app.logger.debug("Deleting all countermeasures that were assigned to threats inside the project")
    db.execute('DELETE FROM project_threat_countermeasure WHERE threat_id IN (SELECT id FROM project_threat WHERE project_id = ?)', (project['id'],))
    db.commit()

    db.execute('DELETE FROM project_threat_countermeasure WHERE countermeasure_id IN (SELECT id FROM project_countermeasure WHERE project_id = ?)', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting all countermeasures inside the project")
    db.execute('DELETE FROM project_countermeasure WHERE project_id = ?', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting all awarenessmeasures that were assigned to threats inside the project")
    db.execute('DELETE FROM project_threat_awarenessmeasure WHERE threat_id IN (SELECT id FROM project_threat WHERE project_id = ?)', (project['id'],))
    db.commit()

    db.execute('DELETE FROM project_threat_awarenessmeasure WHERE awarenessmeasure_id IN (SELECT id FROM project_awarenessmeasure WHERE project_id = ?)', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting all awarenessmeasures inside the project")
    db.execute('DELETE FROM project_awarenessmeasure WHERE project_id = ?', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting all associated employee groups of the project. (Just the relations, not the Emp-Groups itself)")
    db.execute('DELETE FROM project_threat_affected_employee_group WHERE threat_id IN (SELECT id FROM project_threat WHERE project_id = ?)', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting all associated employee groups of the project. (Just the relations, not the Emp-Groups itself)")
    db.execute('DELETE FROM project_threat_affected_employee_group WHERE threat_id IN (SELECT id FROM employee_group WHERE project_id = ?)', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting the project's threats")
    db.execute('DELETE FROM project_threat WHERE project_id = ?', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting the project's employee_groups")
    db.execute('DELETE FROM employee_group WHERE project_id = ?', (project['id'],))
    db.commit()

    current_app.logger.debug("Deleting the project itself")
    db.execute('DELETE FROM project WHERE id = ?', (project['id'],))
    db.commit()

    if 'selected_project' in session and project['id'] == session['selected_project']:
        session['selected_project'] = None

    current_app.logger.info("Deletion of the project was successful!")

    return redirect(url_for('project.index'))



def get_countermeasures_of_threat(project_id, threat_id):
    countermeasure_arr = []
    db = get_db()
    countermeasures = db.execute(
        'SELECT pc.id, pc.name, pc.description, pc.percentage_executed, pc.project_id, pc.created_at, pc.due_date'
        ' FROM project_countermeasure pc, project_threat_countermeasure ptc'
        ' WHERE pc.id = ptc.countermeasure_id AND ptc.threat_id = ? AND pc.project_id = ?', (threat_id, project_id,)
    ).fetchall()

    for cm in countermeasures:
        countermeasure_arr.append(cm)

    return countermeasure_arr


def get_affected_employees_of_threat(project_id, threat_id):
    emp_group_arr = []
    db = get_db()
    emp_groups = db.execute(
        'SELECT eg.id, eg.name, eg.description'
        ' FROM employee_group eg, project_threat_affected_employee_group ptaeg'
        ' WHERE eg.id = ptaeg.employee_group_id AND ptaeg.threat_id = ?', (threat_id,)
    ).fetchall()

    for emp in emp_groups:
        emp_group_arr.append(emp['name'])

    return emp_group_arr


def get_awarenessmeasures_of_threat(project_id, threat_id):
    awarenessmeasure_arr = []
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT pa.id, pa.name, pa.description, pa.percentage_executed, pa.needs_legal_attention, pa.legal_description, pa.project_id, pa.created_at, pa.due_date'
        ' FROM project_awarenessmeasure pa, project_threat_awarenessmeasure ptc'
        ' WHERE pa.id = ptc.awarenessmeasure_id AND ptc.threat_id = ? AND pa.project_id = ?', (threat_id, project_id,)
    ).fetchall()

    for am in awarenessmeasures:
        awarenessmeasure_arr.append(am)


    return awarenessmeasure_arr


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_threats_of_project_with_subattributes(project_id):
    db = get_db()
    db.row_factory = dict_factory
    threats = db.execute(
        'SELECT id, name, description, priority, project_id, created_at, due_date'
        ' FROM project_threat'
        ' WHERE project_id = ?', (project_id,)
    ).fetchall()

    for threat in threats:
        threat_id = threat['id']
        threat["countermeasures"] = get_countermeasures_of_threat(project_id, threat_id)
        threat["countermeasures_names"] = [cm['name'] for cm in threat["countermeasures"]]
        threat["affected_employees"] = get_affected_employees_of_threat(project_id, threat_id)
        threat["awarenessmeasures"] = get_awarenessmeasures_of_threat(project_id, threat_id)
        threat["awarenessmeasures_legal_descriptions"] = [am['legal_description'] for am in threat["awarenessmeasures"] if am['legal_description'] is not None and am['legal_description'] != ""]
        threat["awarenessmeasures_names"] = [am['name'] for am in threat["awarenessmeasures"]]


    return sorted(threats, key=lambda k: k['priority'])


def get_unique_awameasures_of_project(project_id):
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT DISTINCT pa.id, pa.name, pa.description, pa.percentage_executed, pa.needs_legal_attention, pa.legal_description, pa.project_id, pa.created_at, pa.due_date'
        ' FROM project_awarenessmeasure pa'
        ' WHERE pa.project_id = ?', (project_id,)
    ).fetchall()

    return awarenessmeasures

def get_awarenessmeasures_of_project(project_id):
    db = get_db()
    awarenessmeasures = db.execute(
        'SELECT DISTINCT pa.id, pa.name, pa.description, pa.percentage_executed, pa.needs_legal_attention, pa.legal_description, pa.project_id, pa.created_at, pa.due_date, t.name as threat_name'
        ' FROM project_awarenessmeasure pa'
        '   LEFT JOIN project_threat_awarenessmeasure ptc ON pa.id = ptc.awarenessmeasure_id'
        '   LEFT JOIN project_threat t ON ptc.threat_id = t.id'
        ' WHERE pa.project_id = ?', (project_id,)
    ).fetchall()

    return awarenessmeasures

def get_unique_countermeasures_of_project(project_id):
    db = get_db()
    countermeasures = db.execute(
        'SELECT DISTINCT pc.id, pc.name, pc.description, pc.percentage_executed, pc.project_id, pc.created_at, pc.due_date'
        ' FROM project_countermeasure pc'
        ' WHERE pc.project_id = ?',
        (project_id,)
    ).fetchall()

    return countermeasures


def get_countermeasures_of_project(project_id):
    db = get_db()
    countermeasures = db.execute(
        'SELECT DISTINCT pc.id, pc.name, pc.description, pc.percentage_executed, pc.project_id, pc.created_at, pc.due_date, t.name as threat_name'
        ' FROM project_countermeasure pc'
        '    LEFT JOIN project_threat_countermeasure ptc ON pc.id = ptc.countermeasure_id'
        '    LEFT JOIN project_threat t ON ptc.threat_id = t.id'
        ' WHERE pc.project_id = ?',
        (project_id,)
    ).fetchall()

    return countermeasures


def write_dashboard_worksheet(workbook, calculated_threats):
    worksheet = workbook.add_worksheet(name='Dashboard')

    data = []
    for threat in calculated_threats:
        data_to_write = (
            threat['id'],
            threat['priority'],
            threat['name'],
            ', '.join([x['name'] for x in threat['countermeasures']]) if threat['countermeasures'] is not None and len(threat['countermeasures']) > 0 else None,
            ', '.join(threat['affected_employees']) if threat['affected_employees'] is not None and len(threat['affected_employees']) > 0 else None,
            ', '.join([x['name'] for x in threat['awarenessmeasures']]) if threat['awarenessmeasures'] is not None and len(threat['awarenessmeasures']) > 0 else None,
            ', '.join(threat['awarenessmeasures_legal_descriptions']) if threat['awarenessmeasures_legal_descriptions'] is not None and len(threat['awarenessmeasures_legal_descriptions']) > 0 else None
        )
        data.append(data_to_write)

    # Set the columns widths.
    worksheet.set_column('A:G', 25)
    worksheet.add_table('A1:G' + str(len(calculated_threats) + 1), {
        'header_row': 1,
        'style': 'Table Style Medium 2',
        'data': data,
        'columns': [
            {'header': 'Bedrohungs-ID'},
            {'header': 'Priorität'},
            {'header': 'Bedrohung'},
            {'header': 'technische/org Gegenmaßnahme'},
            {'header': 'Betroffene Mitarbeiter'},
            {'header': 'Awarenessmaßnahmen'},
            {'header': 'Rechtliche Abklärung'}
        ]
    })


def write_threat_worksheet(workbook, calculated_threats):
    worksheet = workbook.add_worksheet(name='Bedrohungen')

    data = []
    for threat in calculated_threats:
        data_to_write = (
            threat['id'],
            threat['priority'],
            threat['name'],
            threat['description'],
            ', '.join(threat['affected_employees']))
        data.append(data_to_write)

    # Set the columns widths.
    worksheet.set_column('A:E', 25)
    worksheet.add_table('A1:E' + str(len(calculated_threats) + 1), {
        'header_row': 1,
        'style': 'Table Style Medium 2',
        'data': data,
        'columns': [
            {'header': 'Bedrohungs-ID'},
            {'header': 'Priorität'},
            {'header': 'Bedrohung'},
            {'header': 'Beschreibung'},
            {'header': 'Betroffene Mitarbeiter'}
        ]
    })


def write_countermeasures_worksheet(workbook, countermeasures_of_project):
    worksheet = workbook.add_worksheet(name='Gegenmaßnahmen')

    data = []
    for countermeasure in countermeasures_of_project:
        data_to_write = (
            countermeasure['threat_name'],
            countermeasure['name'],
            countermeasure['description'],
            countermeasure['percentage_executed'],
            countermeasure['due_date'].strftime("%d.%m.%Y") if countermeasure['due_date'] is not None else None
        )
        data.append(data_to_write)

    # Set the columns widths.
    worksheet.set_column('A:E', 25)
    worksheet.add_table('A1:E' + str(len(countermeasures_of_project) + 1), {
        'header_row': 1,
        'style': 'Table Style Medium 2',
        'data': data,
        'columns': [
            {'header': 'Bedrohung'},
            {'header': 'Name'},
            {'header': 'Beschreibung'},
            {'header': '% umgesetzt'},
            {'header': 'Fällig bis'}
        ]
    })


def write_awarenessmeasures_worksheet(workbook, awarenessmeasures_of_project):
    worksheet = workbook.add_worksheet(name='Awarenessmaßnahmen')

    data = []
    for am in awarenessmeasures_of_project:
        data_to_write = (
            am['name'],
            am['description'],
            am['threat_name'],
            am['percentage_executed'],
            'y' if am['needs_legal_attention'] is True or am['needs_legal_attention'] == 1 else 'n',
            am['legal_description'] if am['legal_description'] is not None else None,
            am['due_date'].strftime("%d.%m.%Y") if am['due_date'] is not None else None
        )
        data.append(data_to_write)

    # Set the columns widths.
    worksheet.set_column('A:G', 25)
    worksheet.add_table('A1:G'+str(len(awarenessmeasures_of_project)+1), {
                                                        'header_row': 1,
                                                        'style': 'Table Style Medium 2',
                                                        'data': data,
                                                        'columns': [
                                                            {'header': 'Awarenessmaßnahme'},
                                                            {'header': 'Beschreibung'},
                                                            {'header': 'Bedrohung'},
                                                            {'header': '% umgesetzt'},
                                                            {'header': 'rechtlich abzuklären (y/n)'},
                                                            {'header': 'Rechtliche Beschreibung'},
                                                            {'header': 'Fällig bis'}
                                                        ]
                                                        })


def write_employees_worksheet(workbook, employee_groups):
    worksheet = workbook.add_worksheet(name='Mitarbeiter')

    data = []
    for eg in employee_groups:
        data_to_write = (
            eg['name'],
            eg['description']
        )
        data.append(data_to_write)

    # Set the columns widths.
    worksheet.set_column('A:B', 25)
    worksheet.add_table('A1:B' + str(len(employee_groups) + 1), {
                                                        'header_row': 1,
                                                        'style': 'Table Style Medium 2',
                                                        'data': data,
                                                        'columns': [
                                                            {'header': 'Abteilung'},
                                                            {'header': 'Besonderheiten (Sprache, Kultur, ...)'}
                                                        ]
                                                        })



def get_employee_groups(project_id):
    db = get_db()
    employees = db.execute(
        'SELECT id, name, description, project_id'
        ' FROM employee_group WHERE project_id = ?', (project_id,)
    ).fetchall()

    return employees


def write_report_tables(worksheet, excel_range_columns, excel_range_data, data_length, write_collection, heading, heading_format):
    data = []
    headers = [
            {'header': 'Name'},
            {'header': 'Beschreibung'}
        ]

    if data_length == 3:
        headers.append({'header': 'Geplant für'})

    for am in write_collection:
        if data_length == 3:
            data_to_write = (
                am['name'],
                am['description'],
                am['due_date'].strftime("%d.%m.%Y") if am['due_date'] is not None else None
            )
        else:
            data_to_write = (
                am['name'],
                am['description']
            )
        data.append(data_to_write)

    worksheet.write(excel_range_columns.split(':')[0] + '1', heading, heading_format)
    # Set the columns widths.
    worksheet.set_column(excel_range_columns, 17)
    worksheet.add_table(excel_range_data, {
        'header_row': 1,
        'style': 'Table Style Medium 2',
        'data': data,
        'columns': headers
    })


def write_report_worksheet(workbook, awarenessmeasures, countermeasures):
    this_month_start = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)
    next_month_start = this_month_start + relativedelta(months=+1)
    two_months_ahead_start = next_month_start + relativedelta(months=+1)

    awarenessmeasures_past = [x for x in awarenessmeasures if
                              x['due_date'] is not None and x['due_date'] < this_month_start]
    awarenessmeasures_this_month = [x for x in awarenessmeasures if
                                    x['due_date'] is not None and x['due_date'] > this_month_start and x[
                                        'due_date'] < next_month_start]
    awarenessmeasures_next_month = [x for x in awarenessmeasures if
                                    x['due_date'] is not None and x['due_date'] > next_month_start and x[
                                        'due_date'] < two_months_ahead_start]
    awarenessmeasures_without_date = [x for x in awarenessmeasures if x['due_date'] is None]
    awarenessmeasures_with_legal_attention = [x for x in awarenessmeasures if
                                              x['needs_legal_attention'] is not None and x[
                                                  'needs_legal_attention'] == 1]


    countermeasures_open = [x for x in countermeasures if
                            x['percentage_executed'] is None or x['percentage_executed'] < 100]


    worksheet = workbook.add_worksheet(name='Auswertungen')

    worksheet.set_column('D:D', 3)
    worksheet.set_column('H:H', 3)
    worksheet.set_column('L:L', 3)
    worksheet.set_column('O:O', 3)
    worksheet.set_column('R:R', 3)
    # Add a heading format to use to highlight cells.
    heading_format = workbook.add_format({'bold': True, 'font_size': 14})

    write_report_tables(worksheet, 'A:C', 'A3:C' + str(len(awarenessmeasures_past) + 4), 3, awarenessmeasures_past, "Awareness Planungen (Vergangenheit)", heading_format)
    write_report_tables(worksheet, 'E:G', 'E3:G' + str(len(awarenessmeasures_this_month) + 4), 3, awarenessmeasures_this_month, "Awareness Planungen (dieser Monat)", heading_format)
    write_report_tables(worksheet, 'I:K', 'I3:K' + str(len(awarenessmeasures_next_month) + 4), 3, awarenessmeasures_next_month, "Awareness Planungen (kommender Monat)", heading_format)

    write_report_tables(worksheet, 'M:N', 'M3:N' + str(len(awarenessmeasures_without_date) + 3), 2, awarenessmeasures_without_date, "Awareness ohne Datum", heading_format)
    write_report_tables(worksheet, 'P:Q', 'P3:Q' + str(len(awarenessmeasures_with_legal_attention) + 3), 2, awarenessmeasures_with_legal_attention, "Rechtliche Abklärungen", heading_format)
    write_report_tables(worksheet, 'S:T', 'S3:T' + str(len(countermeasures_open) + 3), 2, countermeasures_open, "Tech/org offene Themen", heading_format)


@bp.route('/<int:project_id>/export', methods=['GET'])
@login_required
def export_as_excel(project_id):
    calculated_threats = get_threats_of_project_with_subattributes(project_id)

    awarenessmeasures = get_awarenessmeasures_of_project(project_id)
    unique_awa_measures = get_unique_awameasures_of_project(project_id)

    countermeasures_of_project = get_countermeasures_of_project(project_id)
    unique_countermeasures = get_unique_countermeasures_of_project(project_id)

    emp_groups = get_employee_groups(project_id)

    chart_data = []
    colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0',
              '#eee3e7', '#ead5dc', '#eec9d2', '#f4b6c2', '#f6abb6',
              '#4a4e4d', '#0e9aa7', '#3da4ab', '#f6cd61', '#fe8a71',
              '#fe9c8f', '#feb2a8', '#fec8c1', '#fad9c1', '#f9caa7',
              '#ee4035', '#f37736', '#fdf498', '#7bc043', '#0392cf',
              '#eeeeee', '#dddddd', '#cccccc', '#bbbbbb', '#aaaaaa',
              '#96ceb4', '#ffeead', '#ff6f69', '#ffcc5c', '#88d8b0',
              '#4b3832', '#854442', '#fff4e6', '#3c2f2f', '#be9b7b']

    for threat in calculated_threats:
        x = {
            'bgColor': colors.pop(),
            'label': threat["name"],
            'r': 20,
            'x': int(sum([y["percentage_executed"] for y in threat["awarenessmeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["awarenessmeasures"])) if len(threat["awarenessmeasures"]) > 0 else 0,
            'y': int(sum([y["percentage_executed"] for y in threat["countermeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["countermeasures"])) if len(threat["countermeasures"]) > 0 else 0
        }

        chart_data.append(x)

    session['selected_project'] = project_id

    filename = str(uuid.uuid4()) + ".xlsx"
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/" + filename
    workbook = xlsxwriter.Workbook(path)

    write_report_worksheet(workbook, unique_awa_measures, unique_countermeasures)
    write_dashboard_worksheet(workbook, calculated_threats)
    write_threat_worksheet(workbook, calculated_threats)
    write_countermeasures_worksheet(workbook, countermeasures_of_project)
    write_awarenessmeasures_worksheet(workbook, awarenessmeasures)
    write_employees_worksheet(workbook, emp_groups)

    workbook.close()

    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/" + filename
    file_handle = open(path, 'rb')
    # This *replaces* the `remove_file` + @after_this_request code above
    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(path)

    return current_app.response_class(
        stream_and_remove_file(),
        headers={'Content-Disposition': 'attachment; filename="export.xlsx"'}
    )

@bp.route('/<int:project_id>', methods=['GET'])
@login_required
def details(project_id):
    calculated_threats = get_threats_of_project_with_subattributes(project_id)

    countermeasures_of_project = get_unique_countermeasures_of_project(project_id)
    countermeasures_open = [x for x in countermeasures_of_project if x['percentage_executed'] is None or x['percentage_executed'] < 100]

    chart_data = []
    colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0',
              '#eee3e7', '#ead5dc', '#eec9d2', '#f4b6c2', '#f6abb6',
              '#4a4e4d', '#0e9aa7', '#3da4ab', '#f6cd61', '#fe8a71',
              '#fe9c8f', '#feb2a8', '#fec8c1', '#fad9c1', '#f9caa7',
              '#ee4035', '#f37736', '#fdf498', '#7bc043', '#0392cf',
              '#eeeeee', '#dddddd', '#cccccc', '#bbbbbb', '#aaaaaa',
              '#96ceb4', '#ffeead', '#ff6f69', '#ffcc5c', '#88d8b0',
              '#4b3832', '#854442', '#fff4e6', '#3c2f2f', '#be9b7b']

    for threat in calculated_threats:
        x = {
            'bgColor': colors.pop(),
            'label': threat["name"],
            'r': 20,
            'x': int(sum([y["percentage_executed"] for y in threat["awarenessmeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["awarenessmeasures"])) if len(threat["awarenessmeasures"]) > 0 else 0,
            'y': int(sum([y["percentage_executed"] for y in threat["countermeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["countermeasures"])) if len(threat["countermeasures"]) > 0 else 0
        }

        chart_data.append(x)

    session['selected_project'] = project_id

    return render_template('project/details.html',
                           project=get_project(project_id), calculated_threats=calculated_threats,
                           countermeasures_open=countermeasures_open,
                           chart_data=chart_data
                           )


@bp.route('/<int:project_id>/awa_dashboard', methods=['GET'])
@login_required
def awareness_dashboard(project_id):
    calculated_threats = get_threats_of_project_with_subattributes(project_id)

    this_month_start = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)
    next_month_start = this_month_start + relativedelta(months=+1)
    two_months_ahead_start = next_month_start + relativedelta(months=+1)

    awarenessmeasures = get_unique_awameasures_of_project(project_id)
    awarenessmeasures_past = [x for x in awarenessmeasures if x['due_date'] is not None and x['due_date'] < this_month_start]
    awarenessmeasures_this_month = [x for x in awarenessmeasures if x['due_date'] is not None and x['due_date'] > this_month_start and x['due_date'] < next_month_start]
    awarenessmeasures_next_month = [x for x in awarenessmeasures if x['due_date'] is not None and x['due_date'] > next_month_start and x['due_date'] < two_months_ahead_start]
    awarenessmeasures_without_date = [x for x in awarenessmeasures if x['due_date'] is None]
    awarenessmeasures_with_legal_attention = [x for x in awarenessmeasures if x['needs_legal_attention'] is not None and (x['needs_legal_attention'] == 1 or x['needs_legal_attention'] is True)]

    session['selected_project'] = project_id



    chart_data = []
    colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0',
              '#eee3e7', '#ead5dc', '#eec9d2', '#f4b6c2', '#f6abb6',
              '#4a4e4d', '#0e9aa7', '#3da4ab', '#f6cd61', '#fe8a71',
              '#fe9c8f', '#feb2a8', '#fec8c1', '#fad9c1', '#f9caa7',
              '#ee4035', '#f37736', '#fdf498', '#7bc043', '#0392cf',
              '#eeeeee', '#dddddd', '#cccccc', '#bbbbbb', '#aaaaaa',
              '#96ceb4', '#ffeead', '#ff6f69', '#ffcc5c', '#88d8b0',
              '#4b3832', '#854442', '#fff4e6', '#3c2f2f', '#be9b7b']

    for threat in calculated_threats:
        x = {
            'bgColor': colors.pop(),
            'label': threat["name"],
            'r': 20,
            'x': int(sum([y["percentage_executed"] for y in threat["awarenessmeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["awarenessmeasures"])) if len(threat["awarenessmeasures"]) > 0 else 0,
            'y': int(sum([y["percentage_executed"] for y in threat["countermeasures"] if
                          y["percentage_executed"] is not None]) / len(
                threat["countermeasures"])) if len(threat["countermeasures"]) > 0 else 0
        }

        chart_data.append(x)

    return render_template('project/awareness_dashboard.html',
                           project=get_project(project_id),
                           awarenessmeasures_past=awarenessmeasures_past,
                           awarenessmeasures_this_month=awarenessmeasures_this_month,
                           awarenessmeasures_next_month=awarenessmeasures_next_month,
                           awarenessmeasures_without_date=awarenessmeasures_without_date,
                           awarenessmeasures_with_legal_attention=awarenessmeasures_with_legal_attention,
                           chart_data=chart_data
                           )