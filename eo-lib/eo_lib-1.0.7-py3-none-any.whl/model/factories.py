import factory
from eo_lib.model.teams.models import *

class PersonFactory(factory.Factory):
    class Meta:
        model = Person

class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization

class Organization_RoleFactory(factory.Factory):
    class Meta:
        model = Organization_Role

class TeamMembershipFactory(factory.Factory):
    class Meta:
        model = TeamMembership

class TeamFactory(factory.Factory):
    class Meta:
        model = Team

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMember

class ProjectTeamFactory(factory.Factory):
    class Meta:
        model = ProjectTeam

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

class OrganizationalTeamFactory(factory.Factory):
    class Meta:
        model = OrganizationalTeam

