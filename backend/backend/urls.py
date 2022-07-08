from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from backend.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/',
         TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
        ] + urlpatterns
