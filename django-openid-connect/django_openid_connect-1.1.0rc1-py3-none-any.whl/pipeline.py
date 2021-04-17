from django.conf import settings
from django.contrib.auth.models import Group
import logging
from urnparse import URN8141


logger = logging.getLogger(__name__)


def user_groups(strategy, details, user=None, *args, **kwargs):
    """
        Update user group membership using data from OpenId provider.

        :raises ValueError
    """
    group_attr = kwargs['response'].get(settings.REMOTE_GROUP_KEY, None)
    if not group_attr:
        return
    internal_group_attr = [URN8141.from_string(g).specific_string.decoded for g in settings.REMOTE_GROUP_FILTER(group_attr)]
    # Create valid nonexist groups
    for g in internal_group_attr:
        try:
            Group.objects.create(name=g)
        except:
            pass
    if user:
        # Remove user from any extra groups that weren't provided by OpenId
        remote_groups = Group.objects.filter(name__in=internal_group_attr)
        extra_groups = user.groups.exclude(name__in=[g.name for g in remote_groups] + settings.PROTECTED_GROUPS)
        # if user is superuser means may have groups assigned for test
        if not user.is_superuser:
            for eg in extra_groups:
                logger.debug('Removing {} from group {}'.format(user.username, eg.name))
                eg.user_set.remove(user)

        # Add user to groups provided by OpenId
        local_groups = user.groups.all()
        new_memberships = remote_groups.exclude(name__in=[g.name for g in local_groups] + settings.PROTECTED_GROUPS)
        for ng in new_memberships:
            logger.debug('Adding {} to group {}'.format(user.username, ng.name))
            user.groups.add(ng.pk)
