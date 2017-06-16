from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from timeseries.models import TimeseriesPluginModel
from django.utils.translation import ugettext as _


class TimeseriesPluginPublisher(CMSPluginBase):
    model = TimeseriesPluginModel  # model where plugin data are saved
    module = _("Timeseries")
    name = _("Timeseries Plugin")  # name of the plugin in the interface
    render_template = "timeseries/timeseries_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

plugin_pool.register_plugin(TimeseriesPluginPublisher)  # register the plugin
