from django.shortcuts import render

# Create your views here.
import datetime

from django.forms import modelformset_factory
from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from Profile.forms import *
import datetime, os
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')

@login_required(login_url='userAuthen')
def categoryList(request):
    # if not chkPermission(request):
    #     return redirect('home')
    categories = Categories.objects.all().order_by('id')
    context = {'categories':categories}
    return render(request, 'categoryList.html', context)

@login_required(login_url='userAuthen')
def categoryNew(request):
    # if not chkPermission(request):
    #     return redirect('home')
    if request.method == 'POST':
        form = CategoiesForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form': form}
            return render(request, 'categoryNew.html', context)
    else:
        form = CategoiesForm()
        context = {'form': form}
        return render(request, 'categoryNew.html', context)

@login_required(login_url='userAuthen')
def categoryUpdate(request, id):
    # if not chkPermission(request):
    #     return redirect('home')
    category = get_object_or_404(Categories, id=id)
    form = CategoiesForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('categoryList')
        else:
            context = {'form':form}
            return render(request, 'categoryUpdate.html')
    else:
        context = {'form':form}
        return render(request, 'categoryUpdate.html', context)

@login_required(login_url='userAuthen')
def categoryDelete(request, id):
    # if not chkPermission(request):
    #     return redirect('home')
    category = get_object_or_404(Categories, id=id)
    form = CategoiesForm(data=request.POST or None, instance=category)
    if request.method == 'POST':
        category.delete()
        return redirect('categoryList')
    else:
        form.deleteForm()
        context = {'form':form, 'category':category}
        return render(request, 'categoryDelete.html', context)

# @login_required(login_url='userAuthen')
def productList(request):
    # if not chkPermission(request):
    #     return redirect('home')
    products = Products.objects.all().order_by('pid')
    context = {'products':products}
    return render(request, 'productList.html', context)

def productNew(request):
    # if not chkPermission(request):
    #     return redirect('home')
    if request.method == 'POST':
        form = ProductsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            pid = newForm.pid
            # filename = newForm.picture.name
            filepath = newForm.picture.name
            # point = filename.rfind('.')
            # ext = filename[point:]
            point = filepath.rfind('.')
            ext = filepath[point:]
            filenames = filepath.split('/')
            filename = filenames[len(filenames)-1]
            newfilename = pid + ext
            newForm.save() # product_tmp/xxx.xxx
            product = get_object_or_404(Products, pid=pid)
            product.picture.name = '/products/'+newfilename # pxxx.xxx
            product.save()
            #
            #             # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
            #             # if os.path.exists('static/products/' + newfilename):
            #             #     os.remove('static/products/' + newfilename)  # file exits, delete it
            #             # os.rename('products_tmp/'+filename, 'static/products/' + newfilename)
            if os.path.exists('static/products/' + newfilename):
                os.remove('static/products/' + newfilename)  # file exits, delete it
            os.rename('static/products/'+filename, 'static/products/' + newfilename)
        else:
            product = get_object_or_404(Products, pid=request.POST['pid'])
            if product:
                messages.add_message(request, messages.WARNING, "รหัสสินค้าซ้ำกับที่มีอยู่แล้วในระบบ")
                context = {'form': form}
                return render(request, 'productNew.html', context)
        return redirect('productList')
    else:
        form = ProductsForm()
        context = {'form':form }
        return render(request, 'productNew.html', context)
#
def productUpdate(request, pid):
    # if not chkPermission(request):
    #     return redirect('home')
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name  # รูปสินค้าเดิม
    # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
    if request.method == 'POST':
        form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        if form.is_valid():
            newForm = form.save(commit=False)
            pid = newForm.pid
            print(newForm.picture.name)
            if newForm.picture.name != picture: #  หากเลือกรูปสินค้าใหม่
                newForm.save()
                filepath = newForm.picture.name
                point = filepath.rfind('.')
                ext = filepath[point:]
                filenames = filepath.split('/')
                filename = filenames[len(filenames) - 1]
                newfilename = pid + ext
                # filename = newForm.picture.name
                # point = filename.rfind('.')
                # ext = filename[point:]
                newfilename =  pid + ext
                product = get_object_or_404(Products, pid=pid)
                product.picture.name = '/products/' +newfilename
                product.save()
                # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
                if os.path.exists('static/products/' + newfilename): # file exits, delete it
                    os.remove('static/products/' +newfilename)
                os.rename('static/products/'+ filename, 'static/products/' +newfilename)
            else:
                newForm.save()
        return redirect('productList')
    else:
        # form = ProductsForm(request.POST or None, instance=product, files=request.FILES)
        form = ProductsForm(instance=product)
        form.updateForm()
        context = {'form': form}
        return render(request, 'productUpdate.html', context)

def productDelete(request, pid):
    # if not chkPermission(request):
    #     return redirect('home')
    product = get_object_or_404(Products, pid=pid)
    picture = product.picture.name  # รูปสินค้าเดิม
    if request.method == 'POST':
        product.delete()
        # บนเซิร์ฟเวอร์ต้องเป็น djangShopping/static/products/'
        # ใน table db เก็บ /products/xxx.xx
        if os.path.exists('static'+picture):  # file exits, delete it
            os.remove('static'+picture)
        return redirect('productList')
    else:
        form = ProductsForm(instance=product)
        form.deleteForm()
        context = {'form': form, 'product':product}
        return render(request, 'productDelete.html', context)

def header(request):
    return render(request, 'header.html')

def product(request):
    return render(request, 'product.html')

def login(request):
    return render(request, 'login.html')

def apply(request):
    return render(request, 'apply.html')

def logout(request):
    return render(request, 'logout.html')

def computer(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'computer.html', context)

def seience(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'seience.html', context)

def religion(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'religion.html', context)

def anime(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'anime.html', context)

def literature(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'literature.html', context)

def farmer(request):
    ProductList = Products.objects.all()
    context = {'ProductList': ProductList}
    return render(request, 'farmer.html', context)


def order(request):
    return render(request, 'order.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if confirmpassword == password:
            user = User.objects.create_user(username,email,password)
            user.save()
            return redirect('login')
        else:
            return render(request,'apply.html')
    else:
        return render(request, 'apply.html')

# def login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username,password=password)
#         if user is not None
#             login(request,user)













