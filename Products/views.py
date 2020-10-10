from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# from django.utils import timezone
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, UpdateView
# from django.views.generic.base import View
from Products.models import FoundGoods, Catalog
from .forms import ProductForm, UpdateProductForm
from accounts.models import CustomUser

'''home'''
class IndexProductListView(LoginRequiredMixin, ListView):
    model = FoundGoods
    # вместо атрибута model мы можем указать объект типа QuerySet с заранее заданными фильтрами.
    template_name = 'products/index.html'
    context_object_name = 'products'
    # paginate_by = 100
    ordering = '-create_at'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexProductListView, self).get_context_data(*args, **kwargs)
        # context['shop'] = CustomUser.objects.get(email=self.request.user).shop_num
        # context['user'] = CustomUser.objects.get(email=self.request.user)
        # print(context['ldap'])
        return context

    #

    def get_queryset(self):

        current_user_shop = CustomUser.objects.get(email=self.request.user).shop_num
        return FoundGoods.objects.filter(Q(update_at__isnull=True) & Q(shop_num=current_user_shop))


'''Фильтр НАЙДЕН + ВЫДАН'''
@login_required(login_url='login')
def filter_table(request, sort_table):
    current_user_shop = CustomUser.objects.get(email=request.user).shop_num
    if sort_table == 'find':
        found_products = FoundGoods.objects.filter(
            Q(update_at__isnull=True) & Q(shop_num=current_user_shop))  # Товар найден
    else:
        found_products = FoundGoods.objects.filter(
            Q(update_at__isnull=False) & Q(shop_num=current_user_shop))  # Товар выдан
    context = {'products': found_products}
    return render(request, 'products/filterTab.html', context)


#  Редактивароние товара.
class UpdateProduct(LoginRequiredMixin, UpdateView):
    form_class = UpdateProductForm
    template_name = 'products/foundgoods_update_form.html'
    success_url = '/'

    def get_queryset(self):
        current_user_shop = CustomUser.objects.get(email=self.request.user).shop_num
        return FoundGoods.objects.filter(shop_num=current_user_shop)

    # queryset = FoundGoods.objects.select_related('custom_user').prefetch_related('?')


#


# TODO Поиск по базе
# 2000150655363,15065536,Цилиндр 35X45KNOB TRANSIT 6P никель  4кл
# 2400000538233,82257709,Костюм Вулкан(молескин)112-116/170-176
@login_required(login_url='login/')
def SearchProductCatalog(request):
    data = {}
    if request.is_ajax and request.method == "GET":
        # get the bar_code from the client side.
        q = request.GET.get("bar_code", None).lstrip()
        try:
            catalog = Catalog.objects.filter(Q(ean=q) |
                                             Q(lm=q)).first()
        except Catalog.DoesNotExist:
            # if bar_code not found, then False 404
            return JsonResponse({"success": False}, status=404)
        data = {
            "success": True,
            "catalog": {
                "ean": catalog.ean,
                "lm": catalog.lm,
                "product_name": catalog.product_name,
            },
        }
    return JsonResponse(data, status=200)


# TODO не могу сделать redirect('home') после сохранения из ajax POST
# class ProductAdd(LoginRequiredMixin, View):
#     form_class = ProductForm
#     template_name = "products/add_products.html"
#
#     def get(self, *args, **kwargs):
#         form = self.form_class(self.request.GET, self.request.user)
#         return render(self.request, self.template_name, {"form": form})
#
#     def post(self, *args, **kwargs):
#         if self.request.is_ajax and self.request.method == "POST":
#             form = self.form_class(self.request.POST, self.request.user)
#             if form.is_valid():
#                 instance = form.save()
#                 ser_instance = serializers.serialize('json', [instance, ])
#                 # messages.add_message(self.request, messages.SUCCESS,
#                 #                      'Данные "{}, {} шт." успешно добавлены'.format(
#                 #                          self.cleaned_data["bar_code"],
#                 #                          self.cleaned_data["lm_code"],
#                 #                          self.cleaned_data["caption"],
#                 #                          self.cleaned_data["amount_goods"],
#                 #                          self.cleaned_data["shop_num"], )
#                 #                      )
#                 return JsonResponse({"instance": ser_instance}, status=200)
#             else:
#                 return JsonResponse({"error": form.errors}, status=400)
#
#         return JsonResponse({"error": ""}, status=400)


# TODO переписать под CBV.
@login_required(login_url='login/')
def ProductAdd(request):
    # current_date = timezone.now().date()
    if request.method == 'POST':
        form = ProductForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            # q(form.save())  # Посмотреть что добавляется в форме.
            messages.add_message(request, messages.SUCCESS,
                                 'Данные: "{}, {} {} {}  шт." успешно добавлены'.format(
                                     form.cleaned_data["bar_code"],
                                     form.cleaned_data["lm_code"],
                                     form.cleaned_data["caption"],
                                     form.cleaned_data["amount_goods"],
                                     form.cleaned_data["shop_num"],
                                 )
                                 )

            return redirect('home')
        else:
            #TODO: Ошибка в форме: показать пользователю
            messages.add_message(request, messages.ERROR, form.errors)
    else:
        if request.method == 'GET' and request.is_ajax:
            form = ProductForm(request.GET, request.user)
        # SearchProductCatalog(request)
    # context = {'form': form, 'message': getattr(request, '_messages', [])}
    # context = {'form': form, 'current_date': current_date.strftime('%Y-%m-%d')}
    context = {'form': form}
    return render(request, 'products/add_products.html', context)

# 60076149
# c76WzcMVZk1
# Nikolai.Vetrov@leroymerlin.ru


# 2000150655363,15065536,Цилиндр 35X45KNOB TRANSIT 6P никель  4кл
# 2400000538233,82257709,Костюм Вулкан(молескин)112-116/170-176
# `3276004635358`,14071344,Тюль цветок морекс 300х260 зелен лент
# 4620018799626,82154947,"ЯЩИКИ бордюр настенный 6,5х60 син"
