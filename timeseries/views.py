from django.shortcuts import render, Http404
from webdashboard.settings import STATIC_ROOT
import os
from datetime import datetime


def home(request):
    if request.method == 'GET':
        context = {
            'bokeh_app_src': 'http://http://104.236.5.21:5006/sources',
            'bokeh_app_width': 800,
            'bokeh_app_height': 800,
        }
        return render(request, 'timeseries/index.html', context=context)
    else:
        return Http404
