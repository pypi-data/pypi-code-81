import factory
from eo_lib.application.teams.application import *
from eo_lib.application.core.application import *

class PersonFactory(factory.Factory):
    class Meta:
        model = ApplicationPerson

class OrganizationFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganization

class TeamFactory(factory.Factory):
    class Meta:
        model = ApplicationTeam

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = ApplicationTeamMember

class Organization_RoleFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganization_Role

class TeamMembershipFactory(factory.Factory):
    class Meta:
        model = ApplicationTeamMembership

class ProjectTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationProjectTeam

class ProjectFactory(factory.Factory):
    class Meta:
        model = ApplicationProject
        
class OrganizationalTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganizationalTeam



