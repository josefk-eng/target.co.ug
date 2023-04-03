from functools import reduce

from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from administrator.models import Product, Category, Season, Banner, Order
from .Serializers import ItemSerializer, CategorySerializer, SeasonSerializer, BannerSerializer, OrderSerializer
from api.Serializers import TokenSerializer
from .models import UserToken
from django.shortcuts import get_object_or_404
import operator
from . import PagingStyle
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf
from django.template.loader import render_to_string


# Create your views here.
@api_view(['GET'])
def productsByCatID(request, catID):
    myCat = Category.objects.get(id=catID)
    items = Product.objects.filter(category=myCat)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productsByID(request, id):
    item = get_object_or_404(Product, id=id)
    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['GET'])
def allProducts(request, page):
    item = Product.objects.filter()[:10]
    serializer = ItemSerializer(item, many=True)
    return Response(serializer.data)


class ProductsRecordsView(ListAPIView):
    # pagination_class = PagingStyle.CustomPagination
    queryset = Product.objects.all().order_by('category')
    serializer_class = ItemSerializer


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
def bannerById(request, id):
    banner = Banner.objects.get(id=id)
    serializer = BannerSerializer(banner)
    return Response(serializer.data)


@api_view(['GET'])
def deals(request):
    deals = Product.objects.filter(tag__icontains="deal")
    serializer = ItemSerializer(deals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def offers(request):
    offers = Product.objects.filter(tag__icontains="offer")
    serializer = ItemSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def special(request):
    special = Product.objects.filter(tag__icontains="special")
    serializer = ItemSerializer(special, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({"Error": "Data is not valid"})


@api_view(['GET'])
def recommended(request):
    strings = ['deal', 'offer', 'special']
    condition = reduce(operator.and_, [Q(tag__icontains=s) for s in strings])
    recommend = Product.objects.filter(condition)  # [:10]
    serializer = ItemSerializer(recommend, many=True)
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
    category = Category.objects.filter(name__icontains=query)
    products = Product.objects.filter(name__icontains=query)
    cat_serializer = CategorySerializer(category, many=True)
    prod_serializer = ItemSerializer(products, many=True)
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
        data = Order.objects.get(pk=3)
        # getting the template
        pdf = html_to_pdf('result.html', {'order': data})

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


@api_view(['POST'])
def add_order(request):
    serializer = OrderSerializer(data=request.body)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors)


@api_view(['GET'])
def check(request):
    return Response(0)
