from django.http import Http404

from djangoldp.views import LDPViewSet, NoCSRFAuthentication
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes 

from .models import Poll,Vote
from .serializers import PollOptionSerializer


class CanVoteOnPollViewSet(APIView):
    authentication_classes = (NoCSRFAuthentication,) 

    def dispatch(self, request, *args, **kwargs):
        '''overriden dispatch method to append some custom headers'''
        response = super(CanVoteOnPollViewSet, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.META.get('HTTP_ORIGIN')
        response["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, cache-control, pragma, user-agent"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Accept-Post"] = "application/ld+json"

        if request.user.is_authenticated:
            try:
                response['User'] = request.user.webid()
            except AttributeError:
                pass
        return response

    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        # '''returns True if the user can vote, or False if they have already voted'''
        headers = {
            "Access-Control-Allow-Origin" : request.META.get('HTTP_ORIGIN'),
            "Access-Control-Allow-Headers": "authorization, Content-Type, if-match, accept, cache-control, pragma, user-agent",
            "Access-Control-Expose-Headers": "Location, User",
            "Access-Control-Allow-Credentials": 'true'
        }

        try:
            poll = Poll.objects.get(pk=pk)
            can_vote = True
            if Vote.objects.filter(relatedPoll=poll, user=request.user).exists():
                can_vote = False
            return Response(can_vote, status=status.HTTP_200_OK, headers=headers)

        except Poll.DoesNotExist:
            return Response(data={'error': {'poll': ['Could not find poll with this ID!']}},
                            status=status.HTTP_404_NOT_FOUND, headers=headers)


class FuturePollViewset(LDPViewSet):
    model = Poll

    def get_queryset(self):
        return super().get_queryset().filter(enddate__gte=datetime.now())


class TotalVotes(LDPViewSet):
    '''view to GET the total counts of votes selecting a particular option'''
    serializer_class = PollOptionSerializer

    def _get_poll_or_404(self):
        pk = self.kwargs['pk']

        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404('could not get a Poll with this ID!')

    def get_serializer_context(self):
        poll = self._get_poll_or_404()

        votes = poll.votes.all()
        context = super().get_serializer_context()
        context.update({'votes_queryset': votes})
        return context

    def get_queryset(self, *args, **kwargs):
        poll = self._get_poll_or_404()
        return poll.pollOptions.all()

    def get_serializer_class(self):
        # NOTE: this is required because currently DjangoLDP overrides the serializer_class during __init__
        # https://git.startinblox.com/djangoldp-packages/djangoldp/issues/241
        return PollOptionSerializer
