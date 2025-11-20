from django.urls import path, re_path
from django.conf import settings
from . import views
from django.views.static import serve

 


urlpatterns = [ 
    path('',views.home,name="home"),        
    path('home/',views.home,name="home"),  
    path('about_us/',views.about_us,name='about_us'),
    path('projects/',views.projects,name='projects'),
    path('contact/',views.contact,name='contact'),
    path('contact_send/', views.contact_send, name='contact_send'),
    path('donate/',views.donate,name='donate'),
    # urls.py
    path('process_donation/', views.process_donation, name="process_donation"),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]


