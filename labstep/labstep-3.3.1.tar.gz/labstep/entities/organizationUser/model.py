#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.generic.entity.model import Entity


class OrganizationUser(Entity):
    __entityName__ = "user-organization"

    def promote(self):
        """
        Promtes a user to admin.


        Example
        -------
        ::

            my_organization.edit(body='My new organization.')
        """
        from labstep.entities.organizationUser.repository import organizationUserRepository

        return organizationUserRepository.promoteUser(self)

    def demote(self):
        """
        Demotes a user to normal member.


        Example
        -------
        ::

            my_organization.edit(body='My new organization.')
        """
        from labstep.entities.organizationUser.repository import organizationUserRepository

        return organizationUserRepository.demoteUser(self)

    def disable(self):
        """
        Disables a user account.


        Example
        -------
        ::

            my_organization.edit(body='My new organization.')
        """
        from labstep.entities.organizationUser.repository import organizationUserRepository

        return organizationUserRepository.disableUser(self)
