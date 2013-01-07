# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User
from sentry.constants import MEMBER_OWNER
from sentry.models import Team

from sentry.testutils import TestCase


class SentrySignalTest(TestCase):
    def test_create_team_member_for_owner(self):
        user = User.objects.create(username='foo')
        team = Team.objects.create(name='foo', slug='foo', owner=user)
        self.assertTrue(team.member_set.filter(user=user, type=MEMBER_OWNER).exists())
