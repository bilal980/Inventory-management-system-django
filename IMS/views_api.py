from setting.models import BusinessDetail
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from setting.models import BusinessDetail


@csrf_exempt
def theme(request):
    if request.method=="POST":
        if request.POST.get('theme')=='dark':
            request.session['theme'] = 'dark'
        else:
            request.session['theme']='light'
    cache.clear()
    return JsonResponse({'theme': request.session.setdefault('theme','light')})

