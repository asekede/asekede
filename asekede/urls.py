from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.defaults import page_not_found

urlpatterns = [
    path('', TemplateView.as_view(template_name='about_me.html'), name='about_me'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
]
