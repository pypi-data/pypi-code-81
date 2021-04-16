import math
from .jobtype import JOBTYPE
from .api import ProjectApi, PipelineApi, WorkflowApi, JobApi


class _BaseModel(object):

    def execute(self, apicall, params, limit=math.inf):
        result = apicall(**params)
        items = result['items']
        if result['next_page_token']:
            page_token = result['next_page_token']
            params['page_token'] = page_token
            while page_token is not None:
                result = apicall(**params)
                items.extend(result['items'])
                if len(items) < limit and result['next_page_token']:
                    page_token = result['next_page_token']
                else:
                    page_token = None
        return items


class Project(_BaseModel):
    def __init__(self, name):
        self.name = name
        self.pipelines = []
        self.api = ProjectApi(name)

    def get_pipelines(self, num=20):
        pipelines = self.execute(self.api.get_pipelines, {}, limit=num)
        self.pipelines = [Pipeline(p['id'], p['state'], p['vcs']['branch']) for p in pipelines]
        return self.pipelines


class Pipeline(_BaseModel):
    def __init__(self, id, state, branch):
        self.id = id
        self.state = state
        self.branch = branch
        self.workflows = []
        self.api = PipelineApi(id)

    def get_workflows(self, failed_only=False):
        workflows = self.execute(self.api.get_workflows, {'failed_only': failed_only})
        self.workflows = [Workflow(w['id'], w['name'], w['status']) for w in workflows]
        return self.workflows


class Workflow:
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status
        self.jobs = []
        self.api = WorkflowApi(id)

    def get_jobs(self, type=JOBTYPE.ALL, failed_only=False):
        jobs = self.execute(self.api.get_jobs, {'type': type, 'failed_only': failed_only})
        self.jobs = [Job(j['id'], j['name'], j['job_number'], j['status'], j['project_slug']) for j in jobs]
        return self.jobs


class Job:
    def __init__(self, id, name, number, status, project_slug):
        self.id = id
        self.name = name
        self.number = number
        self.status = status
        self.project_slug = project_slug
        self.tests = []
        self.api = JobApi(id, number, project_slug)

    def get_tests(self, failed_only=False):
        tests = self.execute(self.api.get_tests, {'failed_only': failed_only})
        self.tests = [Test(t['result'], t['message'], t['file'], t['name'], t['classname']) for t in tests]
        return self.tests


class Test:
    def __init__(self, result, message, file, name, classname):
        self.result = result
        self.message = message
        self.file = file
        self.name = name
        self.classname = classname

    def __str__(self):
        return f'{self.name} - {self.result} - {self.message}'
