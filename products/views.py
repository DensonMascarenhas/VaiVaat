from django.shortcuts import render
import http
import sqlite3

from django.shortcuts import render,redirect
from django.http import HttpResponse

import products.views
from .models import product


def index(request):
    items=product.objects.all()
    return render(request, 'index.html')


def talk(request):
    if request.method=="POST":
        from datetime import date
        import googletrans
        import speech_recognition as sr
        import gtts
        import pyttsx3
        # import pyodbc
        import datetime
        import htmls


        recognizer = sr.Recognizer()
        listener = sr.Recognizer()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        total_amount = 0
        counter = 0
        id = 0
        price = 0
        stock = 0
        gstp=0
        total_amount = 0
        total_qty = 0
        discount=0.0
        now = datetime.datetime.now()
        t_qty = 0;
        t_price=0.
        iname=[]
        iqty=[]
        iprice=[]
        idis=[]
        iperamt=[]
        gst=[]
        grand=0


        try:
            conn=sqlite3.connect('db.sqlite3')
            curs=conn.cursor()
        except:
            print("not coonect")
        datie = str(datetime.datetime.now().day)
        engine.runAndWait()
        while (True):
            with sr.Microphone() as source:
                recognizer.pause_threshold = 0.5
                pyttsx3.speak("tell item name...")
                print("Listening...")
                voice = recognizer.listen(source, phrase_time_limit=5)
                text = recognizer.recognize_google(voice)
                text = text.lower()
                print(text)
                if "finish" in text:
                    pyttsx3.speak("Total amount is to pay is {}....Thank you for shopping with us...".format(total_amount))
                    if total_amount > 0 and total_qty > 0:

                        grand=total_amount

                        print("Uploaded Successfully")
                        curs.close()
                        print("Executes")
                    else:
                        return 0
                    conn = sqlite3.connect('db.sqlite3')
                    cur = conn.cursor()
                    cur.execute("select name,info from products_shop_name")
                    r = cur.fetchall()
                    return render(request, 'bill.html',{'bill':zip(iname,iqty,iprice,gst,idis,iperamt),'amt':total_amount,'grand':grand,"r":r})
                else:

                    cur=conn.cursor()
                    cur.execute(" SELECT * FROM products_product")
                    rows=cur.fetchall()
                    for row in rows:
                        if row[1] == text:
                            counter = 1
                            id = row[0]
                            price = row[2]
                            stock = row[3]
                            discount=row[4]
                            gstp=row[5]

                    if (counter == 1):
                        pyttsx3.speak("Specified item is found in your inventory")


                        while (True):
                            try:

                                with sr.Microphone() as src:
                                    pyttsx3.speak("Specify the quantity...")
                                    print("Listening...")
                                    listener.pause_threshold = 0.5
                                    qty_voice = recognizer.listen(src, phrase_time_limit=5)
                                    qty_text = recognizer.recognize_google(qty_voice)
                                    # print(qty_text)
                                    pyttsx3.speak("Specified quantity is...")
                                    pyttsx3.speak(qty_text)
                                    qty_text = float(qty_text)
                                    if (qty_text < stock):
                                        total_qty += qty_text
                                        if discount == 1.0:
                                            discount = 0.0
                                        temp = (qty_text * price) - (qty_text * price * discount) + (qty_text * price * gstp)
                                        total_amount = total_amount + temp
                                        stock = stock - qty_text
                                        if stock<10.0:
                                            pyttsx3.speak("Item {} is running out of stock.".format(iname))

                                        iqty.append(qty_text)
                                        iprice.append(price)
                                        gst.append(gstp)
                                        iperamt.append(temp)
                                        iname.append(text)
                                        if discount==1.0:
                                            idis.append("No")
                                        else:
                                            idis.append(discount)
                                        query = ''' insert into products_entry(qty,price,datie,name)values(?,?,?,?) '''
                                        curs.execute(query, (qty_text, temp, datetime.datetime.today().date(),text))
                                        conn.commit()

                                        cur.execute('''update products_product set stock={} WHERE id={}'''.format(stock, id))
                                        conn.commit()

                                        counter = 0
                                        id = 0
                                        stock = 0
                                        price = 0
                                        gstp=0
                                        discount=0
                                    else:
                                        pyttsx3.speak("Not enough stock to sell this item.")

                                break
                            except:
                                pyttsx3.speak("Could not get you sir. Please pronounce the digit properly...")

                    else:
                        pyttsx3.speak("Item is Not present in your inventory")





def news(request):
    return render(request, 'bill.html')


def less(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT * FROM products_product where stock<10")
    rows = cur.fetchall()
    return render(request,"less_stock.html",{"row":rows})


def sales(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT name,qty,price,datie FROM products_entry")
    rows = cur.fetchall()
    return render(request, "sales.html", {"row": rows})


def find_sale(request):
    import datetime
    emp1 = []
    emp2 = []
    emp3 = []
    emp4 = []
    qtysum=0
    sum=0

    frm=request.POST["from"]
    to=request.POST["to"]
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT name,qty,price,datie FROM products_entry")
    rows = cur.fetchall()
    for r in rows:
        if datetime.datetime.fromisoformat(r[3])>=datetime.datetime.fromisoformat(frm) and datetime.datetime.fromisoformat(r[3])<=datetime.datetime.fromisoformat(to):
            emp1.append(r[0])
            emp2.append(r[1])
            emp3.append(r[2])
            emp4.append(r[3])
            qtysum+=r[1]
            sum+=r[2]


    return render(request, "sales.html", {"row": zip(emp1,emp2,emp3,emp4),"qtysum":qtysum,"sum":sum})




def daily(request):
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    dates=str(datetime.datetime.today().date())
    cur.execute("select id,qty,price,datie,name from products_entry")
    rows=cur.fetchall()
    emp1=[]
    emp2 = []
    emp3 = []
    emp4 = []
    emp5 = []
    emp6=0.0
    for row in rows:
        if row[3]==dates:
            emp1.append(row[0])
            emp2.append(row[1])
            emp3.append(row[2])
            emp4.append(row[3])
            emp5.append(row[4])
            emp6+=row[2]
    return render(request, "daily.html", {"row":zip(emp1,emp2,emp3,emp4,emp5),"r":emp6})

def add_stock(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT id,name,stock FROM products_product where stock<10")
    rows = cur.fetchall()
    return render(request, "add_stock.html", {"row":rows})


def report(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT id,name,stock FROM products_product")
    rows = cur.fetchall()
    return render(request, "report.html", {"row": rows})


def show_rep(request):
    import datetime
    pricepur=0
    qtypur=0
    pricesold=0
    qtysold=0
    pr=0
    if request.method == "POST":
        d=datetime.datetime.today().date()-datetime.timedelta(days=30)
        item=request.POST["dslist"]
        frm=request.POST["from"]
        to=request.POST["to"]
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("SELECT item_id,item_name,qty,datie,price,supplier,purchase_price FROM products_stock_purchase")
        r = cur.fetchall()
        k=0
        cur.execute( "SELECT qty,name,price,datie FROM products_entry")
        s=cur.fetchall()
        cur.execute(" SELECT * FROM products_product")
        rows = cur.fetchall()
        for rd in r:
            if rd[1]==item:

                if datetime.datetime.fromisoformat(rd[3])>=datetime.datetime.fromisoformat(frm) and datetime.datetime.fromisoformat(rd[3])<=datetime.datetime.fromisoformat(to):
                    pricepur=int(rd[6])
                    qtypur+=int(rd[2])
                    k=rd[6]


        for sd in s:
            if sd[1]==item:

                if datetime.datetime.fromisoformat(rd[3])>=datetime.datetime.fromisoformat(frm) and datetime.datetime.fromisoformat(rd[3])<=datetime.datetime.fromisoformat(to) :
                    pricesold+=int(sd[2])
                    qtysold+=int(sd[0])
        for f in rows:
            if f[1]==item:
                pr = f[2]

        temp=qtysold*k
        result=""
        if (pricesold-temp)<0:
            result="Loss"
        elif (pricesold-temp)==0 :
            result="Nutral"
        else:
            result="Gain"

        return render(request, 'gen.html', {"a":item, "b":pricepur, "c":qtypur, "d":pricesold, "e":qtysold, "f":temp,"g":pricesold-temp,"h":result,"i":pr})


def purchase_bill(request):
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        frm = request.POST["from"]
        to = request.POST["to"]
        cur.execute(" SELECT item_id,item_name,qty,datie,price,supplier FROM products_stock_purchase")
        rows = cur.fetchall()
        a=[]
        b=[]
        c=[]
        d=[]
        e=[]
        f=[]
        total=0
        for r in rows:
            if datetime.datetime.fromisoformat(r[3]) >= datetime.datetime.fromisoformat(frm) and datetime.datetime.fromisoformat(r[3]) <= datetime.datetime.fromisoformat(to):
                a.append(r[0])
                b.append(r[1])
                c.append(r[2])
                d.append(r[3])
                e.append(r[4])
                f.append(r[5])
                total=total+float(r[4])
        return render(request, "purchase_bill.html", {"row":zip(a,b,c,d,e,f),"total":total})



    else:
        cur.execute(" SELECT item_id,item_name,qty,datie,price,supplier FROM products_stock_purchase")
        rows = cur.fetchall()
        return render(request, "purchase_bill.html", {"row": rows,"total":"Yet to Find"})


def credit(request):
    import pyttsx3
    import datetime
    counter=0
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['number']
        total=request.POST['total']
        paying=request.POST['paying']
        balance=request.POST['pending']
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        query="insert into products_credit(name,phone,bill_amount,paid_amount,pending_amount,datie) values(?,?,?,?,?,?)"
        cur.execute(query,(name,phone,total,paying,balance, datetime.datetime.today().date()))
        conn.commit()
        pyttsx3.speak("Information stored successfully in our side.")
        from .models import product
        rows = product.objects.all()
        return render(request, "main.html", {'name': rows})



def pay_credit(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method=="POST":
        phone=request.POST["dslist"]
        cur.execute("select * from products_credit where phone={}".format(phone))
        rs = cur.fetchall()
        cur.execute("select distinct(phone),name from products_credit")
        r = cur.fetchall()
        total=0
        for k in rs:
            if k[2]==phone:
                total+=float(k[5])
        cur.execute("select phone,already_amount from products_paytm")
        rpm = cur.fetchall()
        fs=0
        for m in rpm:
            if m[0]==phone:
                fs+=float(m[1])

        yet=total-fs
        return render(request, "credit.html", {"rs": rs, "r": r,"ph":phone,"tot":total,"all":fs,"yet":yet})

    else:

        cur.execute("select distinct(phone),name from products_credit")
        r=cur.fetchall()
        return render(request,"credit.html",{"r":r})


def view_credit(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method=="POST":
        name=request.POST["dslist"]
        cur.execute("select * from products_admin_credit ")
        rs = cur.fetchall()
        total=0
        a=[]
        b=[]
        c=[]
        d=[]
        e=[]
        f=[]
        for r in rs:
            if r[1]==name:
                total+=float(r[4])
                a.append(r[0])
                b.append(r[1])
                c.append(r[2])
                d.append(r[3])
                e.append(r[4])
                f.append(r[5])
        cur.execute("select distinct(supplier),balance from products_admin_credit")
        r = cur.fetchall()
        cur.execute("select supplier,already_amount from products_paytm2")
        rpm = cur.fetchall()

        fs=0
        for m in rpm:
            if m[0]==name:
                fs+=float(m[1])
        yet=total-fs
        return render(request, "view-credit.html", {"rs": zip(a,b,c,d,e,f),"r":r,"name":name,"tot":total,"all":fs,"yet":yet})
    else:
        a=[]
        cur.execute("select distinct(supplier),balance from products_admin_credit")
        r = cur.fetchall()
        try:
            for k in r:
                if k not in a:
                    a.append(k)
            return render(request, "view-credit.html", {"r": a})
        except:
            cur.execute("No credit List found.")
            from .models import product
            rows = product.objects.all()
            return render(request, "main.html", {'name': rows})



def paytm(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        num=request.POST["num"]
        total=request.POST["total"]
        already=request.POST["already_paid"]
        paying=request.POST["paying"]
        balance=request.POST["balance"]
        res=float(already)+float(paying)
        cur.execute("select phone,already_amount from products_paytm")
        rpm = cur.fetchall()
        counter=0
        if float(balance)==0.0:
            cur.execute("delete from products_credit where phone={}".format(num))
            conn.commit()
            cur.execute("delete from products_paytm where phone={}".format(num))
            conn.commit()
        else:

            for r in rpm:
                if r[0]==num:
                    counter=1
            if counter==1:
                cur.execute("update products_paytm set already_amount={},datie={},balance={} where phone={}".format(res,datetime.datetime.today().date(),balance,num))
                conn.commit()
            else:
                query="insert into products_paytm(phone,bill_amount,already_amount,balance,datie)values(?,?,?,?,?)"
                cur.execute(query,(num,total,paying,balance,datetime.datetime.today().date()))
                conn.commit()
        pyttsx3.speak("Updated Successfully.")

        cur.execute("select distinct(phone),name from products_credit")
        r = cur.fetchall()
        return render(request, "credit.html", {"r": r})






def stop(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        pyttsx3.speak("Thank you.")
        from .models import product
        rows = product.objects.all()
        return render(request, "main.html", {'name': rows})



def paytm2(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    id1 = 0
    id2 = 0
    if request.method == "POST":
        name = request.POST["name"]
        total = request.POST["total"]
        already = request.POST["already_paid"]
        paying = request.POST["paying"]
        balance = request.POST["balance"]
        res = float(already) + float(paying)
        cur.execute("select * from products_paytm2")
        rpm = cur.fetchall()
        cur.execute("select * from products_admin_credit")
        rpm2 = cur.fetchall()
        counter=0

        for r in rpm:
            if r[1]==name:
                id1=r[0]
                if float(balance) == 0.0:
                    cur.execute("delete from products_paytm2 where id={}".format(id1))
                    conn.commit()

        for k in rpm2:
            if k[1]==name:
                id2=k[0]
                if float(balance) == 0.0:
                    cur.execute("delete from products_admin_credit where id={}".format(id2))
                    conn.commit()


        for r in rpm:
            if r[1]==name:
                counter=1
        if counter == 1:
            cur.execute("update products_paytm2 set already_amount={},datie={},balance={} where id={}".format(res,
                                                                                                                datetime.datetime.today().date(),
                                                                                                                balance,
                                                                                                                id1))
            conn.commit()
        else:
            query = "insert into products_paytm2(supplier,bill_amount,already_amount,balance,datie)values(?,?,?,?,?)"
            cur.execute(query, (name, total, paying, balance, datetime.datetime.today().date()))
            conn.commit()

        pyttsx3.speak("Updated Successfully.")
        a = []
        cur.execute("select distinct(supplier),balance from products_admin_credit")
        r = cur.fetchall()
        return render(request, "view-credit.html", {"r": r})


def end(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        pyttsx3.speak("Transaction Succesful")
        cur.execute("select distinct(supplier),balance from products_admin_credit")
        r = cur.fetchall()
        return render(request, "view-credit.html", {"r": r})


def setting(request):
    import pyttsx3
    import datetime
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == "POST":
        name = request.POST["name"]
        info = request.POST["info"]
        cur.execute("delete from products_shop_name")
        conn.commit()
        query="insert into products_shop_name(name,info) values(?,?)"
        cur.execute(query,(name,info))
        conn.commit()
        pyttsx3.speak("Updated Successfully")
        from .models import product
        rows = product.objects.all()
        return render(request, "main.html", {'name': rows})
    else:
        cur.execute("select name,info from products_shop_name")
        r = cur.fetchall()
        return render(request, "setting.html", {"r": r})



def add_db(request):
    import pyttsx3
    import datetime
    if request.method == "POST":
        k=request.POST['dslist']
        l=request.POST['qty']
        s=request.POST['supp']
        pur=request.POST["pur"]
        sell=request.POST["sell"]
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(" SELECT id,name,stock,price,purchase_price FROM products_product where stock<10")
    rows = cur.fetchall()
    for row in rows:
        if row[1]==k:
            id=row[0]
            stock=row[2]
            temp=int(stock)+int(l)

            j=int(row[3])
            e=int(row[4])
            if len(pur)!=0:
                e=int(pur)
            if len(sell)!=0:
                j=int(sell)
            p = int(e) * int(l);
            cur.execute('''update products_product set stock={},price={},purchase_price={} WHERE id={}'''.format(temp, j, e, id))
            conn.commit()
            pyttsx3.speak("Item Added to Stock")
            query = ''' insert into products_stock_purchase(item_id,item_name,qty,datie,price,supplier,purchase_price)values(?,?,?,?,?,?,?) '''
            cur.execute(query, (id,k,l, datetime.datetime.today().date(),p,s,e))
            conn.commit()
            return render(request, "admin_credit.html", {"a":k,"b":l,"c":p,"d":s,"e":e})



def admin_credit(request):
    import datetime
    import pyttsx3
    if request.method == "POST":
        name=request.POST['name']
        total=request.POST['total']
        paid=request.POST['paying']
        balance=request.POST['balance']
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        name=str(name).lower()
        query="insert into products_admin_credit(supplier,total,paid,balance,datie) values(?,?,?,?,?)"
        cur.execute(query,(name,total,paid,balance,datetime.datetime.today().date()))
        conn.commit()
        pyttsx3.speak("Operation saves Successfully.")
        cur.execute(" SELECT id,name,stock FROM products_product where stock<10")
        rows = cur.fetchall()
        return render(request, "add_stock.html", {"row": rows})







def main(request):
    from .models import product
    rows=product.objects.all()
    return render(request,"main.html",{'name':rows})

a=[]
b=[]



def sub(request):
    import datetime
    import pyttsx3
    if request.method == "POST":
        k=request.POST['dslist']
        l=request.POST['qty']

        if l=="404":
            if len(a)==0:
                pyttsx3.speak("Please purchase atleast one item.")

            else:
                taken=passing()
                iname=list(taken["name"])
                iqty=list(taken["iqty"])
                iprice=list(taken["iprice"])
                iperamt=list(taken["iperamt"])
                total_amount=taken["amt"]
                grands=taken["grand"]
                gst=taken["gst"]
                discount=taken["discount"]
                if len(iname)!=0:
                    conn = sqlite3.connect('db.sqlite3')
                    cur = conn.cursor()
                    cur.execute("select name,info from products_shop_name")
                    r = cur.fetchall()
                    return render(request,"bill.html",{"bill":zip(iname,iqty,iprice,gst,discount,iperamt),'amt':total_amount,'grand':grands,"r":r})
                else:
                    from .models import product
                    rows = product.objects.all()
                    return render(request, "main.html", {'name': rows})

            # return render(request,"bill.html",taken)

        else:
            a.append(k)
            b.append(float(l))

    from .models import product
    rows = product.objects.all()
    return render(request, "main.html", {'name': rows})

def passing():
    import pyttsx3
    import datetime
    iname = []
    iqty = []
    iprice = []
    idis = []
    iperamt = []
    total_amount=0
    total_qty = 0
    gstp=0
    discount=0
    gst=[]

    conn = sqlite3.connect('db.sqlite3')

    cur = conn.cursor()
    cur.execute(" SELECT * FROM products_product")
    rows = cur.fetchall()

    for i in range(0,len(a)):
        for row in rows:
            if row[1]==a[i]:
                id = row[0]
                price = row[2]
                stock = row[3]
                qty_text = b[i]
                discount = row[4]
                gstp = row[5]

                if (b[i] < stock):
                    total_qty += qty_text
                    if discount==1.0:
                        discount=0.0
                    temp=(qty_text*price)-(qty_text*price*discount)+(qty_text*price*gstp)
                    total_amount = total_amount + temp
                    stocks = stock - qty_text
                    print(stocks)
                    if(stocks<10.0):
                        pyttsx3.speak("Item {} is running out of stock.".format(a[i]))

                    iqty.append(qty_text)
                    iprice.append(price)
                    iperamt.append(temp)
                    iname.append(a[i])
                    gst.append(gstp*100)
                    query = ''' insert into products_entry(qty,price,datie,name)values(?,?,?,?) '''
                    cur.execute(query, (qty_text,temp, datetime.datetime.today().date(),a[i]))
                    conn.commit()
                    if discount == 1.0:
                        idis.append("No")
                    else:
                        idis.append(discount*100)

                    cur.execute('''update products_product set stock={} WHERE id={}'''.format(stocks, id))
                    conn.commit()
                else:
                    pyttsx3.speak("No Sufficient Quantity is available for {}. So Skipping ".format(a[i]))


    pyttsx3.speak("Total amount is to pay is {}....Thank you for shopping with us...".format(total_amount))
    grands=0
    if total_amount > 0 and total_qty>0:

        grands = total_amount
        cur.close()

        products.views.a=[]
        products.views.b=[]
    return ({"name":iname,"iqty":iqty,"iprice":iprice,"iperamt":iperamt,'amt':total_amount,'grand':grands,'gst':gst,'discount':idis})
