from django.shortcuts import render

# Create your views here.
from random import random

from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

import pandas as pd
import os
# from webdashboard import settings


df = pd.read_excel(
    io=str(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'timeseries/dados.xlsx')),
    sheetname='Sheet1',
    index_col=None,
)
datas = df.date_published.unique()
datas = [str(d[:10]) for d in datas][:10]
datas = list(set(datas))
source = ColumnDataSource(
    dict(top=[len(df[df.date_published > d][df.date_published < (d + u'Z')]) for d in datas], x=datas[0])
)

# create a plot and style its properties
p = figure(y_range=(0, 100), x_range=datas, toolbar_location=None)
glyph = VBar(x=datas, width=1, top=100)
p.add_glyph(source, glyph)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None


# add a text renderer to our plot (no data yet)
# r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
#            text_baseline="middle", text_align="center")

i = 0

# ds = r.data_source

def callback_crivella():
    global i
    candidato = u'Crivella'

    for j in datas:
        new_data = dict()
        new_data['x'] = j[:10]
        new_data['y'] = len(
            df[df.candidato == candidato][df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
        )
        ds.data = new_data


def callback_freixo():
    global i
    candidato = u'Freixo'
    datas = df.date_published.unique()

    for j in datas:
        new_data = dict()
        new_data['x'] = j[:10]
        new_data['y'] = len(
            df[df.candidato == candidato][df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
        )
        ds.data = new_data


def callback_both():
    global i
    datas = df.date_published.unique()

    for j in datas:
        new_data = dict()
        new_data['x'] = j[:10]
        new_data['y'] = len(
            df[df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
        )
        ds.data = new_data

# btn_crivella = Button(label='Crivella')
# btn_crivella.on_click(callback_crivella())
#
# btn_freixo = Button(label='Freixo')
# btn_freixo.on_click(callback_freixo())
#
# btn_both = Button(label='Ambos')
# btn_both.on_click(callback_both())

# # create a callback that will add a number in a random location
# def callback():
#     global i
#
#     # BEST PRACTICE --- update .data in one step with a new dict
#     new_data = dict()
#     new_data['x'] = ds.data['x'] + [random() * 70 + 15]
#     new_data['y'] = ds.data['y'] + [random() * 70 + 15]
#     new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i % 3]]
#     new_data['text'] = ds.data['text'] + [str(i)]
#     ds.data = new_data
#
#     i = i + 1
#
#
# # add a button widget and configure with the call back
# button = Button(label="Press Me")
# button.on_click(callback)
#
# # put the button and plot in a layout and add to the document
# curdoc().add_root(column(button, p))
curdoc().add_root(column(p))
