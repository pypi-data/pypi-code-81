import uuid
import json
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.test import APITestCase, APIClient

from djangoldp_polls.models import Poll, PollOption, Vote
from djangoldp_polls.tests.models import User


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.setUpLoggedInUser()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def setUpPoll(self):
        self.poll_option_a = PollOption.objects.create(name='Yes')
        self.poll_option_b = PollOption.objects.create(name='No')
        self.poll = self._get_poll('Test')

    def _get_poll(self, title):
        poll = Poll.objects.create(endDate=datetime.now(), title=title, hostingOrganisation='Test',
                                   shortDescription='Hello', longDescription='Hello World')
        poll.pollOptions.add(self.poll_option_a, self.poll_option_b)
        return poll

    def _get_poll_post_request(self, option):
        return {
            '@context': settings.LDP_RDF_CONTEXT,
            'choiceValue': '',
            'chosenOption': {'@id': option.urlid}
        }

    def test_get_total_votes_cache(self):
        self.setUpPoll()
        response = self.client.get('/polloptions/{}/'.format(self.poll_option_a.pk))
        self.assertFalse('total_votes' in response.data)

        response = self.client.get('/polls/total_votes/{}/'.format(self.poll.pk))
        print(str(response.data))
        self.assertTrue('total_votes' in response.data['ldp:contains'][0])
        self.assertTrue('total_votes' in response.data['ldp:contains'][1])

    def test_can_vote_view(self):
        # I should be able to vote
        self.setUpPoll()
        response = self.client.get('/polls/{}/can_vote/'.format(self.poll.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, True)

        # I should not be able to vote
        Vote.objects.create(user=self.user, relatedPoll=self.poll, chosenOption=self.poll_option_a)
        response = self.client.get('/polls/{}/can_vote/'.format(self.poll.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, False)

    def test_post_vote(self):
        # post on one poll
        self.setUpPoll()
        body = self._get_poll_post_request(self.poll_option_a)
        response = self.client.post('/polls/{}/votes/'.format(self.poll.pk), json.dumps(body), content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

        # post on another
        other_poll = self._get_poll('Second Poll')
        body = self._get_poll_post_request(self.poll_option_b)
        response = self.client.post('/polls/{}/votes/'.format(other_poll.pk), json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

    def test_post_vote_duplicate(self):
        # post once
        self.setUpPoll()
        body = self._get_poll_post_request(self.poll_option_a)
        response = self.client.post('/polls/{}/votes/'.format(self.poll.pk), json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 201)

        # post again - should be rejected
        body = self._get_poll_post_request(self.poll_option_b)
        response = self.client.post('/polls/{}/votes/'.format(self.poll.pk), json.dumps(body),
                                    content_type='application/ld+json')
        self.assertEqual(response.status_code, 400)
