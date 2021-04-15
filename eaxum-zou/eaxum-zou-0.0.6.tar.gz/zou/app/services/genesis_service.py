import requests
from zou.app.config import GENESIS_HOST, GENESIS_PORT, SVN_SERVER_PARENT_URL
from zou.app.services import (
                                file_tree_service,
                                persons_service,
                                projects_service,
                                assets_service,
                                tasks_service,
                                shots_service
                            )
import os

def create_project(data):
    project_name = data['name']
    requests.post(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}")
    svn_url = os.path.join(SVN_SERVER_PARENT_URL, project_name.replace(' ', '_').lower())
    data.update({'file_tree': file_tree_service.get_tree_from_file('eaxum'), 'data': {'local_svn_url': svn_url, 'remote_svn_url': svn_url}})

def project_rename(data, instance_dict):
    try:
        if instance_dict['name'] != data['name']:
            payload = {
                'old_project_name':instance_dict['name'],
                'new_project_name':data['name']
                }
            project_name = data['name']
            requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}", json=payload)
    except KeyError:
        pass

def archive_project(project_name):
    print(project_name)
    requests.delete(url=f"{GENESIS_HOST}:{GENESIS_PORT}/project/{project_name}")

def get_svn_base_directory(project:dict, working_file_path):
    '''
        get svn repository acl directory
    '''
    root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],project['name'].replace(' ', '_'),'')
    base_svn_directory = os.path.join(f"{project['name']}:",working_file_path.split(root.lower(),1)[1])
    return base_svn_directory.lower()

def get_base_file_directory():
    pass

def create_task_file(entity, task, task_type, project_id):
    working_file_path = file_tree_service.get_working_file_path(task.serialize())
    # working_file_path = file_tree_service.get_working_file_path(task.serialize()) \
    #     .rsplit('/', 1)
    # working_file_path = os.path.join(working_file_path[0], entity['name'].replace(' ', '_').lower())
    project = projects_service.get_project(project_id)
    all_persons = persons_service.get_persons()
    project_name = project['name'].replace(' ', '_').lower()
    base_svn_directory = get_svn_base_directory(project, working_file_path)
    payload = {
            "project":project,
            "base_file_directory":working_file_path,
            "base_svn_directory":base_svn_directory,
            "all_persons":all_persons,
            "task_type":task_type['name'].lower()
    }
    requests.post(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task/{project_name}", json=payload)

def rename_task_file(data, task, entity, project, payload, entity_type):
    tasks_service.clear_task_cache(task['id'])
    task_type = tasks_service.get_task_type(task['task_type_id'])
    # FIXME working file path different from new entity name when task is renamed
    # added a hack for now
    print(entity.serialize())
    if entity_type == 'asset':
        # set working file path to previous name
        working_file_path = file_tree_service.get_working_file_path(task) \
            .rsplit('/', 1)
        working_file_path = os.path.join(working_file_path[0], entity.serialize()['name'].replace(' ', '_').lower())
        new_file_name = data['name'].replace(' ', '_').lower()
    elif entity_type == 'shot':
        working_file_path = file_tree_service.get_working_file_path(task) \
            .rsplit('/', 2)
        entity_name = entity.serialize()['name'].replace(' ', '_').lower()
        shot_file_name = f"{working_file_path[2].rsplit('_', 1)[0]}_{entity_name}"
        new_file_name = f"{working_file_path[2].rsplit('_', 1)[0]}_{data['name'].replace(' ', '_').lower()}"
        working_file_path = os.path.join(working_file_path[0],entity_name,shot_file_name)

        print('sd',data['name'], working_file_path)
    print(working_file_path)
    print(file_tree_service.get_working_file_path(task))
    base_svn_directory = get_svn_base_directory(project, working_file_path)
    task_payload = {
        'entity_type':entity_type,
        'project':project,
        'base_svn_directory':base_svn_directory,
        'working_file_path':working_file_path,
        'new_file_name':new_file_name,
        'task_type':task_type['name'].lower(),
    }
    payload.append(task_payload)

def rename_asset_task_file(data, entity):
    if data['name'] != entity.serialize()['name']:
        print(entity.serialize()['name'], '-----------------', data['name'])
        print(entity)
        project = projects_service.get_project(entity.serialize()["project_id"])
        if assets_service.is_asset(entity):
            assets_service.clear_asset_cache(str(entity.id))
            full_asset = assets_service.get_full_asset(entity.serialize()['id'])
            asset_tasks = full_asset['tasks']
            if asset_tasks:
                payload = []
                for task in asset_tasks:
                    rename_task_file(
                        data=data,
                        task=task,
                        entity=entity,
                        project=project,
                        payload=payload,
                        entity_type='asset'
                    )
                requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/asset/{project['name']}", json=payload)
        elif shots_service.is_shot(entity.serialize()):
            shots_service.clear_shot_cache(str(entity.id))
            full_shot = shots_service.get_full_shot(entity.serialize()['id'])
            shot_tasks = full_shot['tasks']
            if shot_tasks:
                payload = []
                for task in shot_tasks:
                    rename_task_file(
                        data=data,
                        task=task,
                        entity=entity,
                        project=project,
                        payload=payload,
                        entity_type='shot'
                    )
                requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/asset/{project['name']}", json=payload)

def delete_task_file(task, entity_type):
    tasks_service.clear_task_cache(task['id'])
    task_type = tasks_service.get_task_type(task['task_type_id'])
    project = projects_service.get_project(task["project_id"])
    # FIXME working file path different from new entity name when task is renamed
    # added a hack for now
    if entity_type == 'asset':
        # set working file path to previous name
        working_file_path = file_tree_service.get_working_file_path(task)
        # working_file_path = file_tree_service.get_working_file_path(task) \
        #     .rsplit('/', 1)
        # working_file_path = os.path.join(working_file_path[0], entity.serialize()['name'].replace(' ', '_').lower())
    elif entity_type == 'shot':
        working_file_path = file_tree_service.get_working_file_path(task)
        # working_file_path = file_tree_service.get_working_file_path(task) \
        #     .rsplit('/', 2)
        # entity_name = entity.serialize()['name'].replace(' ', '_').lower()
        # shot_file_name = f"{working_file_path[2].rsplit('_', 1)[0]}_{entity_name}"
        # working_file_path = os.path.join(working_file_path[0],entity_name,shot_file_name)
    base_svn_directory = get_svn_base_directory(project, working_file_path)
    task_payload = {
        'entity_type':entity_type,
        'project':project,
        'base_svn_directory':base_svn_directory,
        "base_file_directory":working_file_path,
        'task_type':task_type['name'].lower(),
    }
    requests.delete(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task/{project['name']}", json=task_payload)

def grant_file_access(task, person, project_id):
    print(task.task_type_id)
    task_type = tasks_service.get_task_type(str(task.task_type_id))
    working_file_path = file_tree_service.get_working_file_path(task.serialize())
    project = projects_service.get_project(project_id)
    # working_file_path = os.path.join(working_file_path[0], entity.serialize()['name'].replace(' ', '_').lower())
    base_svn_directory = get_svn_base_directory(project, working_file_path)
    print(base_svn_directory)
    project_name = project['name'].replace(' ', '_').lower()
    payload = {
        'base_svn_directory':base_svn_directory,
        "task_type":task_type['name'].lower(),
        'person':person.serialize(),  
    }
    requests.put(url=f"{GENESIS_HOST}:{GENESIS_PORT}/task_acl/{project_name}", json=payload)
