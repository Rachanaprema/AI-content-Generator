from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comparetextCheck/', views.twofiletest1, name='comparetextCheck'),
    path('comparefilecheck/', views.twofilecompare1, name='comparefilecheck'),
    path('helpus/', views.helpus, name='helpus'),
    path('contactus/', views.contactus, name='contactus'),
    path('text_helper/', views.text_helper, name='text_helper'),
    path('image_analysis/', views.image_analysis, name='image_analysis'),
    path('summary_generator/', views.summary_generator, name='summary_generator'),
    path('websearch/', views.websearch, name='websearch'),
]
