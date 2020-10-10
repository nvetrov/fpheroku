from django.urls import path
from .views import IndexProductListView,  ProductAdd, SearchProductCatalog, UpdateProduct, filter_table

# ViewProductAdd,


# index, Search,  FoundGoodsView
urlpatterns = [
    path('', IndexProductListView.as_view(), name='home'),
    path('<int:pk>/update/', UpdateProduct.as_view(), name='UpdateProduct'),
    path('add/', ProductAdd, name='prod_add'),
    # path('add/', ProductAdd.as_view(), name='prod_add'),
    # path('search/', SearchProductCatalog.as_view(), name='search'),
    path('search/', SearchProductCatalog, name='search'),
    path('<str:sort_table>/', filter_table, name='sort_table'),
]
