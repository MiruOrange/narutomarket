from django.shortcuts import render,redirect
from django.http import HttpResponse, response
from myapp.models import ProductModel

# Create your views here.
cartlist = []
shipping = 100

def index(request):
    products = ProductModel.objects.all()
    productlist = []
    for i in range(1, 9):
        product = ProductModel.objects.get(id = i)
        productlist.append(product)
    return render(request, 'index.html', locals())

def detail(request, id=None):
    product = ProductModel.objects.get(id = id)
    return render(request, 'detail.html', locals())

def addtocart(request, type=None, id=None):
    global cartlist
    #add update empty remove
    if type=='add':
        product = ProductModel.objects.get(id = id)
        #購物車裡，有沒有已經存在的商品？
        #如果有，就更新session裡面的商品數量、金額
        #如果沒有，就把商品，放到session裡
        #True False
        noCartSession = True
        for unit in cartlist:
            if product.pname == unit[0]:
                unit[2] = str(int(unit[2])+1)
                unit[3] = str(int(unit[3])+product.pprice*1)
                noCartSession = False
        if noCartSession:
            templist = []
            #(pname, pprice, 1, 1*pprice)
            templist.append(product.pname)
            templist.append(str(product.pprice))
            templist.append(str(1))
            templist.append(str(product.pprice*1))
            #全域變數
            cartlist.append(templist)
        request.session['cartlist'] =cartlist
        print(request.session['cartlist'])
        return redirect('/cart/')

def cart(request):
    global cartlist
    global shipping         #運費
    localcartlist = cartlist        #購物車的session
    total = 0                       #小計的金額
    localshipping = shipping        #運費
    
    for unit in cartlist:
        total = total + int(unit[3])
    grandtotal = total + localshipping  #總價(加上運費的價格)
    return render(request, 'cart.html', locals())
