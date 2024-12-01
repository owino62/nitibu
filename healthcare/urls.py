from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('illness/<id>/',views.illness,name='illness'),
    path('create_ugonjwa/',views.create_ugonjwa,name='create_ugonjwa'),
    path('typhoid/',views.typhoid_view, name='typhoid'),
    path('cholera/',views.cholera_view, name='cholera'),
    path('bilharzia/',views.bilharzia_view, name='bilharzia'),
    path('malaria/',views.malaria_view, name='malaria'),
    path('gonorrhoea/',views.gonorrhoea_view, name='gonorrhoea'),
    path('syphilis/',views.syphilis_view, name='syphilis'),
    path('genital_herpes/',views.herpes_view, name='genital_herpes'),
    #path('symptoms/',views.symptoms,name='symptoms'),
    #path('create_illness/', views.create_illness, name='create_illness'),
    path('tengeneza_illness/', views.tengeneza_illness, name='tengeneza_illness'),
    path('illness/<str:illness_name>/', views.illness_detail_view, name='illness_detail'),
    path('search/',views.search_view,name='search'),
    path('shop_now', views.shop_now, name='shop_now'),
    path('tengeneza_product/', views.tengeneza_product, name='tengeneza_product'),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
]