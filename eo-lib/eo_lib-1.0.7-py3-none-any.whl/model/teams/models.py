from eo_lib.config.base import Entity
from sqlalchemy import Column, Boolean ,ForeignKey, Integer, DateTime, Date, String, Text
from sqlalchemy.orm import relationship
from eo_lib.model.relationship.models import *

class Person(Entity):
	
	"""A human Physical Agent."""
	
	is_instance_of = "person"
	__tablename__  = "person"
	serialize_only = ('name', 'description', 'email',
	)
	type = Column(String(50))
	email = Column(String)


	organization_id = Column(Integer, ForeignKey('organization.id'))
	organization = relationship("Organization", back_populates="people")

	__mapper_args__ = {
		'polymorphic_identity':'team',
		'polymorphic_on':type
	}

class Organization(Entity):
	
	"""An Organization """
	
	is_instance_of = "organization "
	__tablename__  = "organization"
	serialize_only = ('name', 'description', 'email',
	'teams.uuid_',
	'people.uuid_',
	)
	email = Column(String)

	teams = relationship("OrganizationalTeam", back_populates="organization")
	people = relationship("Person", back_populates="organization")

	configuration = relationship("Configuration", back_populates="organization")

class Organization_Role(Entity):
	
	"""A Social Role, recognized by the Organization, assigned to Agents when they are hired, included in a team, allocated or  participating in activities.Ex.: System Analyst, Designer, Programmer, Client Organization."""
	
	is_instance_of = "organizational_role"
	__tablename__  = "organization_role"
	serialize_only = ('name', 'description', 'teammembership.uuid_',
	)

	teammembership = relationship("TeamMembership", back_populates="organization_role")



class TeamMembership(Entity):
	
	"""Relationship among Team member, organizational Role and team."""
	
	is_instance_of = "TeamMembership"
	__tablename__  = "teammembership"
	serialize_only = ('name', 'description', 'date',
	)
	date = Column(Date)


	teammember_id = Column(Integer, ForeignKey('teammember.id'))
	teammember = relationship("TeamMember", back_populates="teammembership")
	team_id = Column(Integer, ForeignKey('team.id'))
	team = relationship("Team", back_populates="teammembership")
	organization_role_id = Column(Integer, ForeignKey('organization_role.id'))
	organization_role = relationship("Organization_Role", back_populates="teammembership")


class Team(Entity):
	
	"""Social Agent representing a group of people with a defined purpose. Ex.: a Testing team, a Quality Assurance team, a Deployment team."""
	
	is_instance_of = "Team"
	__tablename__  = "team"
	serialize_only = ('name', 'description', 'teammembership.uuid_',
	)
	type = Column(String(50))

	teammembership = relationship("TeamMembership", back_populates="team")


	__mapper_args__ = {
		'polymorphic_identity':'team',
		'polymorphic_on':type
	}

class TeamMember(Person):
	
	"""A member of a team"""
	
	is_instance_of = "Person"
	__tablename__  = "teammember"
	serialize_only = ('name', 'description', 'teammembership.uuid_',
	)
	id = Column(Integer, ForeignKey('person.id'), primary_key=True)

	teammembership = relationship("TeamMembership", back_populates="teammember")


	__mapper_args__ = {
		'polymorphic_identity':'teammember',
	}

class ProjectTeam(Team):
	
	"""A Team with a project"""
	
	is_instance_of = "Team"
	__tablename__  = "projectteam"
	serialize_only = ('name', 'description', )
	id = Column(Integer, ForeignKey('team.id'), primary_key=True)


	project = Column(Integer, ForeignKey('project.id'))

	__mapper_args__ = {
		'polymorphic_identity':'projectteam',
	}

class Project(Entity):
	
	"""A Social Object as a temporary endeavor undertaken to create a unique product, service, or result. Ex.: A project to produce a software on demand."""
	
	is_instance_of = "Project"
	__tablename__  = "project"
	serialize_only = ('name', 'description', 'team.uuid_',
	)

	team = relationship("ProjectTeam", back_populates="project")



class OrganizationalTeam(Team):
	
	"""An Administrative Team from an Organization"""
	
	is_instance_of = "Team"
	__tablename__  = "organizationalteam"
	serialize_only = ('name', 'description', )
	id = Column(Integer, ForeignKey('team.id'), primary_key=True)


	organization = Column(Integer, ForeignKey('organization.id'))

	__mapper_args__ = {
		'polymorphic_identity':'organizationalteam',
	}
