from django.shortcuts import render,redirect
from django.http import HttpResponse, response
from myapp.models import ProductModel, OrderModel, DetailModel
from smtplib import SMTP
from email.mime.text import MIMEText

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
    elif type == 'empty':
        cartlist=[]
        request.session['cartlist'] = cartlist
        return redirect('/cart/')
    elif type == 'update':
        if request.method == 'POST':
            n =1
            for unit in cartlist:
                unit[2] = request.POST.get('quantity'+str(n), '1')
                unit[3] = str(int(unit[1])*int(unit[2]))
                n = n+1
            request.session['cartlist'] = cartlist
            return redirect('/cart/')
    elif type == 'remove':
        del cartlist[int(id)] #這個id，是cartlist的索引值
        request.session['cartlist'] = cartlist
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

def cartorder(request):
    global cartlist
    global shipping
    localcartlist = cartlist
    localshipping = shipping
    total = 0
    for unit in cartlist:
        total = total + int(unit[3])
    grandtotal = total + localshipping  #總價(加上運費的價格)
    return render(request, 'cartorder.html', locals())

def cartok(request):
    global cartlist
    global shipping
    if request.method =='POST':
        customername = request.POST['customername']
        localcustomername = customername
        customerphone = request.POST['customerphone']
        customeremail = request.POST['customeremail']
        customeraddress = request.POST['customeraddress']
        paytype = request.POST['paytype']
        total = 0
        for unit in cartlist:
            total = total + int(unit[3])
        grandtotal = total + shipping

    #--將訂購人資訊，寫進OrderModel表單------
    productOrder = OrderModel.objects.create(customername = customername, customerphone = customerphone, customeremail = customeremail, customeraddress = customeraddress, paytype = paytype, grandtotal= grandtotal, shipping = shipping, subtotal = total)
    productOrder.save()

    #--將該筆訂單，寫進DetailModel表單----
    #--預判的商品不會只有一筆，用for迴圈，將資料一筆一筆放入資料庫
    dtotal = 0
    for unit in cartlist:
        dtotal = int(unit[1])*int(unit[2])
        unitDetail = DetailModel.objects.create(dorder = productOrder, pname = unit[0], unitprice = int(unit[1]), quantity = int(unit[2]), dtotal = dtotal)
        unitDetail.save()
    
    #----在這裡清空購物車
    cartlist = []

    #----郵件寄送------
    mailfrom = 'Your Gmail Account'
    mailpw = 'Your App Password'
    mailto = customeremail
    mailsubject = '木葉商城-訂單通知'
    mailcontent = customername+'忍者，您的忍具已訂購成功！ 我們會盡速且祕密的把忍具送至您指定的地點。請在指定地點四周佈好木葉情報警戒結界，以確保您忍具的安全，感謝您的支持。'
    send_message(mailfrom, mailpw, mailto, mailsubject, mailcontent)
    return render(request, 'cartok.html', locals())

def send_message(mailfrom, mailpw, mailto, mailsubject, mailcontent):
    strSmtp = 'smtp.gmail.com:587'
    strAccount = mailfrom
    strPassword = mailpw
    msg = MIMEText(mailcontent)
    msg['Subject'] = mailsubject
    mailto1 = mailto
    server = SMTP(strSmtp)
    server.ehlo() #跟主機溝通
    server.starttls() #TTLS安全認證
    server.login(strAccount, strPassword)
    server.sendmail(strAccount,mailto1, msg.as_string())
