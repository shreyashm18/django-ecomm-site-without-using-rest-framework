from django.shortcuts import render,redirect
from .models import Products , Category , Cart, Cartitems
from .forms import ProductForm,CartItemForm, CategoryForm, SelectCustomer
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import User,auth

#### without framework ####
from django.shortcuts import render
from django.views.generic import View
import json
from django.http import HttpResponse
# Create your views here.
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .mixins import ResponseMixin
from.util import is_json
#### without framework ####


@method_decorator(csrf_exempt, name='dispatch')        
class ProductCRUDSingleEndpoint(View,ResponseMixin):
    def get_object_by_id(self , id):
        try:
            e = Products.objects.get(id = id)
        except Products.DoesNotExist:
            e = None
        return e
    def get(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        if id is None:
            query_set = Products.objects.all()
            for i in query_set:
                print(i.category)
            print(f'query_set = {query_set}')
            json_data = serialize('json' , query_set)
            return self.render_to_http_response(json_data)
        else:
            prod = self.get_object_by_id(id = id)
            if prod is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            json_data = serialize('json' , [prod,])
            return self.render_to_http_response(json_data)

    def post(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        prod_data = json.loads(data)
        prod_form = ProductForm(prod_data)
        if prod_form.is_valid():
            prod_form.save()
            json_data = json.dumps({'msg':"data updated successfully in database"})
            return self.render_to_http_response(json_data)
        if prod_form.errors:
            json_data = json.dumps(prod_form.errors)
            return self.render_to_http_response(json_data ,  status = 400)    

    def put(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        # p_data.pop('id')
        if id is None:
            json_data = json.dumps({'msg':"Cant update data without id, you must provide id"})
            return self.render_to_http_response(json_data ,  status = 400)
        else:
            prod = self.get_object_by_id(id = id)
            if prod is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            prod_data = {
                "product_name": prod.product_name,
                "category": prod.category, 
                "description": prod.description, 
                "price": prod.price
            }
            # provided_data = json.loads(p_data)
            prod_data.update(p_data)
            prod_form = StudentForm(prod_data , instance= prod)
            if prod_form.is_valid():
                prod_form.save()
                json_data = json.dumps({'msg':"data updated successfully in database"})
                return self.render_to_http_response(json_data)
            if prod_form.errors:
                json_data = json.dumps(prod_form.errors)
                return self.render_to_http_response(json_data ,  status = 400)

    def delete(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        # p_data.pop('id')
        if id is None:
            json_data = json.dumps({'msg':"Cant delete data without id, you must provide id"})
            return self.render_to_http_response(json_data ,  status = 400)
        else:
            prod = self.get_object_by_id(id = id)
            if prod is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            prod.delete()
            json_data = json.dumps({'msg':"data deleted successfully"})
            return self.render_to_http_response(json_data)

@method_decorator(csrf_exempt, name='dispatch')   
class CategoryCRUDSingleEndpoint(View,ResponseMixin):
    def get_object_by_id(self , id):
        try:
            e = Category.objects.get(id = id)
        except Category.DoesNotExist:
            e = None
        return e
    def get(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        if id is None:
            query_set = Category.objects.all()
            json_data = serialize('json' , query_set)
            return self.render_to_http_response(json_data)
        else:
            cat = self.get_object_by_id(id = id)
            if cat is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            json_data = serialize('json' , [cat,])
            return self.render_to_http_response(json_data)

    def post(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        category_data = json.loads(data)
        category_form = CategoryForm(category_data)
        if category_form.is_valid():
            category_form.save()
            json_data = json.dumps({'msg':"data updated successfully in database"})
            return self.render_to_http_response(json_data)
        if category_form.errors:
            json_data = json.dumps(category_form.errors)
            return self.render_to_http_response(json_data ,  status = 400)    

    def put(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        # p_data.pop('id')
        if id is None:
            json_data = json.dumps({'msg':"Cant update data without id, you must provide id"})
            return self.render_to_http_response(json_data ,  status = 400)
        else:
            category = self.get_object_by_id(id = id)
            if category is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            category_data = {
                "category_name": category.category_name, 
            }
            # provided_data = json.loads(p_data)
            category_data.update(p_data)
            cat_form = CategoryForm(category_data , instance= category)
            if cat_form.is_valid():
                cat_form.save()
                json_data = json.dumps({'msg':"data updated successfully in database"})
                return self.render_to_http_response(json_data)
            if cat_form.errors:
                json_data = json.dumps(cat_form.errors)
                return self.render_to_http_response(json_data ,  status = 400)

    def delete(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        # p_data.pop('id')
        if id is None:
            json_data = json.dumps({'msg':"Cant delete data without id, you must provide id"})
            return self.render_to_http_response(json_data ,  status = 400)
        else:
            cat = self.get_object_by_id(id = id)
            if cat is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            cat.delete()
            json_data = json.dumps({'msg':"data deleted successfully"})
            return self.render_to_http_response(json_data)

class ProductByCategoryId(View,ResponseMixin):
    def get_object_by_id(self , id):
        try:
            e = Products.objects.filter(category = id)
        except Products.DoesNotExist:
            e = None
        return e
    def get(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        prod = self.get_object_by_id(id = id)
        print(f'prod by cat from server = {prod}')
        if prod is None:
            json_data = json.dumps({'msg':"data not found, please enter correct id"})
            return self.render_to_http_response(json_data ,  status = 400)
        json_data = serialize('json' , prod)
        return self.render_to_http_response(json_data)

@method_decorator(csrf_exempt, name='dispatch')   
class CartAddRemove(View,ResponseMixin):
    def get_object_by_id(self , id):
        try:
            e = Products.objects.get(id = id)
        except Products.DoesNotExist:
            e = None
        return e
    def post(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        user = p_data.get('user', None)
        user = User.objects.get(username = user)
        if not id or user:
            json_data = json.dumps({'msg':"Please provide id and username both"})
            return self.render_to_http_response(json_data,  status = 400)
        print(f'id === {id} +++++++++++++')
        prod = self.get_object_by_id(id = id)
        print(f'prod =================== {prod} ')
        if prod is None:
            json_data = json.dumps({'msg':"data not found, please enter correct id"})
            return self.render_to_http_response(json_data ,  status = 400)
        
        try:
            cart = Cart.objects.get(user = user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user = user,cart_name=str(user))
        cart.save()
        try:
            cart_item=Cartitems.objects.get(prod_id=id,cart_name=str(user))
            print(f'##########cart name = {cart_item.cart_name}###########')
            
            cart_item.qnty += 1
            cart_item.final_price = cart_item.item_price * cart_item.qnty
            cart_item.save()
            cart.total += cart_item.item_price
            if cart.total > 10000:
                cart.discounted_price = cart.total - 500
            print(f'current item price {cart_item.item_price} and total price {cart.total}')
            cart.save()
        except Cartitems.DoesNotExist:
            cart_item = Cartitems.objects.create(cart = cart,cart_name=str(user), item_name = prod.product_name, item_price =prod.price, final_price=prod.price, prod_id= id)
            cart_item.save()
            cart.total += cart_item.item_price
            if cart.total > 10000:
                cart.discounted_price = cart.total - 500
            print(f'current item price {cart_item.item_price} and total price {cart.total}')
            cart.save()
        json_data = json.dumps({'msg':"Item added to cart"})
        return self.render_to_http_response(json_data)

    def delete(self,request,*args,**kwrgs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        p_data = json.loads(data)
        id = p_data.get('id', None)
        print(f'######## id ==== {id} ############')
        prod = self.get_object_by_id(id = id)
        user = p_data.get('user', None)
        user = User.objects.get(username = user)
        if id is None:
            json_data = json.dumps({'msg':"Cant delete data without id, you must provide id"})
            return self.render_to_http_response(json_data ,  status = 400)
        if user is None:
            json_data = json.dumps({'msg':"Please provide id and username both"})
            return self.render_to_http_response(json_data,  status = 400)
        cart = Cart.objects.get(user = user)
        cart_item=Cartitems.objects.get(prod_id=prod.id,cart_name=str(user))
        if (cart_item.qnty > 1):
            cart_item.qnty -= 1
            cart_item.final_price = cart_item.item_price * cart_item.qnty
            cart_item.save()
            cart.total -= cart_item.item_price
            if cart.total > 10000:
                cart.discounted_price = cart.total - 500
            if cart.total <= 10000:
                cart.discounted_price = None
            print(f'current item price {cart_item.item_price} and total price {cart.total}')
            cart.save()
        else:
            cart_item.delete()
            cart.total -= cart_item.item_price
            if cart.total > 10000:
                cart.discounted_price = cart.total - 500
            if cart.total <= 10000:
                cart.discounted_price = None
            print(f'current item price {cart_item.item_price} and total price {cart.total}')
            cart.save()
            json_data = json.dumps({'msg':"data deleted successfully"})
            return self.render_to_http_response(json_data)

    def get(self,request,*args,**kwrgs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        session_id = p_data.get('session', None)
        print(f'session id === {session_id}   +++++++++++')
        user = p_data.get('user', None)
        print(f'requested user ==== {request.user} ')
        print(f'++++++++++++++ session key == {request.session.session_key}')
        if not request.session.session_key:
            request.session.create()
            print(f'requested user ==== {request.user} ')
            print(request.session.session_key)
        if user is None:
            json_data = json.dumps({'msg':"Please provide username "})
            return self.render_to_http_response(json_data,  status = 400)
        user = User.objects.get(username = user)
        cart = Cart.objects.get(user = user)
        if cart is None:
            json_data = json.dumps({'msg':"data not found"})
            return self.render_to_http_response(json_data ,  status = 400)
        ct = cart.cartitems_set.all()
        total = 0 
        dis_msg = ''
        discounted_price = 0
        
        for citem in ct:
            print(citem.final_price)
            total += citem.final_price
        print(f'total = {total}')
        if total > 10000:
            dis_msg = 'Congratulations you are getting 500 RS discount'
            discounted_price = total - 500
        print(f' ++++++++++++ cart = {cart} +++++++++++++')
        print(f' ++++++++++++ cart item = {ct} +++++++++++++')
        json_data = serialize('json' , [cart,])
        return self.render_to_http_response(json_data)
        
class cart_bill(View,ResponseMixin):
    def get_object_by_name(self , user):
        try:
            cart = Cart.objects.get(user = user)
            print(f'cart ================= {cart}')
        except Cart.DoesNotExist:
            cart = None
        return cart
    def get(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data)
        p_data = json.loads(data)
        session_id = p_data.get('session', None)
        print(f'session id === {session_id}   +++++++++++')
        user = p_data.get('user', None)
        print(f'requested user ==== {request.user} ')
        print(f'++++++++++++++ session key == {request.session.session_key}')
        if not request.session.session_key:
            request.session.create()
            print(f'requested user ==== {request.user} ')
            print(request.session.session_key)
        if user is None:
            json_data = json.dumps({'msg':"Please provide  username "})
            return self.render_to_http_response(json_data,  status = 400)
        print(f'cart user to find = {user}')
        user = User.objects.get(username = user)
        cart = self.get_object_by_name(user = user)
        if cart is None:
            json_data = json.dumps({'msg':"User not found"})
            return self.render_to_http_response(json_data ,  status = 400)
        ct = Cartitems.objects.filter(cart = cart)
        print(ct)
        json_data = serialize('json' , ct)
        return self.render_to_http_response(json_data)