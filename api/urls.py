from django.urls import path
from . import views

urlpatterns = [
    path('',views.allCategories,name='categories'),
    path('category/<id>',views.categoryById,name='categoryById'),
    path('products/<catID>/',views.productsByCatID,name='productsByCatID'),
    path('product/<id>/',views.productsByID,name='productsByID'),
    path('products',views.ProductsRecordsView.as_view(),name='products'),
    path('addToken', views.addToken,name='addToken'),
    path('allSeasons', views.allSeasons,name='allSeasons'),
    path('season/<id>', views.seasonById,name='season'),
    path('bannersBySeason/<SeasonID>/', views.bannersByID,name='bannersBySeason'),
    path('banners', views.allBanners,name='banners'),
    path('banner/<id>', views.bannerById,name='banner'),
    path('deals', views.deals,name='deals'),
    path('offers', views.offers,name='offers'),
    path('recomm', views.recommended,name='recomm'),
    path('special', views.special,name='special'),
    path('order', views.order,name='special'),
    path('search/<str:query>', views.search,name='search'),
    path('receipt', views.some_view,name='receipt'),
    path('pdf/', views.GeneratePdf.as_view()),
    path('order', views.add_order, name="order"),
    path('check', views.check, name="order"),
]
