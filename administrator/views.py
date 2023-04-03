from django.shortcuts import render, redirect
from . import models
import csv
from .forms import CsvForm, ItemForm, BannerForm
from django.shortcuts import get_object_or_404
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    return redirect('login')


def products_view(request):
    if request.user.is_authenticated:
        items = models.Product.objects.all()
        csvForm = CsvForm()
        return render(request, 'products.html',
                      {'products': items,'csvform': csvForm})
    else:
        return redirect('login')


def orders_view(request):
    if request.user.is_authenticated:
        orders = models.Order.objects.all()
        return render(request, 'orders.html',
                      {'products': orders,})
    else:
        return redirect('login')


def dept_view(request):
    if request.user.is_authenticated:
        depts = models.Category.objects.all()
        return render(request, 'department.html', {'depts':depts})
    else:
        return redirect('login')


def banners_view(request):
    if request.user.is_authenticated:
        allBanners = models.Banner.objects.all()
        return render(request, 'banners.html', {'banners': allBanners})
    else:
        return redirect('login')



def uploadcsv(request):
    csvForm = CsvForm(request.POST or None, request.FILES or None)
    items = models.Product.objects.all()
    categories = models.Category.objects.all()
    user = request.user
    form = ItemForm()
    if csvForm.is_valid():
        csvForm.save()
        csvForm = CsvForm()
        obj = models.Csv.objects.get(is_activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i == 0:
                    pass
                else:
                    number = row[0]
                    stock_id = row[1]
                    tmp = row[2]
                    try:
                        serial_number = float(tmp)
                    except:
                        serial_number = 0
                    name = row[3].upper()
                    quantity = row[4]
                    cost_price = row[5]
                    price = row[6]
                    cat, created = models.Category.objects.get_or_create(
                        name=row[8]
                    )
                    department = models.Employee.objects.get(id=user.id).department
                    availability = quantity != "0"
                    models.Product.objects.create(
                        number=number,
                        stockId=stock_id,
                        serialNumber=serial_number,
                        name=name,
                        quantity=quantity,
                        cost_price=cost_price,
                        price=price,
                        department=department,
                        category=cat,
                        availability=availability
                    )
                    # print(row)
                    # print(type(row))
            obj.is_activated = True
            obj.save()
    return render(request, 'products.html',
                  {'products': items, 'form': form, 'csvform': csvForm})


class ProductUpdateView(BSModalUpdateView):
    model = models.Product
    template_name = 'update_product.html'
    form_class = ItemForm
    success_message = 'Success: Product was Updated.'
    success_url = reverse_lazy('index')


class BannerCreateView(BSModalCreateView):
    template_name = 'create_banner.html'
    form_class = BannerForm()
    success_message = 'Success: Banner was created.'
    success_url = reverse_lazy('index')


def receipt_preview(request):
    if request.user.is_authenticated:
        order = models.Order.objects.get(pk=3)
        return render(request, 'result.html', {'order': order})
    else:
        return redirect('login')
