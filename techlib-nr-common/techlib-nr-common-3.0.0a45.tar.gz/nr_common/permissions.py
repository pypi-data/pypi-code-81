# DRAFT dataset record manipulation
from invenio_access import authenticated_user
from invenio_records_rest.utils import deny_all, allow_all
from oarepo_communities.permissions import read_object_permission_impl, create_object_permission_impl, \
    update_object_permission_impl, delete_object_permission_impl, publish_permission_impl, unpublish_permission_impl, \
    community_member_permission_impl, community_curator_permission_impl
from oarepo_fsm.permissions import require_any, require_all
from flask_principal import Permission, RoleNeed

CURATOR_ROLE_PERMISSIONS = Permission(
    RoleNeed('curator')
)

INGESTER_ROLE_PERMISSIONS = Permission(
    RoleNeed('ingester')
)

ADMIN_ROLE_PERMISSIONS = Permission(
    RoleNeed('admin')
)

AUTHENTICATED_PERMISSION = Permission(authenticated_user)

COMMUNITY_MEMBER_PERMISSION = community_member_permission_impl
COMMUNITY_CURATOR_PERMISSION = community_curator_permission_impl

create_draft_object_permission_impl = require_any(
    INGESTER_ROLE_PERMISSIONS,
    create_object_permission_impl
)
update_draft_object_permission_impl = require_any(
    INGESTER_ROLE_PERMISSIONS,
    update_object_permission_impl
)
read_draft_object_permission_impl = require_any(
    INGESTER_ROLE_PERMISSIONS,
    read_object_permission_impl
)
delete_draft_object_permission_impl = delete_object_permission_impl
list_draft_object_permission_impl = allow_all

# DRAFT dataset file manipulation
put_draft_file_permission_impl = require_any(
    INGESTER_ROLE_PERMISSIONS,
    update_object_permission_impl
)
get_draft_file_permission_impl = require_any(
    INGESTER_ROLE_PERMISSIONS,
    read_draft_object_permission_impl
)
delete_draft_file_permission_impl = update_object_permission_impl

# DRAFT dataset publishing
publish_draft_object_permission_impl = publish_permission_impl
unpublish_draft_object_permission_impl = unpublish_permission_impl

# PUBLISHED dataset manipulation
update_object_permission_impl = require_all(ADMIN_ROLE_PERMISSIONS)

# ALL dataset list
list_all_object_permission_impl = allow_all
