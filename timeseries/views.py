from django.shortcuts import render, HttpResponse

from random import random

from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource
from bokeh.models.glyphs import VBar
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc, show
from bokeh.embed import file_html
from bokeh.resources import CDN

import pandas as pd
import os
from calendar import monthrange


# from webdashboard import settings


def get_news_by_date(df, date):
    """

    :param date:
    :param df:
    :return:
    """
    return len(df[df.date_published > date][df.date_published < date + 'Z'])


def get_news_by_month(df, year, month):
    """

    :param year:
    :param month:
    :param df:
    :return:
    """
    return [get_news_by_date(df, '{}-{:0>2}-{:0>2}'.format(year, month, day))
            for day in range(1, monthrange(int(year), int(month))[1] + 1)]


def get_news_by_year(df, year):
    """

    :param year:
    :param df:
    :return:
    """
    return [get_news_by_month(df, '{}-{:0>2}'.format(year, month)) for month in range(1, 13)]


def home(request):
    df = pd.read_excel(
        io=str(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'timeseries/dados.xlsx')),
        sheetname='Sheet1',
        index_col=None,
    )
    datas = df.date_published
    new_datas = {}
    for d in datas:
        # year = d[:4], month = d[5:7], day = d[8:10]. Good luck!
        new_datas.setdefault(d[:4], {}).setdefault(d[5:7], []).append(d[8:10])

    candidatos = df.candidato.unique()

    # create a plot and style its properties
    p = figure(y_range=(0, 250), x_range=(0, 31), toolbar_location=None)
    p.vbar(x=range(1, monthrange(2016, 10)[1] + 1), top=get_news_by_month(df, '2016', '10'), width=0.5)
    # p.border_fill_color = 'black'
    # p.background_fill_color = 'black'
    # p.outline_line_color = None
    # p.grid.grid_line_color = None

    # def callback_crivella():
    #     global i
    #     candidato = u'Crivella'
    #
    #     for j in datas:
    #         new_data = dict()
    #         new_data['x'] = j[:10]
    #         new_data['y'] = len(
    #             df[df.candidato == candidato][df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
    #         )
    #         ds.data = new_data
    #
    #
    # def callback_freixo():
    #     global i
    #     candidato = u'Freixo'
    #     datas = df.date_published.unique()
    #
    #     for j in datas:
    #         new_data = dict()
    #         new_data['x'] = j[:10]
    #         new_data['y'] = len(
    #             df[df.candidato == candidato][df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
    #         )
    #         ds.data = new_data
    #
    #
    # def callback_both():
    #     global i
    #     datas = df.date_published.unique()
    #
    #     for j in datas:
    #         new_data = dict()
    #         new_data['x'] = j[:10]
    #         new_data['y'] = len(
    #             df[df.date_published > j[:10]][df.date_published < (j[:10] + u'Z')]
    #         )
    #         ds.data = new_data


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
    return HttpResponse(file_html(p, CDN, "my plot"))
