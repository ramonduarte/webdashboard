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


# noinspection PyShadowingNames
def get_news_by_date(df, date):
    """

    :param date:
    :param df:
    :return:
    """
    return len(df[df.date_published > date][df.date_published < date + 'Z'])


# noinspection PyShadowingNames
def get_news_by_month(df, year, month):
    """

    :param year:
    :param month:
    :param df:
    :return:
    """
    return [get_news_by_date(df, '{}-{:0>2}-{:0>2}'.format(year, month, day))
            for day in range(1, monthrange(int(year), int(month))[1] + 1)]


# noinspection PyShadowingNames
def get_news_by_year(df, year):
    """

    :param year:
    :param df:
    :return:
    """
    return [get_news_by_month(df, '{}-{:0>2}'.format(year, month)) for month in range(1, 13)]


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

candidatos = [u'Todos'] + sorted(list(df.candidato.unique()))

# Interactive controls
candidato_choice = Select(title='Candidato', options=candidatos)

# Hover tooltips can actually be defined before being instantiated
hover = HoverTool(tooltips=[
    ('Noticias', '@top'),
    ('Candidato', '@candidato')
])

source = ColumnDataSource(data=dict(
    x=range(1, monthrange(2016, 10)[1] + 1),
    top=get_news_by_month(df, '2016', '10'),
    # color=[],
    candidato=[u'Todos']*31,
    # noticias=[],
    # alpha=[],
))

# Creating and styling a plot comes after all interactive controls have been set
p = figure(y_range=(0, 250), x_range=(0, 31), toolbar_location=None, tools=[hover])
p.vbar(
    x=range(1, monthrange(2016, 10)[1] + 1),
    top=get_news_by_month(df, '2016', '10'),
    width=0.5,
    source=source,
)


#
def select_news():
    candidato_value = candidato_choice.value  # selected by the end user
    both = (candidato_value == u'Todos')
    selected = df[
        (df.candidato == candidato_value) |
        both
        ]
    return selected


def update():
    dataframe = select_news()
    days_in_month = monthrange(2016, 10)[1]
    candidato = list(dataframe.candidato.unique())
    if len(candidato) != 1:
        candidato = [u'Todos']
    candidato *= days_in_month

    source.data = dict(
        x=range(1, days_in_month + 1),
        top=get_news_by_month(dataframe, '2016', '10'),
        candidato=candidato,
    )


controls = [
    candidato_choice,
]
for c in controls:
    c.on_change('value', lambda attr, old, new: update())

sizing_mode = 'fixed'

inputs = widgetbox(*controls, sizing_mode=sizing_mode)
lay_out = layout([
    [inputs, p]
], sizing_mode=sizing_mode)

# open a session to keep our local document in sync with server
curdoc().add_root(lay_out)
# session = push_session(curdoc())
update()
curdoc().add_periodic_callback(update, 50)

# session.loop_until_closed()  # run forever
