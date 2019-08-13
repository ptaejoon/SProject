from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    #path('', views.post_list, name = 'post_list'),
    path('pdList/',views.productListAPI.as_view(),name='product_list'),
    path('productSpec/',views.productSPecAPI.as_view(),name='product_spec'),

]