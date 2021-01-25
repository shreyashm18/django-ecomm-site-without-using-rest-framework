from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from Product.models import Category

# Create your views here.
from django.shortcuts import render
from django.views.generic import View
import json
from django.http import HttpResponse
# Create your views here.
from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from Product.mixins import ResponseMixin
from Product.util import is_json




@method_decorator(csrf_exempt, name='dispatch')        
class EmployeeCRUDSingleEndpoint(View,ResponseMixin):
    def get_object_by_id(self , id):
        try:
            e = User.objects.get(id = id)
        except User.DoesNotExist:
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
            query_set = User.objects.all()
            json_data = serialize('json' , query_set)
            return self.render_to_http_response(json_data)
        else:
            user = self.get_object_by_id(id = id)
            if user is None:
                json_data = json.dumps({'msg':"data not found, please enter correct id"})
                return self.render_to_http_response(json_data ,  status = 400)
            json_data = serialize('json' , [user,])
            return self.render_to_http_response(json_data)
            
    def post(self , request , *args , **kwargs):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        emp_data = json.loads(data)
        emp_form = UserForm(emp_data)
        if emp_form.is_valid():
            emp_form.save()
            json_data = json.dumps({'msg':"data updated successfully in database"})
            return self.render_to_http_response(json_data)
        if emp_form.errors:
            json_data = json.dumps(emp_form.errors)
            return self.render_to_http_response(json_data ,  status = 400)    


@method_decorator(csrf_exempt, name='dispatch')
class LoginLogoutApi(View,ResponseMixin):
    def post(self,request):
        data = request.body
        valid = is_json(data)
        if not valid:
            json_data = json.dumps({'msg':"Please provide data in json format"})
            return self.render_to_http_response(json_data ,  status = 400)
        user_data = json.loads(data)
        print(f'user data = {user_data}')
        username=user_data['username']
        password=user_data['password']
        print(f'+++++++pass =  {password} ++++++++++')
        user = auth.authenticate(request,username = username, password = password)
        if user:
            auth.login(request,user=user)
            print(f'logged in user =====  {request.user} ++++++++++++++++++++++++')
            print(f'++++++++++++++ session key == {request.session.session_key}')
            json_data = json.dumps({'msg':"You have loggedin successfully",'user':user.username,'session':request.session.session_key})
            return self.render_to_http_response(json_data)       
        else:
            json_data = json.dumps({'msg':"Wrong Credintials"})
            return self.render_to_http_response(json_data)
        
    def get(self,request):
        auth.logout(request)
        print(f'++++++++++++++ {request.user} ++++++++++++++++')
        json_data = json.dumps({'msg':"Logged Out successfully"})
        return self.render_to_http_response(json_data)
