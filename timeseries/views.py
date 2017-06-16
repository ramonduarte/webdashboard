from django.shortcuts import render, Http404
from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource, HoverTool
from bokeh.models.glyphs import VBar
from bokeh.models.widgets import Slider, Select
from bokeh.palettes import RdYlBu3
from bokeh.layouts import layout, widgetbox
from bokeh.plotting import figure, curdoc, show, output_file
from bokeh.embed import file_html, components
from bokeh.resources import CDN
from bokeh.client import push_session

import pandas as pd
import os
from calendar import monthrange


# from webdashboard import settings

def home(request):
    if request.method == 'GET':
        context = {
            'bokeh_app_src': 'http://localhost:5006/dashboard',
            'bokeh_app_width': 1024,
            'bokeh_app_height': 800,
        }
        return render(request, 'timeseries/index.html', context=context)
    else:
        return Http404
