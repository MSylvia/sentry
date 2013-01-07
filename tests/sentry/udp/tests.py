# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User
from sentry.models import Project, Team, TeamProject
from sentry.utils.auth import get_auth_header
from sentry.services.udp import SentryUDPServer

from sentry.testutils import TestCase


class SentryUDPTest(TestCase):
    def setUp(self):
        self.address = (('0.0.0.0', 0))
        self.server = SentryUDPServer(*self.address)
        self.user = User.objects.create(username='coreapi')
        self.project = Project.objects.create(owner=self.user, name='Foo')
        self.team = Team.objects.create(owner=self.user, name='Foo')
        TeamProject.objects.create(team=self.team, project=self.project)
        self.pm = self.team.member_set.get(user=self.user)
        self.pk = self.project.key_set.create(project=self.project, user=self.user)

    def test_failure(self):
        self.assertNotEquals(None, self.server.handle('deadbeef', self.address))

    def test_success(self):
        data = {'message': 'hello', 'server_name': 'not_dcramer.local', 'level': 40, 'site': 'not_a_real_site'}
        message = self._makeMessage(data)
        header = get_auth_header('udpTest', api_key=self.pk.public_key, secret_key=self.pk.secret_key)
        packet = header + '\n\n' + message
        self.assertEquals(None, self.server.handle(packet, self.address))
