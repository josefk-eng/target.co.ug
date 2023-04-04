import io
import operator
from functools import reduce

from django.db.models import Q
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

from administrator import models
from api.Serializers import TokenSerializer
from . import Serializers
from .models import UserToken
from .process import html_to_pdf
from .utils import custom_exception_handler


# Create your views here.
@api_view(['GET'])
def productsByCatID(request, catID):
    myCat = models.Category.objects.get(id=catID)
    items = models.Product.objects.filter(category=myCat)
    serializer = Serializers.ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productsByID(request, id):
    item = get_object_or_404(models.Product, id=id)
    serializer = Serializers.ItemSerializer(item)
    return Response(serializer.data)


@api_view(['GET'])
def allProducts(request, page):
    item = models.Product.objects.filter()[:10]
    serializer = Serializers.ItemSerializer(item, many=True)
    return Response(serializer.data)


class ProductsRecordsView(ListAPIView):
    # pagination_class = PagingStyle.CustomPagination
    queryset = models.Product.objects.all().order_by('category')
    serializer_class = Serializers.ItemSerializer


@api_view(['GET'])
def allCategories(request):
    cats = models.Category.objects.all()
    serializer = Serializers.CategorySerializer(cats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def categoryById(request, id):
    cate = get_object_or_404(models.Category, id=id)
    serializer = Serializers.CategorySerializer(cate)
    return Response(serializer.data)


@api_view(['GET'])
def allSeasons(request):
    seas = models.Season.objects.all()
    serializer = Serializers.SeasonSerializer(seas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def seasonById(request, id):
    season = models.Season.objects.get(id=id)
    serializer = Serializers.SeasonSerializer(season)
    return Response(serializer.data)


@api_view(['GET'])
def bannersByID(request, SeasonID):
    banners = models.Banner.objects.filter(season=SeasonID)
    serializer = Serializers.BannerSerializer(banners, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def allBanners(request):
    banners = models.Banner.objects.all()
    serializer = Serializers.BannerSerializer(banners, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bannerById(request, id):
    banner = models.Banner.objects.get(id=id)
    serializer = Serializers.BannerSerializer(banner)
    return Response(serializer.data)


@api_view(['GET'])
def deals(request):
    deals = models.Product.objects.filter(tag__icontains="deal")
    serializer = Serializers.ItemSerializer(deals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def offers(request):
    offers = models.Product.objects.filter(tag__icontains="offer")
    serializer = Serializers.ItemSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def special(request):
    special = models.Product.objects.filter(tag__icontains="special")
    serializer = Serializers.ItemSerializer(special, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def order(request):
    serializer = Serializers.OrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({"Error": "Data is not valid"})


@api_view(['GET'])
def recommended(request):
    strings = ['deal', 'offer', 'special']
    condition = reduce(operator.and_, [Q(tag__icontains=s) for s in strings])
    recommend = models.Product.objects.filter(condition)  # [:10]
    serializer = Serializers.ItemSerializer(recommend, many=True)
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
    else:
        serializer = TokenSerializer(data=token)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print(serializer.errors)


class SearchResult:
    def __init__(self, cats, prods):
        self.depts = cats
        self.products = prods


@api_view(['GET'])
def search(request, query):
    category = models.Category.objects.filter(name__icontains=query)
    products = models.Product.objects.filter(name__icontains=query)
    cat_serializer = Serializers.CategorySerializer(category, many=True)
    prod_serializer = Serializers.ItemSerializer(products, many=True)
    return Response({
        "depts": cat_serializer.data,
        "products": prod_serializer.data
    })


def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = models.Order.objects.get(pk=3)
        # getting the template
        pdf = html_to_pdf('result.html', {'order': data})

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


@api_view(['POST'])
def add_order(request):
    serializer = Serializers.OrderSerializer(data=request.body)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors)


@api_view(['GET'])
def check(request):
    return Response(0)


@api_view(['POST'])
def addressing(request):
    query = request.data["type"]
    quota = request.data["quota"]
    if query == "district":
        districts = models.District.objects.all()
        serializer = Serializers.DistrictSerializer(districts,many=True)
        return Response(serializer.data)
    elif query == "division":
        division = models.Division.objects.filter(district=quota)
        serializer = Serializers.DivisionSerializer(division, many=True)
        return Response(serializer.data)
    elif query == "parish":
        parish = models.Parish.objects.filter(division=quota)
        serializer = Serializers.ParishSerializer(parish, many=True)
        return Response(serializer.data)
    elif query == "village":
        village = models.Village.objects.filter(parish=quota)
        serializer = Serializers.VillageSerializer(village,many=True)
        return Response(serializer.data)
    elif query == "street":
        street = models.Street.objects.filter(village=quota)
        serializer = Serializers.StreetSerializer(street,many=True)
        return Response(serializer.data)
    else:
        return custom_exception_handler(APIException(detail="Unknown AddressType", code=status.HTTP_400_BAD_REQUEST), context={"request": request})
