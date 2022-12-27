from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import UploadJsonFileForm
from .functions import get_probability_success
import json
import os

# specify path to millennium-falcon.json file
app_dir = "singlepage"
example_folder = "example1"

files_dir_path = os.path.join(app_dir, "json_files", "examples", example_folder)
millennium_file = os.path.join(files_dir_path, "millennium-falcon.json")


def upload_file(request):
    context = {}
    if request.method == 'POST':
        form = UploadJsonFileForm(request.POST, request.FILES)
        if form.is_valid():
            empire_file = form.cleaned_data.get("file")
        probability_success = get_probability_success(millennium_file, empire_file)
        formatted_probability = f"{int(100 * probability_success)} %"
        return JsonResponse(
            {
            "probability_success": formatted_probability
            }
        )
    else:
        form = UploadJsonFileForm()
        context['form'] = form
    return render(request, 'singlepage/upload.html', context)


