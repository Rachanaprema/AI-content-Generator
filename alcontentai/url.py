from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('comparefilecheck/', views.comparefilecheck, name='comparefilecheck'),
    path('comparetextCheck/', views.comparetextCheck, name='comparetextCheck'),
    path('documentUpload/', views.documentUpload, name='documentUpload'),
    path('textUpload/', views.textUpload, name='textUpload'),
    path('help/', views.helpus, name='helpus'),
    path('contactus/', views.contactus, name='contactus'),
    path('filetest/', views.filetest, name='filetest'),
    path('twofiletest1/', views.twofiletest1, name='twofiletest1'),
    path('twofilecompare1/', views.twofilecompare1, name='twofilecompare1'),
    path('test/', views.test, name='test'),
    path('summary_generator/', views.summary_generator, name='summary_generator'),
    path('websearch/', views.websearch, name='websearch'),
    path('image_analysis/', views.image_analysis, name='image_analysis'),
    path('text_helper/', views.text_helper, name='text_helper'),
]
