import factory
from eo_lib.application.teams.application import *

class PersonFactory(factory.Factory):
    class Meta:
        model = ApplicationPerson

class OrganizationFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganization

class Organization_RoleFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganization_Role

class TeamMembershipFactory(factory.Factory):
    class Meta:
        model = ApplicationTeamMembership

class TeamFactory(factory.Factory):
    class Meta:
        model = ApplicationTeam

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = ApplicationTeamMember

class ProjectTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationProjectTeam

class ProjectFactory(factory.Factory):
    class Meta:
        model = ApplicationProject

class OrganizationalTeamFactory(factory.Factory):
    class Meta:
        model = ApplicationOrganizationalTeam

