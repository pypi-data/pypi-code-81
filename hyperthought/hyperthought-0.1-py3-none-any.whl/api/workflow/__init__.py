from datetime import datetime
from functools import partial
import os
import sys
from xml.etree.ElementTree import tostring

import requests

up = os.path.dirname
# <submodule>/api/workflow/common.py
submodule_directory = up(up(up(__file__)))
sys.path.append(submodule_directory)

from api.base import GenericAPI, ERROR_THRESHOLD
import utils

from ._construction import algorithms as alg, xml_generation as xmlgen


class WorkflowAPI(GenericAPI):
    """
    Files API switchboard.

    Contains methods that (loosely) correspond to endpoints for the
    HyperThought workflow app.  The methods simplify some get/update tasks.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers and cookies needed to call
        HyperThought endpoints.
    """

    def __init__(self, auth):
        super().__init__(auth)

    def get_templates(self, project_id):
        """
        Get templates in a given project.

        Parameters
        ----------
        project_id : str
            The id (uuid) of the project of interest.
            This can be found in the url of the project as the 'project'
            query parameter.

        Returns
        -------
        A list of dicts, each dict providing information on a workflow in the
        project.

        TODO:  Add additional parameters per the view class definition.
               See apps/workflow/api.py -> class Templates.
        """
        url = (
            f"{self._base_url}/api/workflow/process/templates/"
            f"?project={project_id}"
        )
        r = requests.get(
            url=url,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        return r.json()

    def get_children(self, workflow_id):
        """
        Get children (contained elements) of a parent workflow.

        Parameters
        ----------
        workflow_id : str 
            The id (uuid) of the parent workflow or subworkflow.
        
        Returns
        -------
        A list of dicts, each dict corresponding to a MarkLogic document
        for a child (contained element).
        """
        url = f"{self._base_url}/api/workflow/process/{workflow_id}/children"
        r = requests.get(
            url=url,
            cookies=self._auth.get_cookies(),
            headers=self._auth.get_headers(),
            verify=False,
        )

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        return r.json()

    def get_process(self, process_id=None, project_id=None, workflow_path=None):
        """
        Get a process (process or workflow) at a given path in a workflow.  

        Parameters
        ----------
        process_id : str or None
            The id of the process to get.  If provided, project_id and
            workflow_path will be ignored.  If None, project_id and
            workflow_path will need to be provided.
        project_id : str
            The id of the project.  
        workflow_path : str
            A human-readable parent->child path, i.e. Test01/A/B/C for a
            workflow named Test01, which contains a workflow named A,
            which contains a workflow named B, which contains a process named C.
        
        Returns
        -------
        Returns a process document for the process at the given path.
        """
        if process_id is None:
            if project_id is None or workflow_path is None:
                raise ValueError(
                    "process_id or project_id/workflow_path must be provided"
                )
        
        if process_id:
            url = f"{self._base_url}/api/workflow/process/{process_id}"
            r = requests.get(
                url=url,
                headers=self._auth.get_headers(),
                cookies=self._auth.get_cookies(),
                verify=False,
            )

            if r.status_code >= ERROR_THRESHOLD:
                # NOTE:  This method will throw an exception.
                self._report_api_error(response=r)

            return r.json()

        process_names = workflow_path.split('/')
        experiment_name = process_names[0]
        remaining_process_names = process_names[1:]
        experiments_url = f"{self._base_url}/api/workflow/process/templates/?project={project_id}"
        r = requests.get(
            url=experiments_url,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False
        )

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        experiments = r.json()
        process = None
        process_id = None
        
        for experiment in experiments:
            if experiment['title'] == experiment_name:
                process = experiment
                process_id = experiment['key']
                break
                
        # TODO:  Raise exception.
        assert process is not None
        
        for process_name in remaining_process_names:
            children = self.get_children(process_id)
            child_process = None
            child_process_id = None
            
            for child in children:
                if child['content']['name'] == process_name:
                    child_process = child
                    child_process_id = child['content']['pk']
                    break
                    
            assert child_process is not None
            process = child_process
            process_id = child_process_id
            
        return process

    def update_process(self, updated_document):
        """Commit updates to a process."""
        process_id = updated_document['content']['pk']
        updates = updated_document['content']

        if 'metadata' in updated_document:
            updates['metadata'] = updated_document['metadata']

        url = f"{self._base_url}/api/workflow/process/{process_id}/"
        curried_request = partial(
            requests.patch,
            url=url,
            json=updates,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )
        # TODO:  Surround all such calls by try/except.  Report errors.
        r = self.attempt_api_call(curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

    def create_workflow(self, project_id, workflow_id, elements,
                        parent_id=None, recurse=True):
        """
        Create a workflow document (as opposed to process or decision).

        Parameters
        ----------
        project_id : str
            The id for the project where the workflow should be created.
        workflow_id : str
            The id (pk) for the workflow document to be created.
        elements: list of dict
            Specifications of workflow documents to be created.
            Keys must include the following:
                id : str
                    Pre-computed id for the process/workflow represented by a
                    canvas element.
                name : str
                    Name of the process/workflow.
                type : str
                    Type of element.  Must be 'process' or 'workflow'.
                predecessors : list of str
                    List of predecessor ids.  (Heads of edges.)
                successors : list of str
                    List of successor ids.  (Tails of edges.)
            Keys may include 'children' (for workflows) and 'metadata'
            (for processes).
        recurse : bool
            Create documents for children as well as workflow itself.

        Returns
        -------
        The payload returned by the API endpoint.
        """
        id_to_element = {element['id']: element for element in elements}
        workflow = id_to_element[workflow_id]
        children = [
            id_to_element[id_]
            for id_ in workflow['children']
        ]
        children = alg.coordinates.add_coordinates(children)
        xml_ = tostring(xmlgen.create_xml(logical_children=children)).decode()
        xml_ = xml_.replace("\"", "\'")
        username = self._auth.get_username()
        create_date = datetime.now().isoformat()
        permissions = {
            'groups': {},
            'users': {},
            'projects': {
                project_id: 'edit'
            }
        }

        payload = {
            'xml': xml_,
            'pk': workflow_id,
            'name': workflow['name'],
            'creator': username,
            'created': create_date,
            'modifier': username,
            'modified': create_date,
            'template': True,
            'process_type': 'workflow',
            'permissions': permissions,
            'children': [child['id'] for child in children],
            'client_id': workflow['client_id'],
            'predecessors': workflow['predecessors'],
            'successors': workflow['successors'],
        }

        if parent_id:
            payload['parent_process'] = parent_id

        url = f"{self._base_url}/api/workflow/process/"
        curried_request = partial(
            requests.post,
            url=url,
            json=payload,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )
        # TODO:  Surround all such calls by try/except.  Report errors.
        r = self.attempt_api_call(curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        if recurse:
            for child in children:
                if child['type'] == 'process':
                    self.create_process(
                        project_id=project_id,
                        process_id=child['id'],
                        client_id=child['client_id'],
                        name=child['name'],
                        parent_id=workflow_id,
                        predecessors=child['predecessors'],
                        successors=child['successors'],
                        metadata=child['metadata'] if 'metadata' in child else None,
                    )
                elif child['type'] == 'workflow':
                    self.create_workflow(
                        project_id=project_id,
                        workflow_id=child['id'],
                        elements=elements,
                        parent_id=workflow_id,
                    )
                else:
                    # TODO:  Raise exception.
                    pass

        return r.json()
        
    def create_process(self, project_id, process_id, client_id, name,
                       predecessors, successors, parent_id, metadata=None):
        """
        Create a process document (as opposed to workflow or decision).

        Parameters
        ----------
        project_id : str
            The id for the project where the workflow should be created.
        process_id : str
            The id for the process document to be created.
        client_id : str
            The id for the process in the graph XML.
        name : str
            The name of the process.
        predecessors : list of str
            ids of processes with arrows leading to the process to be created.
        successors : list of str
            ids of processes with arrows leading from the process to be created.
        parent_id : str
            id of parent process.
        metadata: list of dict or None
            Metadata items to associate with the process.
            Metadata structure must be the same as elsewhere in HyperThought:
            Keys:   'keyName', 'value' (subkeys 'type' and 'link'), 'unit',
                    'annotation'

        Returns
        -------
        The payload returned by the API endpoint.
        """
        username = self._auth.get_username()
        create_date = datetime.now().isoformat()
        permissions = {
            'groups': {},
            'users': {},
            'projects': {
                project_id: 'edit'
            }
        }

        payload = {
            'pk': process_id,
            'client_id': client_id,
            'name': name,
            'creator': username,
            'created': create_date,
            'modifier': username,
            'modified': create_date,
            'template': True,
            'process_type': 'process',
            'permissions': permissions,
            'parent_process': parent_id,
            'predecessors': predecessors,
            'successors': successors,
        }

        url = f"{self._base_url}/api/workflow/process/"
        curried_request = partial(
            requests.post,
            url=url,
            json=payload,
            headers=self._auth.get_headers(),
            cookies=self._auth.get_cookies(),
            verify=False,
        )
        r = self.attempt_api_call(curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        document = r.json()

        if metadata:
            utils.validate_metadata(metadata)
            document['metadata'] = metadata
            self.update_process(document)
    
        return document
