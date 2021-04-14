from eo_lib.service.teams.service import *
from eo_lib.application.abstract_application import AbstractApplication

class ApplicationPerson(AbstractApplication):

	""" Application of  Person"""
	def __init__(self):
		super().__init__(PersonService())
	
class ApplicationOrganization(AbstractApplication):

	""" Application of  Organization"""
	def __init__(self):
		super().__init__(OrganizationService())
	
class ApplicationOrganization_Role(AbstractApplication):

	""" Application of  Organization_Role"""
	def __init__(self):
		super().__init__(Organization_RoleService())
	
class ApplicationTeamMembership(AbstractApplication):

	""" Application of  TeamMembership"""
	def __init__(self):
		super().__init__(TeamMembershipService())
	
class ApplicationTeam(AbstractApplication):

	""" Application of  Team"""
	def __init__(self):
		super().__init__(TeamService())
	
class ApplicationTeamMember(AbstractApplication):

	""" Application of  TeamMember"""
	def __init__(self):
		super().__init__(TeamMemberService())
	
class ApplicationProjectTeam(AbstractApplication):

	""" Application of  ProjectTeam"""
	def __init__(self):
		super().__init__(ProjectTeamService())
	
class ApplicationProject(AbstractApplication):

	""" Application of  Project"""
	def __init__(self):
		super().__init__(ProjectService())
	
class ApplicationOrganizationalTeam(AbstractApplication):

	""" Application of  OrganizationalTeam"""
	def __init__(self):
		super().__init__(OrganizationalTeamService())
	
