from django.shortcuts import HttpResponse, get_object_or_404

# from .models import Parent


def index(request):
    # p = get_object_or_404(Parent, slug='adam').slug
    return HttpResponse(
        f'{1+1}')
