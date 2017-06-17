from django.shortcuts import render, Http404


# from webdashboard import settings

def home(request):
    if request.method == 'GET':
        context = {
            'bokeh_app_src': 'http://localhost:5006/dashboard',
            'bokeh_app_width': 800,
            'bokeh_app_height': 400,
        }
        return render(request, 'timeseries/index.html', context=context)
    else:
        return Http404
