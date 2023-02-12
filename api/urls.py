from django.urls import path
from . import views

urlpatterns = [
    path('',views.allCategories,name='categories'),
    path('category/<id>',views.categoryById,name='categoryById'),
    path('products/<catID>/',views.productsByCatID,name='productsByCatID'),
    path('product/<id>/',views.productsByID,name='productsByID'),
    path('products',views.allProducts,name='products'),
    path('addToken', views.addToken,name='addToken'),
    path('allSeasons', views.allSeasons,name='allSeasons'),
    path('season/<id>', views.seasonById,name='season'),
    path('bannersBySeason/<SeasonID>/', views.bannersByID,name='bannersBySeason'),
    path('banners', views.allBanners,name='banners'),
    path('banner/<id>', views.bannerById,name='banner'),
]
