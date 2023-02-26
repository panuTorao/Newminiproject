from Profile import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    #
    path('categoryList', views.categoryList, name='categoryList'),
    path('categoryNew', views.categoryNew, name='categoryNew'),
    path('<id>/categoryUpdate', views.categoryUpdate, name='categoryUpdate'),
    path('<id>/categoryDelete', views.categoryDelete, name='categoryDelete'),

    path('productList', views.productList, name='productList'),
    # path('<pageNo>/productListPage', views.productListPage, name='productListPage'),
    path('productNew', views.productNew, name='productNew'),
    path('<pid>/productUpdate', views.productUpdate, name='productUpdate'),
    path('<pid>/productDelete', views.productDelete, name='productDelete'),

    path('header', views.header, name='header'),
    path('product', views.product, name='product'),
    path('order', views.order, name='order'),
    path('Profile', views.Profile, name='Profile'),
    # path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('apply', views.apply, name='apply'),
    path('logout', views.logout, name='logout'),
    path('computer', views.computer, name='computer'),
    path('seience', views.seience, name='seience'),
    path('religion', views.religion, name='religion'),
    path('anime', views.anime, name='anime'),
    path('literature', views.literature, name='literature'),
    path('farmer', views.farmer, name='farmer'),
]


