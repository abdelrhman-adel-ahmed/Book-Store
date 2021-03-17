from decimal import Decimal

from django.conf import settings
from store.models import Product


class Basket:
    '''
        base basket class for creating sesssions if not already exisited
    '''
    def __init__(self,request):
        #print('initiate session')
        self.session = request.session  
        #skey:session key
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        #basket have the dict that have the session data 
        self.basket = basket

        '''
        self.session=request.session
        basket=self.session.get('skye')
        if 'skey' not in request.session:
            <!--error was here bakset instead of basjet->
            bakset=self.session['skey']={}
        self.basket=basket
        '''



    def add(self,product,product_qty):
        '''
        add and update user session data
        '''
        product_id=str(product.id)
        if product_id not in self.basket:
            #we store it as string to store the floating point of the price
            self.basket[product_id]={'price':str(product.regular_price),'qty':int(product_qty)}
        else:
            self.basket[product_id]['qty']=product_qty


        #save the changes we made
        self.session.modified = True

    def delete(self,product_Id):
        '''
        delete item from the basket
        '''        
        product_id=str(product_Id)
        if product_id in self.basket:
            del self.basket[product_id]
        print('deleted')
        self.session.modified = True

    def update(self,product_Id,product_Qty):
        '''
        update qty in items
        '''        
        print('update')
        product_id = str(product_Id)
        self.basket[product_id]['qty'] = product_Qty
        self.session.modified = True

    def get_item_total(self,item_id):
        item_i=str(item_id)
        item=self.basket[item_i]
        item['total_price']=int(float(item['price']))*item['qty']
        return item['total_price']

    def __len__(self):
        '''
        if we select one item and then select two item it will show 3 item , we need to refresh 
        to show the correct value wich is 2 
        '''
        '''
        count the qty of all items in the basket
        '''
        """
        the patterns that its add another item in the dict with the new values without yet remove the old ones
        """
        #print(self.basket.keys())
        #print(self.basket.values())
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        '''
        collect the product_id in the session data and get query the data for all the product from 
        the database and return them
        '''
        products_id=self.basket.keys()
        products=Product.objects.filter(id__in=products_id)
        basket=self.basket.copy()

        for product in products:
            ''''
            for every product_id in the dict add another key to the dict called product and the value of that 
            key is the product information  basket={'skey' : {1:{'price' : ,'qty' : , 'product' : }}}.
            notes that we add to the copy of the basket not the original one.
            '''
            basket[str(product.id)]['product']=product
        
        '''
        what will happen :
        1- we iteate through the item in the basket 
        2-__iter__ method will get called 
        3-we will reach this for loop where we use generator(yiled)
        4-the values will get retrived one after another with explicite next()fucntion that for loops in python
        implemented with ,in the template loop ...
        '''
        for item in basket.values():
             item['price']=Decimal(item['price'])
             item['total_price']=item['qty']*item['price']
             yield item

    def get_total_price(self):
        subtotal= sum(Decimal(item['price'])*item['qty'] for item in self.basket.values())
        if subtotal ==0:
            shipping=Decimal(0.00)
        else:
            shipping=Decimal(11.50)

        total=subtotal+shipping
        return total

    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        
    def clear(self):
        #remove the basket from the session
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True




        

        

