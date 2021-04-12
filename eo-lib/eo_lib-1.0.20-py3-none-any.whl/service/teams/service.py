from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from eo_lib.model.teams.models import *
from eo_lib.service.base_service import BaseService

class PersonService(BaseService):

    """ Service of Person"""

    def __init__(self):
        super(PersonService,self).__init__(Person)

class OrganizationService(BaseService):

    """ Service of Organization"""

    def __init__(self):
        super(OrganizationService,self).__init__(Organization)

class Organization_RoleService(BaseService):

    """ Service of Organization_Role"""

    def __init__(self):
        super(Organization_RoleService,self).__init__(Organization_Role)

class TeamMembershipService(BaseService):

    """ Service of TeamMembership"""

    def __init__(self):
        super(TeamMembershipService,self).__init__(TeamMembership)

class TeamService(BaseService):

    """ Service of Team"""

    def __init__(self):
        super(TeamService,self).__init__(Team)

class TeamMemberService(BaseService):

    """ Service of TeamMember"""

    def __init__(self):
        super(TeamMemberService,self).__init__(TeamMember)

class ProjectTeamService(BaseService):

    """ Service of ProjectTeam"""

    def __init__(self):
        super(ProjectTeamService,self).__init__(ProjectTeam)

class ProjectService(BaseService):

    """ Service of Project"""

    def __init__(self):
        super(ProjectService,self).__init__(Project)

class OrganizationalTeamService(BaseService):

    """ Service of OrganizationalTeam"""

    def __init__(self):
        super(OrganizationalTeamService,self).__init__(OrganizationalTeam)

