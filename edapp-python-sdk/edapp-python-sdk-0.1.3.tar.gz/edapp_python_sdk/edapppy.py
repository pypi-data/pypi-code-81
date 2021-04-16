import collections
import json
import sys

import html2text
import requests
import logging
import os
import re
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import errno
from tqdm import tqdm
import time
from random import randint

HTTP_USER_AGENT_ID = "edapp-python-sdk"


class EdApp:
    def __init__(self, api_token, start_date):
        self.current_dir = os.getcwd()
        self.log_dir = self.current_dir + "/log/"
        self.start_date = start_date

        # Root URLs
        self.api_url = "https://rest.edapp.com"
        self.catalog_url = self.api_url + "/v2/catalog"
        self.analytics_url = self.api_url + "/v2/analytics"

        # Users
        self.users = self.api_url + "/v2/users"
        self.user_groups = self.api_url + "/v2/usergroups"

        # Catalog
        self.course_collections = self.catalog_url + "/courseCollections"
        self.courses = self.catalog_url + "/courses"

        # Analytics
        self.survey_answers = self.analytics_url + "/surveyanswers"
        self.survey_definitions = self.analytics_url + "/surveyquestiondefinitions"
        self.attempts = self.analytics_url + "/attempts"
        self.courseProgress = self.analytics_url + "/courseprogress"
        self.courseStatistics = self.analytics_url + "/coursestatistics"
        self.lessonProgressEvents = self.analytics_url + "/lesson-progress/events"
        self.lessonStatistics = self.analytics_url + "/lessonstatistics"

        self.create_directory_if_not_exists(self.log_dir)
        self.configure_logging()
        self.api_token = api_token
        logger = logging.getLogger(__name__)
        if self.api_token:
            self.custom_http_headers = {
                "User-Agent": HTTP_USER_AGENT_ID,
                "Authorization": "Bearer " + self.api_token,
            }
        else:
            logger.error("No valid API token parsed! Exiting.")
            sys.exit(1)

    def authenticated_request_get(self, url):
        return requests.get(url, headers=self.custom_http_headers)

    def authenticated_request_post(self, url, data):
        self.custom_http_headers["content-type"] = "application/json"
        response = requests.post(url, data, headers=self.custom_http_headers)
        del self.custom_http_headers["content-type"]
        return response

    def authenticated_request_put(self, url, data):
        self.custom_http_headers["content-type"] = "application/json"
        response = requests.put(url, data, headers=self.custom_http_headers)
        del self.custom_http_headers["content-type"]
        return response

    def authenticated_request_delete(self, url):
        return requests.delete(url, headers=self.custom_http_headers)

    @staticmethod
    def parse_json(json_to_parse):
        """
        Parse JSON string to OrderedDict and return
        :param json_to_parse:  string representation of JSON
        :return:               OrderedDict representation of JSON
        """
        return json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(
            json_to_parse.decode("utf-8")
        )

    @staticmethod
    def log_critical_error(ex, message):
        """
        Write exception and description message to log

        :param ex:       Exception instance to log
        :param message:  Descriptive message to describe exception
        """
        logger = logging.getLogger("ea_logger")

        if logger is not None:
            logger.critical(message)
            logger.critical(ex)

    def configure_logging(self):
        """
        Configure logging to log to std output as well as to log file
        """
        log_level = logging.INFO

        log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
        ea_logger = logging.getLogger(__name__)
        ea_logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")

        fh = logging.FileHandler(filename=self.log_dir + log_filename)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        ea_logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(log_level)
        sh.setFormatter(formatter)
        ea_logger.addHandler(sh)

    def create_directory_if_not_exists(self, path):
        """
        Creates 'path' if it does not exist

        If creation fails, an exception will be thrown

        :param path:    the path to ensure it exists
        """
        try:
            os.makedirs(path)
        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                self.log_critical_error(
                    ex, "An error happened trying to create " + path
                )
                raise

    def discover_analytics(
        self,
        to_export,
        courseid=None,
        courseexternalid=None,
        lessonid=None,
        lessonexternalid=None,
        userid=None,
        userexternalid=None,
        startdatetime=None,
        enddatetime=None,
        page=1,
        pagesize=1000,
    ):

        # Write out the arguments passed to the function
        func_args = locals().items()

        logger = logging.getLogger("ea_logger")

        result_count = None

        total_results = []

        if to_export == "surveyanswers":
            search_url = self.survey_answers
        elif to_export == "surveydefinitions":
            search_url = self.survey_definitions
        elif to_export == "attempts":
            search_url = self.attempts
        elif to_export == "courseprogress":
            search_url = self.courseProgress
        elif to_export == "coursestatistics":
            search_url = self.courseStatistics
        elif to_export == "lessonprogress":
            search_url = self.lessonProgressEvents
        else:
            logger.error(f"{to_export} is not defined.")
            sys.exit()

        search_url = search_url + "?"

        # Append any additional arguments to the URL
        for k, v in func_args:
            if v and k not in ["self", "to_export", "page", "pagesize"]:
                search_url += f"&{k}={v}"
        if to_export == "lessonprogress":
            if startdatetime:
                total_results = self.get_all_lesson_events(
                    start_date_time=startdatetime
                )
            else:
                total_results = self.get_all_lesson_events()
        else:
            total_results = self.get_all_results(search_url, to_export)

        if to_export == "surveyanswers":
            for survey in total_results:
                for k, v in survey.items():
                    if k == "questionContent":
                        cleaned_v = html2text.html2text(v)
                        survey[k] = cleaned_v.strip()

        return total_results

    def get_all_lesson_events(self, start_date_time=None):
        if not start_date_time:
            start_date_time = self.start_date
        start_date_time_str = start_date_time.strftime("%Y-%m-%dT%H:%M:%S+0")
        start_date_time = parse(start_date_time_str)
        now_plus_7 = datetime.now(timezone.utc)
        now_plus_7 = now_plus_7 + timedelta(days=7)
        all_lesson_events = []
        while start_date_time < now_plus_7:
            max_date_time = start_date_time + timedelta(days=7)
            max_date_time_str = max_date_time.strftime("%Y-%m-%dT%H:%M:%S")
            start_date_time_str = start_date_time.strftime("%Y-%m-%dT%H:%M:%S")
            current_url = f"{self.lessonProgressEvents}?&page=1&pagesize=1000&mineventdatetime={start_date_time_str}&maxeventdatetime={max_date_time_str}"
            all_lesson_events.extend(
                self.get_all_results(current_url, "lessonprogress")
            )
            start_date_time = max_date_time

        return all_lesson_events if all_lesson_events else None

    def get_all_results(
        self,
        search_url,
        to_export,
        page=1,
        pagesize=1000,
        startdatetime="2000-01-01T00:00:00.000Z",
    ):
        logger = logging.getLogger("ea_logger")
        result_count = None
        total_results = []
        if "?" not in search_url:
            if search_url.endswith("/"):
                search_url = search_url[:-1]
            search_url = search_url + "?"
        while result_count != 0:
            current_url = f"{search_url}&page={page}&pagesize={pagesize}"

            log_string = f"\nDownloading {to_export}: " + "\n"
            log_string += "modifiedsince = " + str(startdatetime) + "\n"
            log_string += "page          = " + str(page) + "\n"
            log_string += "page size     = " + str(pagesize) + "\n"
            logger.info(log_string)
            print(current_url)
            response = self.authenticated_request_get(current_url)
            result = (
                response.json() if response.status_code == requests.codes.ok else None
            )
            number_discovered = str(result["totalCount"]) if result is not None else "0"
            log_message = (
                f"on {to_export}: "
                + number_discovered
                + " discovered using "
                + search_url
            )

            self.log_http_status(response.status_code, log_message)

            total_count = result["totalCount"]
            result = result["items"]
            result_count = len(result)
            if total_count == result_count:
                result_count = 0
            total_results.extend(result)
            page += 1

        return total_results

    def discover_lessons(self, courses):
        if courses:
            list_of_courses = self.list_dict_or_str(courses, dict_key="id")
            compiled_list = self.get_results(list_of_courses, self.courses, "lessons")
        else:
            compiled_list = None

        return compiled_list

    @staticmethod
    def list_dict_or_str(item, dict_key=None):
        if type(item) == list:
            if type(item[0]) == dict and dict_key:
                returned_list = []
                [returned_list.append(x[dict_key]) for x in item]
            else:
                returned_list = item
        else:
            returned_list = [item]

        return returned_list

    def get_results(self, list_of_items, url, item):
        compiled_list = []
        progress_bar = tqdm(list_of_items)
        for c in progress_bar:
            search_url = url + f"/{c}/{item}"
            progress_bar.set_description(f"Getting {item} from ID {c}")
            response = self.authenticated_request_get(search_url)
            result = (
                response.json() if response.status_code == requests.codes.ok else None
            )
            progress_bar.set_description(f"Found {len(result)} {item} in {c}")
            if result:
                if item == "lessons":
                    result = [dict(item, **{"courseId": c}) for item in result]
                compiled_list.extend(result)

        return compiled_list

    def get_user(self, user_id):
        search_url = self.users + f"/{user_id}"
        response = self.authenticated_request_get(search_url)
        result = response.json() if response.status_code == requests.codes.ok else None

        return result

    def get_user_groups(self):
        search_url = self.user_groups + "?"
        return self.get_all_results(search_url, "usergroups")

    def get_child_user_groups(self, group_id):
        if type(group_id) == list:
            all_child_groups = []
            for group in group_id:
                search_url = self.user_groups + "/" + group["id"] + "/children?"
                result = self.get_all_results(search_url, "children")
                add_group = [
                    dict(item, **{"parentGroupId": group["id"]}) for item in result
                ]
                all_child_groups.extend(add_group)

            return all_child_groups if all_child_groups else None
        else:
            search_url = self.user_groups + group_id + "/children?"
            result = self.get_all_results(search_url, "children")
            if result:
                return [dict(item, **{"parentGroupId": group_id}) for item in result]
            else:
                return None

    def get_users_in_group(self, group_id):
        if type(group_id) == list:
            all_group_users = []
            for group in group_id:
                search_url = self.user_groups + "/" + group["id"] + "/users?"
                all_group_users.extend(self.get_all_results(search_url, "usersgroups"))
            result = all_group_users if all_group_users else None
        else:
            search_url = self.user_groups + group_id + "/users"
            response = self.authenticated_request_get(search_url)
            result = (
                response.json() if response.status_code == requests.codes.ok else None
            )

        return result

    def discover_users(self):
        search_url = self.users + "?"
        list_of_users = self.get_all_results(search_url, to_export="users")
        custom_fields = []
        user_groups = []
        for user in list_of_users:
            user_id = user["id"]
            user_email = user["email"]
            for k, v in user.items():
                if k == "userGroups":
                    if v:
                        for y in v:
                            if "," in y:
                                y.split(",")
                                for line in y:
                                    new_row = {"user_id": user_id, "group_id": line}
                                    user_groups.append(new_row)
                            else:
                                new_row = {"user_id": user_id, "group_id": y}
                                user_groups.append(new_row)
                if k == "customFields":
                    if v != {}:
                        for x, y in v.items():
                            if y:
                                field_title = "custom_" + x
                                new_row = {
                                    "user_id": user_id,
                                    "user_email": user_email,
                                    "custom_field": field_title,
                                    "custom_value": y,
                                }
                                custom_fields.append(new_row)
                if type(v) == list:
                    if not v:
                        user[k] = None
                    else:
                        user[k] = ",".join(v)

        return list_of_users, custom_fields, user_groups

    def discover_courses(self):
        return self.get_all_results(self.courses, to_export="courses")

    def create_group(self, group, invite_code=None):
        if not invite_code:
            invite_name = re.sub("[^A-Za-z0-9]+", "_", group)
            invite_code = invite_name + "_" + str(randint(11111, 99999))
        request = {"name": group, "inviteCode": invite_code.lower()}

        response = self.authenticated_request_post(
            self.user_groups, json.dumps(request)
        )
        result = response.json() if response.status_code == requests.codes.ok else None

        return result

    @staticmethod
    def log_http_status(status_code, message):
        """
        Write http status code and descriptive message to log

        :param status_code:  http status code to log
        :param message:      to describe where the status code was obtained
        """
        logger = logging.getLogger("ea_logger")
        status_description = requests.status_codes._codes[status_code][0]
        log_string = (
            str(status_code)
            + " ["
            + status_description
            + "] status received "
            + message
        )
        logger.info(log_string) if status_code == requests.codes.ok else logger.error(
            log_string
        )
