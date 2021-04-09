from djangoldp.permissions import LDPPermissions

class VotePermissions(LDPPermissions):
	
	def get_object_permissions(self, request, view, obj):
		perms = super().get_object_permissions(request, view, obj)

		return perms


	def get_container_permissions(self, request, view, obj=None):
		perms = super().get_container_permissions(request, view, obj)

		return perms


class PollPermissions(LDPPermissions):
	with_cache = False

	# # this is needed as soon as I redefine the poll permissions class
	# def has_permission(self, request, view):
	# 	return request.method == 'OPTIONS' or not request.user.is_anonymous
# 
	# # give more permissions to users that are admins of the first circle
	# def user_permissions(self, user, obj_or_model, obj=None):
	# 	perms = super().user_permissions(user, obj_or_model, obj)
# 
	# 	if not user.is_anonymous and user.is_superuser:
	# 		perms.append('delete')
	# 		perms.append('change')
	# 	return perms

	def get_container_permissions(self, request, view, obj=None):
		perms = super().get_container_permissions(request, view, obj)

        # Remove add to user who already voted
		from .models import Vote
		if 'add' in perms and obj is not None:
			if Vote.objects.filter(relatedPoll=obj.pk, user=request.user).exists():
				perms.remove('add')

		return perms