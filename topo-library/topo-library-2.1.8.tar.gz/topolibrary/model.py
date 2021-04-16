"""Mongo data models."""

from mongoengine.fields import (Document, StringField, DateTimeField,
                                ListField, IntField, EmbeddedDocument,
                                EmbeddedDocumentListField, BooleanField,
                                DictField, FloatField, EmbeddedDocumentField)


class VelocityKPI(EmbeddedDocument):
    """The velocity KPI total and sub-totals."""

    size = FloatField(default=0.0)
    duration = FloatField(default=0.0)
    dev_time = FloatField(default=0.0)
    commit_count = FloatField(default=0.0)
    commit_freq = FloatField(default=0.0)


class DevelopmentKPI(EmbeddedDocument):
    """The investment KPI total and sub-totals."""

    feature = FloatField(default=0.0)
    debt = FloatField(default=0.0)
    debug = FloatField(default=0.0)
    defect = FloatField(default=0.0)


class IssuesTotal(EmbeddedDocument):
    """The infrastructure KPI total and sub-totals."""
    code_warnings = IntField(default=0)
    code_errors = IntField(default=0)
    devops_warnings = IntField(default=0)
    devops_errors = IntField(default=0)


class LinterScanEvent(EmbeddedDocument):
    """A sub-document for static analysis events.

    Attributes:
        linter_name (StringField): The name of the linter that ran against the file.
        file_path (StringField): The full path of the file in the repo.
        errors_total (IntField): Total number of errors.
        warnings_total (IntField): Total number of warnings.
        linter_output (StringField): Full output from the linter.
    """

    file_type = StringField()
    linter_name = StringField()
    file_path = StringField()

    warnings = IntField()
    errors = IntField()

    linter_output = StringField()


class AutomationKPI(EmbeddedDocument):
    """The maturity KPI total and sub-totals."""

    automation_total = FloatField(default=0.0)
    iac = FloatField(default=0.0)
    containers = FloatField(default=0.0)
    build_tools = FloatField(default=0.0)
    local_dev = FloatField(default=0.0)


class CicdKPI(EmbeddedDocument):
    """The quality KPI total and sub-totals."""

    cicd_total = FloatField(default=0.0)
    pipeline = FloatField(default=0.0)
    testing = FloatField(default=0.0)
    static_analysis = FloatField(default=0.0)
    deploy = FloatField(default=0.0)


class SecurityKPI(EmbeddedDocument):
    """The risk KPI total and sub-totals."""

    security_total = FloatField(default=0.0)
    least_privledge = FloatField(default=0.0)
    secrets = FloatField(default=0.0)
    auth = FloatField(default=0.0)
    keys = FloatField(default=0.0)


class InfrastructureKPI(EmbeddedDocument):
    """The infrastructure KPI total and sub-totals."""

    infrastructure_total = FloatField(default=0.0)
    networking = FloatField(default=0.0)
    compute_resources = FloatField(default=0.0)
    environments = FloatField(default=0.0)
    tags = FloatField(default=0.0)


class UserCommit(EmbeddedDocument):
    ''' User Commit '''
    sha = StringField(required=True)
    name = StringField(required=True)


class UserEvent(Document):
    """The repository events collection model.

    Attributes:
        event_type (StringField): The GitHub event type https://developer.github.com/v3/activity/event_types
        organization (StringField): The organization name of the GitHub repo.
        repository (StringField): The name of the GitHub repo.
        timestamp (DateTimeField): The datetime timestamp of the event.
    """

    meta = {'allow_inheritance': True}

    # Crawler fields
    organization = StringField(required=True)
    repository = StringField(required=True)
    timestamp = DateTimeField(required=True)

    # Processed File List
    file_list = ListField()

    # Commit fields
    sha = StringField(required=True)
    ref = StringField(required=True, null=True)
    user = StringField(required=True)

    # PR Details
    additions = IntField(default=0)
    deletions = IntField(default=0)
    total = IntField(default=0)
    commit_files = ListField()

    # KPIs
    development_kpi = EmbeddedDocumentField(DevelopmentKPI)
    velocity_kpi = EmbeddedDocumentField(VelocityKPI)


class PrEvent(Document):
    """The GitHub commit events model.

    Attributes:
        sha (StringField): The SHA of the most recent commit on ref after the push.
        ref (StringField): The full git ref that was pushed. Example: refs/heads/master.
        content_flags (ListField, optional): Flags that matched the file content rules.
        filename_flags (ListField, optional): Flags that matched the filename rules.
        LinterScanEvents (Document): A sub-document for static analysis events.
    """
    meta = {'allow_inheritance': True}

    # Crawler fields
    organization = StringField(required=True)
    repository = StringField(required=True)
    timestamp = DateTimeField(required=True)

    # Commit fields
    sha = StringField(required=True)
    ref = StringField(required=True, null=True)
    user = StringField(required=True)

    # PR Details
    additions = IntField(default=0)
    deletions = IntField(default=0)
    total = IntField(default=0)
    commit_files = ListField()

    # KPIs
    development_kpi = EmbeddedDocumentField(DevelopmentKPI)
    velocity_kpi = EmbeddedDocumentField(VelocityKPI)

    # User Contributions
    users_commits = EmbeddedDocumentListField(UserCommit)

    # Category and Tokens
    repo_type = StringField()
    category = DictField()
    file_count = DictField()
    tokens = DictField()
    file_list = ListField()
    file_details = ListField()

    # Size and details
    total_length = IntField(default=0)
    comment_percent = FloatField()
    space_percent = FloatField()
    char_per_lines = FloatField()

    # Linter fields
    linter_events = EmbeddedDocumentListField(LinterScanEvent)
    issues_total = EmbeddedDocumentField(IssuesTotal)

    # Analysis fields
    total_kpis = FloatField(default=0.0)
    automation_kpi = EmbeddedDocumentField(AutomationKPI)
    cicd_kpi = EmbeddedDocumentField(CicdKPI)
    security_kpi = EmbeddedDocumentField(SecurityKPI)
    infra_kpi = EmbeddedDocumentField(InfrastructureKPI)


class PipelineRun(Document):
    """Pipeline events"""
    name = StringField(max_length=120, required=True)
    number = IntField()
    repo = StringField(max_length=200)
    branch = StringField(max_length=50)
    sha = StringField(max_length=50)
    commit_id = StringField(max_length=50)

    build_files = ListField(StringField(max_length=128))
    file_count = IntField()

    buildnumber = IntField(required=True)
    building = BooleanField(required=True)
    duration_millis = IntField()
    result = StringField(max_length=50)
    timestamp = DateTimeField()
    url = StringField(max_length=256)

    fail_stage = StringField(max_length=50)
    fail_logs = StringField(max_length=10000)


class Group(Document):
    """Group data"""
    name = StringField(max_length=120, primary_key=True, required=True)
    username = StringField(max_length=120, required=True)
    children = ListField(StringField(max_length=120))


class Set(Document):
    """Set data"""
    name = StringField(max_length=120, primary_key=True, required=True)
    username = StringField(max_length=120, required=True)
    children = ListField(StringField(max_length=120))


class JiraIssue(Document):
    """Agile issues"""
    issue_id = StringField()
    issue_key = StringField(primary_key=True, required=True)
    issuetype_name = StringField()
    parent_issue_key = StringField()
    parent_issue_id = StringField()
    project_id = StringField()
    project_key = StringField()
    project_name = StringField()
    resolution_name = StringField()
    resolution_date = DateTimeField()
    created = DateTimeField()
    priority_name = StringField()
    priority_id = StringField()
    status_name = StringField()
    assignee_key = StringField()
    story_points = FloatField()
    labels = ListField(StringField())
    updated = DateTimeField()
    work_begin_date = DateTimeField()
    work_completed_date = DateTimeField()


class SkippedRepo(Document):
    """Skipped repos logged from celery"""
    repo_name = StringField(max_length=120, primary_key=True, required=True)
    error = StringField(max_length=10000)


class LineHistory(EmbeddedDocument):
    """A sub-document for user contribution history"""

    index = IntField()
    user = StringField()
    commit = StringField()
    line_type = StringField()
    line_number = IntField()
    code = StringField()


class UserContribution(Document):
    """File line commit history"""
    organization = StringField()
    repository = StringField()
    file = StringField()
    line_history = EmbeddedDocumentListField(LineHistory)


class FileCommitHistory(Document):
    """File line commit history"""
    organization = StringField()
    repository = StringField()
    file = StringField()
    commits = ListField(StringField())


class Endpoints(Document):
    """ URLs that need to be tested 
    
    Attributes:
        name (StringField): Endpoint name
        url (StringField): Endpoint URL address which will be tested
        num_requests (IntField): Number of requests.
        response_timeout (IntField): Stop waiting for a response after a given number of seconds
    """
    name = StringField(max_length=120, required=True)
    url = StringField(required=True)
    num_requests = IntField()
    response_timeout = IntField()

class SmokeTestResults(Document):
    """ Smoke test results """
    name = StringField(max_length=120, required=True)
    url = StringField(required=True)
    response_status = StringField(required=True)
    avg_response_time = FloatField()

class CrawlerHistory(Document):
    """ Crawler History  """
    sysetm = StringField(max_length=120, required=True)
    timestamp = DateTimeField(required=True)
    url = StringField(required=True)
    run_time = FloatField()
    number_of_events = IntField()
    logs = StringField(max_length=10000)