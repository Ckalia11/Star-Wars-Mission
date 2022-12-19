from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadJsonFileForm
from .functions import traverse_graph, compute_probability_success, get_millennium_data, get_empire_data, get_routes
import json
import click

def upload_file(request):
    context = {}
    if request.method == 'POST':
        form = UploadJsonFileForm(request.POST, request.FILES)
        empire_file = request.FILES.get("file")
        countdown, hunting = get_empire_data(empire_file)
        autonomy, departure, arrival, routes_db = get_millennium_data()
        routes = get_routes(routes_db)
        bounty_encounters = traverse_graph(routes, departure, arrival, countdown, hunting, autonomy)
        probability_success = compute_probability_success(bounty_encounters)
        context["probability_success"] =  str(100 * probability_success) + "%"
    else:
        form = UploadJsonFileForm()
        context['form'] = form
    context['request'] = request
    return render(request, 'singlepage/upload.html', context)


