from django.conf import settings
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404
from rest_framework import serializers
import functools
from django.utils.timezone import localdate, timedelta

from djangoldp.models import Model
from djangoldp.views import LDPViewSet
from djangoldp_conversation.models import Conversation
from djangoldp_circle.models import Circle

from djangoldp_polls.permissions import *

# User = settings.AUTH_USER_MODEL
# User.name=User.get_full_name

#========================

#========================

class Tag (Model):
	name = models.CharField(max_length=250,verbose_name="Name")

	class Meta(Model.Meta):
		serializer_fields = ['@id','name']
		anonymous_perms = ['view']
		authenticated_perms = ['inherit','add']

	def __str__(self):
		return self.name


class PollOption (Model):
	name = models.CharField(max_length=250,verbose_name="Options available for a vote")

	class Meta(Model.Meta):
		serializer_fields = ['@id','name']
		nested_fields = ['userVote','relatedPollOptions']
		anonymous_perms = ['view','add']
		authenticated_perms =  ['inherit','add','delete','change']


	def __str__(self):
		return self.name

def onMonthLater():
	return localdate() + timedelta(days=30)



class Poll (Model):
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='createdVotes', null=True, blank=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=250,verbose_name="Title")
	image = models.URLField(verbose_name="Illustration",default=settings.BASE_URL +"/media/defaultpoll.png")
	hostingOrganisation = models.CharField(max_length=250,verbose_name="Name of the hosting organisation", null=True, blank=True)
	startDate = models.DateField(verbose_name="Start date", blank=True, null=True ) 
	endDate = models.DateField(verbose_name="End data", default=onMonthLater )
	shortDescription = models.CharField(max_length=250,verbose_name="Short description")
	longDescription = models.TextField(verbose_name="Long description")
	tags = models.ManyToManyField(Tag, related_name='polls', blank=True)
	pollOptions = models.ManyToManyField(PollOption, related_name='relatedPollOptions', blank=True)
	debate = models.ManyToManyField(Conversation, related_name='polls', blank=True)
	circle = models.ForeignKey(Circle, null=True, related_name="polls", on_delete=models.SET_NULL)

	class Meta(Model.Meta):
		auto_author = 'author'
		serializer_fields = ['@id','created_at','debate','pollOptions','votes','author','title','image','circle',\
		                    'hostingOrganisation','startDate','endDate','shortDescription','longDescription','tags', 'vote_result', 'vote_result_rank']
		nested_fields = ['tags','votes','pollOptions','debate','circle']
		anonymous_perms = ['view','add']
		authenticated_perms = ['inherit','change','delete']
		owner_perms = ['inherit','change','delete']
		owner_field = 'author'
		permission_classes = [PollPermissions]

	def __str__(self):
		return self.title

	# compute vote result following majority jugement algorithm
	@property
	def vote_result(self):
		# total number of submitted votes
		total = self.votes.count()
		if total == 0:
			return None

		# compute the median
		median = 0
		for option in self.pollOptions.all():
			median += self.votes.filter(chosenOption=option).count()
			if(median >= total/2):
				# The winning option has been found
				break
		return option

	# compute vote result rank (used to sort polls)
	@property
	def vote_result_rank(self):
		if not self.vote_result:
			return str(-1)
		rank = 0
		# find which rank is the result option
		for option in self.pollOptions.all():
			if option == self.vote_result :
				break
			else :
				rank += 1
		# make it a string to be able to sort it
		# see https://git.startinblox.com/framework/sib-core/issues/679
		return str(rank)


# used to execute func after a DB transaction is commited
# https://docs.djangoproject.com/en/dev/topics/db/transactions/#django.db.transaction.on_commit
def on_transaction_commit(func):
	def inner(*args, **kwargs):
		transaction.on_commit(lambda: func(*args, **kwargs))
	return inner

@receiver(post_save, sender=Poll)
@on_transaction_commit
def post_create_poll(sender, instance, **kwargs):

	# pollOptions list to generate
	model = ['À rejeter', 'À revoir', 'Moyen', 'Bien', 'Très bien']

	# verify if the options list is already correct
	if len(instance.pollOptions.all()) != len(model) or not functools.reduce(lambda x, y : x and y, map(lambda p, q: p.name == q,instance.pollOptions.all(),model), True):
		# if not, clear it and create the right ones
		instance.pollOptions.clear()
		for option in model:
			instance.pollOptions.add( PollOption.objects.create(name=option) )
		# save the new list (will re-enter this function but the check avoid infinite loop)
		instance.save()

# I know this shouldn't live here, but putting it in views results in circular dependency problems
# https://git.startinblox.com/djangoldp-packages/djangoldp/issues/278
class VoteViewSet(LDPViewSet):
	def is_safe_create(self, user, validated_data, *args, **kwargs):
		try:
			if 'poll' in validated_data.keys():
				poll = Poll.objects.get(urlid=validated_data['poll']['urlid'])
			else:
				poll = self.get_parent()

			if Vote.objects.filter(relatedPoll=poll, user=user).exists():
				raise serializers.ValidationError('You may only vote on this poll once!')

		except Poll.DoesNotExist:
			return True
		except (KeyError, AttributeError):
			raise Http404('circle not specified with urlid')

		return True


class Vote (Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes',null=True,blank=True, on_delete=models.SET_NULL)
	chosenOption =  models.ForeignKey(PollOption, related_name='userVote', on_delete=models.CASCADE)
	relatedPoll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)

	class Meta(Model.Meta):
		auto_author = "user"
		serializer_fields = ['@id','chosenOption','relatedPoll']
		nested_fields = []
		permission_classes = [VotePermissions]
		anonymous_perms = ['view','add','change']
		authenticated_perms =  ['inherit','add','delete']
		view_set = VoteViewSet

	def __str__(self):
		return self.chosenOption.__str__()
