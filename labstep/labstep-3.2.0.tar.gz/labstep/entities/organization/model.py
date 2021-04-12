#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.organizationUser.repository import organizationUserRepository
from labstep.generic.entity.model import Entity
from labstep.entities.workspace.repository import workspaceRepository


class Organization(Entity):
    __entityName__ = "organization"

    def edit(self, name, extraParams={}):
        """
        Edit Organization.

        Parameters
        ----------
        name (str)
            The name of the Organization.

        Returns
        -------
        :class:`~labstep.entities.organization.model.Organization`
            An object representing the organization.

        Example
        -------
        ::

            my_organization.edit(body='My new organization.')
        """
        from labstep.entities.organization.repository import organizationRepository

        return organizationRepository.editOrganization(self.__user__, name, extraParams=extraParams)

    def inviteUsers(self, emails, workspace_id=None):
        from labstep.entities.organization.repository import organizationRepository

        return organizationRepository.inviteUsers(self, emails=emails, workspace_id=workspace_id)

    def getWorkspaces(self, count=100, search_query=None):
        return workspaceRepository.getWorkspaces(self.__user__,
                                                 count=count,
                                                 search_query=search_query,
                                                 extraParams={'organization_id': self.id})

    def getUsers(self, count, extraParams):
        return organizationUserRepository.getOrganizationUsers(self,
                                                               count=count,
                                                               extraParams=extraParams)
