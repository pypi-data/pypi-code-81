"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

"""djangoldp project URL Configuration"""
from django.conf.urls import url,include
from djangoldp.models import Model
from djangoldp_polls.views import TotalVotes, CanVoteOnPollViewSet
from djangoldp_polls.models import PollOption

urlpatterns = [
    url(r'^polls/total_votes/(?P<pk>[0-9]+)/', TotalVotes.urls(model_prefix='total-votes',
                                                                model=PollOption,
                                                                permission_classes=Model.get_meta(PollOption,
                                                                                                  'permission_classes',
                                                                                                  []),
                                                                fields=Model.get_meta(PollOption, 'serializer_fields',[]),
                                                                nested_fields=Model.get_meta(PollOption, 'nested_fields', []))),
    url(r'^polls/(?P<pk>[0-9]+)/can_vote/', CanVoteOnPollViewSet.as_view())
]
