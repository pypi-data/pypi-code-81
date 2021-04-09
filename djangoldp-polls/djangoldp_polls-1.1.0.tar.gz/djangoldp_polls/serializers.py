from rest_framework import serializers
from djangoldp.serializers import LDPSerializer
from djangoldp_polls.models import PollOption


class PollOptionSerializer(LDPSerializer):
    total_votes = serializers.SerializerMethodField()
    with_cache = False

    class Meta:
        model = PollOption
        fields = ['urlid','name', 'total_votes']

    def get_total_votes(self, obj):
        votes_queryset = self.context.get("votes_queryset")
        return votes_queryset.filter(chosenOption=obj).count()
