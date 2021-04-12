#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.service.helpers import getTime
from labstep.entities.organizationUser.model import OrganizationUser
from labstep.generic.entity.repository import entityRepository


class OrganizationUserRepository:
    def getOrganizationUsers(self, organization, count=100, extraParams={}):

        params = {
            'organization_id': organization.id,
            **extraParams,
        }

        return entityRepository.getEntities(
            organization.__user__,
            OrganizationUser, count,
            filterParams=params)

    def promoteUser(self, organizationUser):
        params = {
            "type": "admin",
        }
        return entityRepository.editEntity(organizationUser, params)

    def demoteUser(self, organizationUser):
        params = {
            "type": "member",
        }
        return entityRepository.editEntity(organizationUser, params)

    def disableUser(self, organizationUser):
        params = {
            "deleted_at": getTime(),
        }
        return entityRepository.editEntity(organizationUser, params)


organizationUserRepository = OrganizationUserRepository()
