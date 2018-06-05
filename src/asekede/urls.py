from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='about_me.html'), name='about_me'),
    path('blog/', include('blog.urls')),
    path('djga/', include('google_analytics.urls')),
    path('admin/', admin.site.urls)
]
