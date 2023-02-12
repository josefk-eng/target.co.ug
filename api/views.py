from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from administrator.models import Product, Category, Season, Banner
from .Serializers import ItemSerializer, CategorySerializer, SeasonSerializer, BannerSerializer
from api.Serializers import TokenSerializer
from .models import UserToken
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(['GET'])
def productsByCatID(request, catID):
    myCat = Category.objects.get(id=catID)
    items = Product.objects.filter(category=myCat)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productsByID(request, id):
    item = get_object_or_404(Product,id=id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)

@api_view(['GET'])
def allProducts(request):
    item = Product.objects.filter()
    serializer = ItemSerializer(item, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def allCategories(request):
    cats = Category.objects.all()
    serializer = CategorySerializer(cats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def categoryById(request, id):
    cate = get_object_or_404(Category, id=id)
    serializer = CategorySerializer(cate)
    return Response(serializer.data)


@api_view(['GET'])
def allSeasons(request):
    seas = Season.objects.all()
    serializer = SeasonSerializer(seas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def seasonById(request, id):
    season = Season.objects.get(id=id)
    serializer = SeasonSerializer(season)
    return Response(serializer.data)

@api_view(['GET'])
def bannersByID(request, SeasonID):
    banners = Banner.objects.filter(season=SeasonID)
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def allBanners(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def bannerById(request,id):
    banner = Banner.objects.get(id=id)
    serializer = BannerSerializer(banner)
    return Response(serializer.data)


@api_view(['POST'])
def addToken(request):
    token = None
    try:
        token = UserToken.objects.get(deviceId=request.POST["deviceId"])
        token.token = request.POST["token"]
        token.save()
    except:
        print("New ID")

    if token is None:
        serializer = TokenSerializer(data=request.data)
    else: serializer = TokenSerializer(data=token)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print(serializer.errors)