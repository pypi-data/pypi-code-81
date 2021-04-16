import json

import requests

from .cli_constants import CliConstants


class ZephyrService:
    def __init__(self, zephyr_configurer):
        self.zephyr_config = zephyr_configurer.get_config()
        self.jira_url = self.zephyr_config.get(CliConstants.JIRA_URL.value)
        self.username = self.zephyr_config.get(CliConstants.USERNAME.value)
        self.password = self.zephyr_config.get(CliConstants.PASSWORD.value)
        self.project_key = self.zephyr_config.get(CliConstants.PROJECT_KEY.value)
        self.cycle_name = self.zephyr_config.get(CliConstants.TEST_CYCLE.value)
        self.folder_name = self.zephyr_config.get(CliConstants.FOLDER_NAME.value)
        self.version_name = self.zephyr_config.get(CliConstants.RELEASE_VERSION.value)
        self.single_update_uri = 'zapi/latest/execution/{}/execute'
        self.auth = (self.username, self.password)

    def get_zephyr_config(self):
        return self.zephyr_config

    def get_issue_by_key(self, issue_key):
        url = self.jira_url + "api/2/issue/" + issue_key

        print(f"Get {url}")
        resp = requests.get(url, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)

        return resp.json()['id']

    def create_new_execution(self, issue_id, zephyr_meta_info):
        url = self.jira_url + "zapi/latest/execution"

        headers = {'content-type': 'application/json'}
        post_data = json.dumps({
            "cycleId": zephyr_meta_info.get("cycleId"),
            "projectId": zephyr_meta_info.get("projectId"),
            "versionId": zephyr_meta_info.get("versionId"),
            "assigneeType": "assignee",
            "assignee": self.zephyr_config.get(CliConstants.USERNAME.value),
            "folderId": zephyr_meta_info.get("folderId"),
            "issueId": issue_id
        })

        print(f"Post {url} with data {post_data}")
        resp = requests.post(url, data=post_data, headers=headers, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)

        keys = resp.json().keys()

        return list(keys)[0]

    def update_execution(self, issue_key, status_number, comment=None):
        issue_id = self.get_issue_by_key(issue_key)

        url = self.jira_url + self.single_update_uri.format(str(issue_id))

        if comment is None:
            data = json.dumps({"status": status_number})
        else:
            data = json.dumps({
                "status": status_number,
                "comment": comment
            })
        headers = {'content-type': 'application/json'}

        print(f"Put {url} with data {data}")
        resp = requests.put(url, headers=headers, data=data, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)

    def get_project_id_by_key(self, project_key=None):
        if project_key is not None:
            p_key = project_key
        else:
            p_key = self.project_key

        url = self.jira_url + 'api/2/project/' + p_key
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        print(f"Get {url}")
        project = requests.get(url, headers=headers, auth=self.auth)
        return project.json()['id']

    def get_version_for_project_id(self, version_name=None, project_id=None):
        if version_name is not None:
            v_name = version_name
        else:
            v_name = self.version_name

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_id_by_key(self.project_key)

        url = self.jira_url + 'zapi/latest/util/versionBoard-list?projectId=' + p_id

        headers = {'accept': 'application/json'}

        print(f"Get {url}")
        project = requests.get(url, headers=headers, auth=self.auth)
        for version in project.json()['unreleasedVersions']:
            if version['label'] == v_name:
                return version['value']

    def create_test_cycle(self, cycle_name, version_id=None, project_id=None, description=None):
        url = self.jira_url + 'zapi/latest/cycle'

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.self.get_version_for_project_id()

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_id_by_key(self.project_key)

        headers = {'content-type': 'application/json'}
        post_data = json.dumps({
            "clonedCycleId": "",
            "name": cycle_name,
            "build": "",
            "environment": "",
            "description": description,
            "projectId": p_id,
            "versionId": v_id
        })

        print(f"Post {url} with data {post_data}")
        resp = requests.post(url, data=post_data, headers=headers, auth=self.auth)

        return resp.json()['id']

    def get_cycle_id(self, cycle_name=None, project_id=None, version_id=None):
        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_id_by_key(self.project_key)

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.get_version_for_project_id()

        url = self.jira_url + 'zapi/latest/cycle?projectId=' + p_id + '&versionId=' + v_id
        print(f"Get {url}")
        resp = requests.get(url, auth=self.auth)
        if cycle_name is not None:
            c_name = cycle_name
        else:
            c_name = self.cycle_name
        for key, value in resp.json().items():
            try:
                if c_name.strip() == value['name'].strip():
                    return key
            except Exception as e:
                raise Exception(f'Cycle name not found {e.__str__()}')

    def delete_folder_from_cycle(self, folder_id=None, project_id=None, version_id=None, cycle_id=None):
        if folder_id is not None:
            f_id = folder_id
        else:
            f_id = self.get_folder_id()

        if cycle_id is not None:
            c_id = cycle_id
        else:
            c_id = self.get_cycle_id(self.cycle_name)

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_id_by_key()

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.get_version_for_project_id()

        delete_data = {
            "versionId": v_id,
            "cycleId": c_id,
            "projectId": p_id
        }
        headers = {'content-type': 'application/json'}
        url = self.jira_url + f"zapi/latest/folder/{f_id}"

        print(f"Delete {url} with query params {delete_data}")
        resp = requests.delete(url, params=delete_data, headers=headers, auth=self.auth)
        if resp.status_code != 200:
            raise Exception(f'Could not delete folder id {folder_id} for versionId: {version_id}, cycleId: {cycle_id}, '
                            f'projectId: {project_id}\nResponse: {resp.text}')

    def get_folder_id(self, cycle_id=None, project_id=None, version_id=None, folder_name=None):
        if cycle_id is not None:
            c_id = cycle_id
        else:
            c_id = self.get_cycle_id(self.cycle_name)

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_id_by_key()

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.get_version_for_project_id()

        url = self.jira_url + 'zapi/latest/cycle/' + c_id + '/folders?projectId=' + p_id + '&versionId=' + v_id

        if folder_name:
            f_name = folder_name
        else:
            f_name = self.folder_name

        print(f"Get {url}")
        resp = requests.get(url, auth=self.auth)
        for folder in resp.json():
            if folder['folderName'] == f_name:
                return folder['folderId']

    def create_folder_under_cycle(self, folder_name, cycle_id=None):
        url = self.jira_url + 'zapi/latest/folder/create'

        if cycle_id is not None:
            c_id = cycle_id
        else:
            c_id = self.get_cycle_id(self.cycle_name)
        project_id = self.get_project_id_by_key()
        version_id = self.get_version_for_project_id()
        post_data = json.dumps({
            "versionId": version_id,
            "cycleId": c_id,
            "projectId": project_id,
            "name": folder_name
        })
        headers = {'content-type': 'application/json'}

        print(f"Post {url} with data {post_data}")
        resp = requests.post(url, data=post_data, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            return self.get_folder_id(cycle_id=cycle_id, project_id=project_id, version_id=version_id,
                                      folder_name=folder_name)
        else:
            raise Exception(f'Unable to create folder {resp.content}')
