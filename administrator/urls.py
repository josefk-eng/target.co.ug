from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='index'),
    path('product',views.products_view, name='product'),
    path('depts',views.dept_view, name='depts'),
    path('banners_view',views.banners_view, name='banners_view'),
    path('uploadcsv',views.uploadcsv, name='uploadcsv'),
    path('update_product/<int:pk>', views.ProductUpdateView.as_view(), name='update_product'),
    path('create_banner/', views.BannerCreateView.as_view(), name='create_banner'),
]