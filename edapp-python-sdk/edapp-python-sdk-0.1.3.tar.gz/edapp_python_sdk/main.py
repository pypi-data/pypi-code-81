import datetime
import sys

import dateutil.relativedelta as rd
import numpy as np
from dateutil.parser import parse

import xlsxwriter
import xlsxwriter.utility

from edapp_python_sdk import edapppy
import pandas as pd
import sqlite3
import configparser
import os
from .sql_models import *

db_name = "edapp.db"
export_folder = "exports"


def create_export_folder():
    if not os.path.exists(f"./{export_folder}"):
        os.mkdir(export_folder)


def check_for_db():
    create_export_folder()
    path = os.path.join(export_folder, db_name)

    return sqlite3.connect(path)


def setup_sqlite(table_name, column_names, values, drop=False):
    conn = check_for_db()
    cur = conn.cursor()
    if drop:
        cur.execute(f"""DROP TABLE if exists {table_name}""")
    cur.execute(f"""CREATE TABLE if not exists {table_name} {column_names}""")
    for row in values:
        cur.execute(f"INSERT OR REPLACE INTO {table_name} VALUES {row}")
    conn.commit()
    conn.close()


def export_to_csv(df, file_name):
    if not os.path.exists(f"./{export_folder}"):
        os.mkdir(export_folder)

    df.to_csv(
        os.path.join(export_folder, f"{file_name}.csv"),
        encoding="utf-8-sig",
        index=False,
    )


def convert_to_records(df, table=None):
    if table:
        if table == "lessonprogress":
            df.insert(
                0,
                "id",
                df["userId"]
                + "_"
                + df["courseId"]
                + "_"
                + df["lessonId"]
                + "_"
                + (
                    pd.to_datetime(df["eventDateTime"]).values.astype(np.int64)
                    // 10 ** 6
                ).astype(str),
            )
        elif table == "courseprogress":
            df.insert(0, "id", df["userId"] + "_" + df["courseId"])

    # Add a column of the last time we did an export
    df["last_export"] = datetime.datetime.now()
    df = df.fillna(value="")
    records = df.to_records(index=False)

    return records


def ensure_table_exists(cur, table):
    column_names = table + "_sql"

    # Create table
    cur.execute(
        f"""CREATE TABLE if not exists {table}
                   {globals()[column_names]}"""
    )


def get_table_rows(cur, table):
    rows = cur.execute(f"SELECT * FROM {table};")
    list_of_rows = list(rows)
    if rows:
        columns = [description[0] for description in rows.description]
        return list_of_rows, columns
    else:
        return None


def df_to_dict(data, columns):
    df = to_dataframe(data, columns=columns)
    export = df_to_dictionary(df)

    return export


def database_or_export(cur, table):
    ensure_table_exists(cur, table)
    rows, cols = get_table_rows(cur, table)
    if rows:
        export = df_to_dict(rows, cols)
        if table == "lessonprogress":
            possible_dates = [x["eventDateTime"] for x in export]
        else:
            possible_dates = [x["last_export"] for x in export]
        last_export = max(possible_dates)
        last_export = parse(last_export)
        if table not in [
            "surveyanswers",
            "attempts",
            "courseprogress",
            "lessonprogress",
        ]:
            one_week_ago = datetime.datetime.today() - rd.relativedelta(hours=24)
            if last_export < one_week_ago:
                print(
                    f"Table '{table}' has not been updated in the last 24 hours, updating."
                )
                return None, None, None
        return export, cols, last_export

    else:
        return None, None, None


def export_reference_tables(ea, include_lessons):
    conn = check_for_db()
    cur = conn.cursor()

    # Users
    users, user_cols, last_export = database_or_export(cur, "users")
    custom_fields, custom_field_cols, last_export = database_or_export(
        cur, "custom_fields"
    )
    user_groups, user_group_cols, last_export = database_or_export(cur, "usergroups")
    if not user_groups:
        user_groups = ea.get_user_groups()
        df_groups = to_dataframe(user_groups)
        export_to_csv(df_groups, "usergroups")
        setup_sqlite(
            "usergroups", usergroups_sql, convert_to_records(df_groups), drop=True
        )
        if user_groups:
            groups_with_children = [x for x in user_groups if x["hasChildren"] is True]
            if groups_with_children:
                user_child_groups = ea.get_child_user_groups(groups_with_children)
                df_child_groups = to_dataframe(user_child_groups)
                export_to_csv(df_groups, "usergroup_children")
                setup_sqlite(
                    "usergroup_children",
                    user_children_sql,
                    convert_to_records(df_child_groups),
                    drop=True,
                )

    if not users or not custom_fields:
        users, custom_fields, user_groups = ea.discover_users()
        df_users = to_dataframe(users)
        df_users = df_users.drop(columns=["customFields", "userGroups"])
        export_to_csv(df_users, "users")
        setup_sqlite("users", users_sql, convert_to_records(df_users), drop=True)

        df_custom_fields = to_dataframe(custom_fields)
        export_to_csv(df_custom_fields, "custom_fields")
        setup_sqlite(
            "custom_fields",
            custom_fields_sql,
            convert_to_records(df_custom_fields),
            drop=True,
        )
        df_user_groups = to_dataframe(user_groups)
        export_to_csv(df_user_groups, "group_users")
        setup_sqlite(
            "group_users",
            group_users_sql,
            convert_to_records(df_user_groups),
            drop=True,
        )

    # Courses
    courses, course_cols, last_export = database_or_export(cur, "courses")
    if not courses:
        courses = ea.discover_courses()
        df_courses = to_dataframe(courses)
        export_to_csv(df_courses, "courses")
        setup_sqlite("courses", course_sql, convert_to_records(df_courses), drop=True)

    # Lessons
    lessons, lesson_cols, last_export = database_or_export(cur, "lessons")
    if not lessons:
        lessons = ea.discover_lessons(courses)
        df_lessons = to_dataframe(lessons)
        export_to_csv(df_lessons, "lessons")
        setup_sqlite("lessons", lessons_sql, convert_to_records(df_lessons), drop=True)

    # Analytics
    survey_answers = export_analytics(ea, cur, "surveyanswers", "surveyanswers_sql")
    attempts = export_analytics(ea, cur, "attempts", "attempts_sql")
    courseprogress = export_analytics(ea, cur, "courseprogress", "courseprogress_sql")
    coursestatistics = export_analytics(
        ea, cur, "coursestatistics", "coursestatistics_sql"
    )
    if include_lessons is True:
        lesson_progress = export_analytics(
            ea, cur, "lessonprogress", "lessonprogress_sql"
        )
    else:
        lesson_progress = None

    return {
        "users": users,
        "custom_fields": custom_fields,
        "courses": courses,
        "lessons": lessons,
        "survey_answers": survey_answers,
        "attempts": attempts,
        "courseprogress": courseprogress,
        "coursestatistics": coursestatistics,
        "lesson_progress": lesson_progress,
    }


def export_analytics(ea, cur, to_export, sql_table):
    data, cols, last_export = database_or_export(cur, to_export)
    updated_data = ea.discover_analytics(to_export, startdatetime=last_export)
    if updated_data:
        df = to_dataframe(updated_data)
        if to_export in ["coursestatistics"]:
            drop = True
        else:
            drop = False
        setup_sqlite(
            to_export,
            globals()[sql_table],
            convert_to_records(df, table=to_export),
            drop=drop,
        )
        data, cols, last_export = database_or_export(cur, to_export)
    df = to_dataframe(data)
    export_to_csv(df, to_export)

    return data


def to_dataframe(export, columns=None):
    if columns:
        return pd.DataFrame(export, columns=columns)
    else:
        return pd.DataFrame(export)


def df_to_dictionary(df):
    return df.to_dict("records")


def format_survey_data(survey_answers, users, courses, lessons):
    user_ids = []
    question_ids = []
    user_names = []
    [
        user_ids.append(x["userId"])
        for x in survey_answers
        if x["userId"] not in user_ids
    ]
    for u in user_ids:
        [user_names.append(x["email"]) for x in users if x["id"] == u]

    user_ref_dict = dict(zip(user_ids, user_names))

    [
        question_ids.append(x["questionId"])
        for x in survey_answers
        if x["questionId"] not in question_ids
    ]

    csv_header = list(survey_answers[0].keys())

    for u in user_ids:
        csv_header.append(u)

    formatted_csv = []
    for q in question_ids:
        relevant_responses = [x for x in survey_answers if x["questionId"] == q]
        new_row = relevant_responses[0]

        # Change the lesson IDs into the lesson name
        lesson_names = join_multiple_entries(relevant_responses, lessons, "lessonId")
        if lesson_names:
            new_row["lessonId"] = lesson_names

        # Create a comma separated list of the course names (useful if the course has been translated.)
        course_names = join_multiple_entries(relevant_responses, courses, "courseId")
        if course_names:
            new_row["courseId"] = course_names

        questions = join_multiple_entries(
            relevant_responses, "questions", "questionContent"
        )
        if questions:
            new_row["questionContent"] = questions

        for u in user_ids:
            user_response = [x for x in relevant_responses if x["userId"] == u]
            if user_response:
                # For this report, it's very likely that a user will have completed it more than once. As a result,
                # we'll grab the most recent response to display in the column.

                answer_dates = [x["answeredDateTime"] for x in user_response]
                most_recent_date = max(answer_dates)
                most_recent_response = [
                    x
                    for x in user_response
                    if x["answeredDateTime"] == most_recent_date
                ]
                user_response = most_recent_response[0]["answerContent"]
            else:
                user_response = None
            new_row[u] = user_response

        if new_row:
            formatted_csv.append(new_row)

    return formatted_csv, user_ref_dict


def join_multiple_entries(relevant_responses, source, col_id):
    list_of_ids = []
    [
        list_of_ids.append(x[col_id])
        for x in relevant_responses
        if x[col_id] not in list_of_ids
    ]
    names_col = []
    for item_id in list_of_ids:
        if source == "questions":
            names_col.append(item_id)
        else:
            name = [x for x in source if x["id"] == item_id]
            names_col.append(name[0]["title"])
    if len(names_col) > 1:
        names = ",\n\n".join(names_col)
    elif names_col:
        names = names_col[0]
    else:
        names = None

    return names


def surveys_to_excel(survey_data, user_ref_dict):
    df_survey_answers = pd.DataFrame(survey_data)
    df_survey_answers = df_survey_answers.rename(columns=user_ref_dict)

    df_survey_answers = df_survey_answers.drop(
        columns=[
            "id",
            "lessonExternalId",
            "courseExternalId",
            "slideId",
            "userId",
            "userExternalId",
            "attemptId",
            "questionId",
            "answerDefinitionId",
            "answerContent",
            "answeredDateTime",
            "last_export",
        ]
    )

    file_name = "survey_export"
    file_name = os.path.join(export_folder, f"{file_name}")
    workbook = xlsxwriter.Workbook("{}.xlsx".format(file_name))
    worksheet = workbook.add_worksheet("Surveys")
    worksheet.activate()

    template_as_list = df_survey_answers.values.tolist()
    columns_as_list = df_survey_answers.columns.values.tolist()

    fixed_template_as_list = []
    for values in template_as_list:
        fixed = [x.replace("\\n\\n", "\n") for x in values if x is not None]
        fixed_template_as_list.append(fixed)

    template_as_list = fixed_template_as_list

    # wrap_format = workbook.add_format({"text_wrap": 1})
    wrap_format = workbook.add_format()
    wrap_format.set_text_wrap()

    reformatted_columns = []
    for column in columns_as_list:
        current_row = {"header": column, "header_format": wrap_format}
        reformatted_columns.append(current_row)

    last_col = len(columns_as_list) - 1
    last_col_letter = xlsxwriter.utility.xl_col_to_name(last_col)

    table_length = len(template_as_list)

    worksheet.set_column(f"A1:{last_col_letter}", 25, wrap_format)
    worksheet.add_table(
        f"A1:{last_col_letter}{table_length}",
        {
            "data": template_as_list,
            "columns": reformatted_columns,
            "banded_rows": 0,
            "banded_columns": 1,
        },
    )
    workbook.close()


def write_new_config(config):
    config["TOKENS"] = {"edapp": "YOUR TOKEN HERE"}
    config["SETTINGS"] = {"start_date": "2021-01-01", "include_lesson_progress": False}
    config.write(open("config.ini", "w"))
    print(
        "Created new config file, please update with your API token and re-run the tool."
    )
    sys.exit()


def get_config():
    config = configparser.ConfigParser()
    if not os.path.isfile("config.ini"):
        write_new_config(config)
    else:
        config.read("config.ini")
        if ["TOKENS", "SETTINGS"] != config.sections():
            write_new_config(config)
        else:
            ea_api_key = config["TOKENS"]["edapp"]

    start_date = parse(config["SETTINGS"]["start_date"])
    include_lesson_progress = config["SETTINGS"]["include_lesson_progress"]

    return {
        "ea": edapppy.EdApp(ea_api_key, start_date),
        "lessons": include_lesson_progress,
    }


def export_survey_report():
    all_results = export_all()
    survey_data, user_ref_dict = format_survey_data(
        all_results["survey_answers"],
        all_results["users"],
        all_results["courses"],
        all_results["lessons"],
    )
    surveys_to_excel(survey_data, user_ref_dict)


def create_new_groups():
    ea = get_config()
    ea = ea["ea"]
    existing_groups = ea.get_user_groups()
    list_of_groups = []
    for group in list_of_groups:
        check_for_existing_group = [x for x in existing_groups if x["name"] == group]
        if check_for_existing_group:
            print("Group already exists, skipping.")
        if not check_for_existing_group:
            ea.create_group(group)


def edapp_export():
    all_results = export_all()
    if all_results:
        print('Export complete.')
    else:
        print('Nothing to export')


def export_all():
    ea = get_config()
    include_lessons = ea["lessons"]
    include_lessons = True if include_lessons.lower() == "true" else False
    ea = ea["ea"]
    # users, custom_fields, courses, lessons, survey_answers, attempts
    all_results = export_reference_tables(ea, include_lessons)

    return all_results
