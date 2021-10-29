import json
import re
from collections import OrderedDict

import Levenshtein
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm
from .models import *
from .pkmn import PkmnDict
from .serializers import PkmnSerializer


def main(request):
    # Main web page
    # If no json db is loaded, the user is redirected to the load page
    # If already loaded, a simple page is shown

    loadedObjects = PkmnModel.objects
    if loadedObjects.count() > 0:
        return HttpResponseRedirect('/show/')
    else:
        return HttpResponseRedirect('/load/')


def load(request):
    # Loading web page
    # The user can load the json db from here
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Extracting binary array
            bin_data = request.FILES['file'].file.read()

            # Extracting a list of dictionaries
            pkmn_list = PkmnDict.read_data(bin_data)

            # Load the dictionaries to the DB
            for pkmn_as_dict in pkmn_list:
                pkmn_as_dict.add_to_db()

            return HttpResponseRedirect('/show/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def show(request):
    # Simple overview web page
    # The user can see from here the loaded data
    loadedObjects = PkmnModel.objects
    if loadedObjects.count() == 0:
        return HttpResponseRedirect('/load/')

    return render(request, 'show.html', {
        'pokemons': PkmnModel.objects.all(),
    })


def pokemon(request):
    # Create one API endpoint /pokemon
    #   This API endpoint should be searchable, filterable and paginatable
    #   Search: name
    #       Bonus: implement fuzzy search using Levenshtein distance
    #   Filter: HP, Attack & Defense
    #       e.g. /pokemon?hp[gte]=100&defense[lte]=200
    #   Pagination: e.g. /pokemon?page=1

    query_res = PkmnModel.objects.all()
    paginate = False
    params = list(request.GET.keys())
    res_list_distance = None

    status = 200

    ########################
    # Parse parameters
    for param in params:
        modifier = None
        m = re.match(r"^(.+)\[(.+)\]$", param)
        value = request.GET[param]
        if m != None:
            param = m.group(1)
            modifier = m.group(2)

        if param == "page":
            paginate = True
            page = int(request.GET["page"])

        elif param == "name":
            query_res = query_res.filter(name__iexact=value)

        elif param == "type":
            query_res = query_res.filter(type1=value) | query_res.filter(
                type2=value)

        elif param == "search":
            res_list_distance = {}
            for n in [q.name for q in query_res.all()]:
                distance = Levenshtein.distance(n.lower(), value.lower())
                res_list_distance[n] = distance

        else:
            for field in PkmnModel._meta.fields:
                if field.name.lower() == param.lower():
                    param = field.name
                    if modifier:
                        param = param + "__" + modifier

                    try:
                        query_res = query_res.filter(**{param: value})
                    except:
                        # Malformed query
                        status = 400
                        query_res = []
                    break

            else:
                # Invalid parameter
                status = 400
                query_res = []

    ########################
    # Reorder by search distance
    if res_list_distance != None:
        query_res = list(query_res)
        query_res.sort(key=lambda obj: res_list_distance[obj.name])
        query_res = query_res

    ########################
    # Serialize
    res_list = []
    for instance in query_res:
        as_dict = PkmnSerializer(instance).data
        res_list.append(as_dict)

    ########################
    # Add metadata
    query_info = OrderedDict()
    query_info["count"] = len(res_list)

    ########################
    # Paging
    if paginate:
        paging = Paginator(res_list, 10)
        query_info["page"] = page
        query_info["num_pages"] = paging.num_pages
        if page not in paging.page_range:
            status = 400
            res_list = []
        else:
            res_list = paging.page(page).object_list

    query_info["result"] = res_list
    response = json.dumps(query_info, indent=2)

    return HttpResponse(response,
                        status=status,
                        content_type="application/json")
