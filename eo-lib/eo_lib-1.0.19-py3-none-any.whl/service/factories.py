import factory
from eo_lib.service.teams.service import *

class PersonFactory(factory.Factory):
    class Meta:
        model = PersonService

class OrganizationFactory(factory.Factory):
    class Meta:
        model = OrganizationService

class TeamMembershipFactory(factory.Factory):
    class Meta:
        model = TeamMembershipService

class TeamFactory(factory.Factory):
    class Meta:
        model = TeamService

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMemberService

class ProjectTeamFactory(factory.Factory):
    class Meta:
        model = ProjectTeamService

class ProjectFactory(factory.Factory):
    class Meta:
        model = ProjectService
