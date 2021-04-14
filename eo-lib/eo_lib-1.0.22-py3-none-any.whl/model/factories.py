import factory
from eo_lib.model.teams.models import *
from eo_lib.model.core.models import *

class PersonFactory(factory.Factory):
    class Meta:
        model = Person

class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization

class TeamFactory(factory.Factory):
    class Meta:
        model = Team

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = TeamMember

class TeamMembershipFactory(factory.Factory):
    class Meta:
        model = TeamMembership

class ProjectTeamFactory(factory.Factory):
    class Meta:
        model = ProjectTeam

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

class OrganizationalTeamFactory(factory.Factory):
    class Meta:
        model = OrganizationalTeam

## Core
class ApplicationTypeFactory(factory.Factory):
    class Meta:
        model = ApplicationType

class ApplicationFactory(factory.Factory):
    class Meta:
        model = Application

class ConfigurationFactory(factory.Factory):
    class Meta:
        model = Configuration

class ApplicationReferenceFactory(factory.Factory):
    class Meta:
        model = ApplicationReference
