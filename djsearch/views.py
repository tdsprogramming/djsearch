from functools import reduce
import operator

from django.shortcuts import render
from django.conf import settings
from django.apps import apps
from django.db.models import Q
from django.http import JsonResponse
from .utils import django_search_serializer

def search(request):
    q = request.GET['q']
    models = apps.get_models()
    context = {
        'results':{}
    }

    # Loop through all models in INSTALLED_APPS
    for m in models:
        # Checks if the 'search_fields' attribute is defined.
        # If the 'search_fields' attribute is not defined, it will not search
        # the model
        if hasattr(m, 'djsearch_fields'):
            filter_kwargs = []

            # initialize an empty queryset for the model in question (m)
            qs = m.objects.none()

            # go through each field
            for s in m.djsearch_fields:

                # split words in search query to search for each one individually
                for word in q.split(' '):
                    filter_kwargs.append(Q(**{s + '__contains': word}))
                    qs = qs | m.objects.filter(reduce(operator.or_, filter_kwargs))
            for i in qs.distinct():
                context['results'][i.__str__()] = django_search_serializer(i)
    return JsonResponse(context)
