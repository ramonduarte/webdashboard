from __future__ import unicode_literals
from cms.models import CMSPlugin
from django.db import models


class TimeseriesPluginModel(CMSPlugin):

    def __unicode__(self):
        return ''
