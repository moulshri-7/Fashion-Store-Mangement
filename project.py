import mysql.connector
import datetime
mydb=mysql.connector.connect(host="localhost",\
                                             user="root",\
                                             passwd="Moulshri.7",\
                                             database="project")

mycursor=mydb.cursor()

def AddProduct():
    L=[]
    stk=[]
    pid=input("Enter the Product ID : ")
    L.append(pid)
    IName=input("Enter the Product Name : ")
    L.append(IName)
    brand=input("Enter the Product's Brand Name : ")
    L.append(brand)
    fr=input("Enter Men/Women/Kids : ")
    L.append(fr)
    sn=input("Enter the season Winter/Summer : ")
    L.append(sn)
    rate=int(input("Enter the Rates for Product : "))
    L.append(rate)
    product=(L)
    sql="Insert into product(product_id,PName,brand,Product_for,Season,rate) values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,product)
    mydb.commit()
    stk.append(pid)
    stk.append(0)
    stk.append("No")
    st=(stk)
    sql="insert into stock(item_id, Instock, status) values(%s,%s,%s)"
    mycursor.execute(sql,st)
    mydb.commit()
    print()
    print("One Product inserted ")
    
def EditProduct():
    pid=input("Enter product ID to be edited : ")
    sql="select * from product where product_id=%s"
    ed=(pid,)
    mycursor.execute(sql,ed)
    res=mycursor.fetchall()
    for x in res:
        print(x)
        print()
    print("product_id , PName , brand , Product_for , season , rate")
    print()
    fld=input("From the above options enter the field which you want to edit : ")

    val=input("Enter the value you want to set : ")
    sql="Update product set " + fld +"='" + val + "' where product_id='" + pid + "'"
    mycursor.execute(sql)
    print()
    print("Editing Done!! ")
    print()
    print("After correction the record is : ")
    sql="select * from product where product_id=%s"
    ed=(pid,)
    mycursor.execute(sql,ed)
    res=mycursor.fetchall()
    for x in res:
        print(x)
    mydb.commit()
    
def DelProduct():
    pid=input("Enter the Product id to be deleted : ")
    sql="delete from sales where item_id=%s"
    id=(pid,)
    mycursor.execute(sql,id)
    mydb.commit()
    sql="delete from purchase where item_id=%s"
    mycursor.execute(sql,id)
    mydb.commit()
    sql="delete from stock where item_id=%s"
    mycursor.execute(sql,id)
    mydb.commit()
    sql="delete from product where product_id=%s"
    mycursor.execute(sql,id)
    mydb.commit()
    print("One Item Deleted")

def ViewProduct():
    print("Display Menu: Select the category to display the data")
    print("1. All Details")
    print("2. Product Name")
    print("3. Product Brand")
    print("4. Product For")
    print("5. Product Season")
    print("6. Product ID")
    ctr=0
    print()
    ch=int(input("Enter your choice to display : "))
    print()

    if ch==1:
        sql="select * from product"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        for ctr in res:
            print(ctr)
        ctr=1

    elif ch==2:
        var='PName'
        val=input("Enter the name of Product : ")

    elif ch==3:
        var='brand'
        val=input("Enter the name of Brand : ")

    elif ch==4:
        var='Product_for'
        val=input("Enter Men/Women/Kids : ")

    elif ch==5:
        var='season'
        val=input("Enter the Season Summer/Winter : ")

    elif ch==6:
        var='product_id'
        val=input("Enter the Product_id : ")
    print("The required records are : ")
    print()

    if ctr==0:
        sql="select * from product where " + var + " = %s"
        sq=sql
        tp=(val,)
        mycursor.execute(sq,tp)
        res=mycursor.fetchall()
        for ctr in res:
            print(ctr)
    
def PurchaseProduct():
    mn=""
    dy=""
    now=datetime.datetime.now()
    purchaseID="P"+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+ str(now.minute)+str(now.second)
    L=[]
    Lst=[]
    L.append(purchaseID)
    itemId=input("Enter Product ID : ")
    L.append(itemId)
    itemNo =int(input("Enter the quantity : "))
    L.append(itemNo)
    sql="select rate from product where product_id=%s"
    pid=(itemId,)
    mycursor.execute(sql,pid)
    res=mycursor.fetchone()

    for x in res:
        print("Rate is : ", x)
    amount=x*itemNo
    print("Total amount is :", amount)
    L.append(amount)
    mnth=now.month

    if mnth<=9:
        mn="0"+str(mnth)

    else:
        mn=str(mnth)
    day=now.day

    if day<=9:
        dy="0"+str(day)

    else:
        dy=str(day)
        
    dt=str(now.year)+"-"+mn+"-"+dy
    L.append(dt)
    tp=tuple(L)
    sql="insert into purchase(purchase_id,item_id, no_of_items,amount, Purchase_date)values(%s,%s,%s,%s,%s)"
    mycursor.execute(sql,tp)
    mydb.commit()
    sql="SELECT EXISTS(Select * from stock where item_id=%s)"
    mycursor.execute(sql,pid)
    res=mycursor.fetchall()
    
    if (res[0][0]==0):
        instock = itemNo
        if instock > 0:
            status = "Available"
        else:
            status = "Unavailable"
        Lst.append(itemId)
        Lst.append(instock)
        Lst.append(status)
        tp=(Lst)
        sql="insert into stock(item_id, Instock, status)values(%s,%s,%s)"
        mycursor.execute(sql,tp)
        mydb.commit()
            
    elif (res[0][0]==1):
        sql="Select Instock from stock where item_id=%s"
        mycursor.execute(sql,pid)
        result=mycursor.fetchall()
        for i in result:
            instock=int(i[0]+itemNo)
            if instock>0:
                status="Available"
            else:
                status="Unavailable"
        Lst.append(instock)
        Lst.append(status)
        Lst.append(itemId)
        tp=(Lst)
        sql="update stock set Instock=%s,status=%s where item_id=%s"
        mycursor.execute(sql,tp)
        mydb.commit()
        
        print()
        print("1 Item purchased and saved in Database")

def ViewPurchase():
    item=input("Enter Product Id : ")
    sql="select product.product_id,product.PName,product.brand,\
purchase.no_of_items, purchase.purchase_date, \
purchase.amount from product INNER JOIN purchase ON product .product_id=purchase.item_id and product.product_id=%s"
    itm=(item,)

    mycursor.execute(sql,itm)
    res=mycursor.fetchall()
    print()
    print("Following are the details of the purchase made :")
    print()
    for x in res:
        print(x)

def ViewStock():
    item=input("Enter Product Id : ")
    sql="select product.product_id,product.PName,stock.Instock,\
stock.status from stock, product where \
product.product_id=stock.item_id and product.product_id=%s"
    itm=(item,)
    mycursor.execute(sql,itm)
    res=mycursor.fetchall()
    print()
    for x in res:
        print(x)
        
def SaleProduct():
    now=datetime.datetime.now()
    saleID="S"+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute) +str(now.second)
    L=[]
    L.append(saleID)
    itemId=input("Enter Product ID : ")
    L.append(itemId)
    itemNo=int(input("Enter the number of Items : "))
    L.append(itemNo)
    sql="select rate from product where product_id=%s"
    pid=(itemId,)
    mycursor.execute(sql,pid)
    res=mycursor.fetchall()
    for x in res:
        print("The rate of item is :",x[0])
    print("Total amount is : ", x[0]*itemNo)
    tot=x[0]*itemNo
    dis=int(input("Enter the discount % : "))
    saleRate=tot-(tot*dis/100)
    print("Payable amount after discount is : ", saleRate)
    L.append(saleRate)
    amount=itemNo*x[0]
    L.append(amount)
    mnth=now.month

    if mnth<=9:
        mn="0"+str(mnth)
    else:
        mn=str(mnth)
    day=now.day
    if day<=9:
        dy="0"+str(day)
    else:
        dy=str(day)

    dt=str(now.year)+"-"+mn+"-"+dy
    L.append(dt)
    tp=(L)
    sql="insert into sales (sale_id, item_id,no_of_items_sold,\
sale_rate,amount,date_of_sale) values(%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,tp)
    mydb.commit()
    sql="Select Instock from stock where item_id=%s"
    mycursor.execute(sql,pid)
    res=mycursor.fetchall()

    for x in res:
        print("Total Items in Stock are : ",x[0])
    instock=x[0]-itemNo
    if instock>0:
        status="Available"
    tp=(instock,status,itemId)
    sql="update stock set instock=%s,status=%s where item_id=%s"
    print("Remaining Items in Stock are : ",instock)
    mycursor.execute(sql,tp)
    mydb.commit()

def ViewSales():
    item=input("Enter Product Id : ")
    sql="select product.product_id, product.PName,product.brand,\
sales.no_of_item_sold,sales.date_of_sale,sales.sale_rate,sales.amount \
from sales, product where product.product_id=sales.item_id \
and product.product_id=%s"
    itm=(item,)
    mycursor.execute(sql,itm)
    res=mycursor.fetchall()
    print("Following are the sales of this product : ")
    print()
    for x in res:
        print(x)
        
def MenuSet():
    print("Enter 1 : To Add Product ")
    print("Enter 2 : To Edit Product ")
    print("Enter 3 : To Delete Product ")
    print("Enter 4 : To View Product ")
    print("Enter 5 : To Purchase Product")
    print("Enter 6 : To View Purchases")
    print("Enter 7 : To View Stock Details")
    print("Enter 8 : To Sell the item")
    print("Enter 9 : To View Sales Details")
    print()
    try:
        userInput = int(input("Please Select An Above Option: "))
    except ValueError:
        exit("\nHi! That's Not A Number")
    else:
        print()
        print("*"*94)
        print()
        if(userInput == 1):
            AddProduct()
        elif(userInput == 2):
            EditProduct()
        elif (userInput==3):
            DelProduct()
        elif (userInput==4):
            ViewProduct()
        elif (userInput==5):
            PurchaseProduct()
        elif (userInput==6):
            ViewPurchase()
        elif (userInput==7):
            ViewStock()
        elif (userInput==8):
            SaleProduct()
        elif (userInput==9):
            ViewSales()
        else:
            print("Please enter a valid choice. . . ")
print()
print("* * * * * * * Welcome to the Project of Apparel Store Database Management System * * * * * * *")
print("*"*94)
print()

MenuSet()

def runAgain():
    
    runAgn = input("\nDo you want to run it again Y/N: ")
    while(runAgn.lower() == 'y'):
        print()
        MenuSet()
        runAgn = input("\nDo you want to run it again Y/N: ")
runAgain()


    
