import requests
import json

emp_endpoint = 'http://127.0.0.1:8000/api/employee/'
login_logout = 'http://127.0.0.1:8000/api/employee/auth/'
product_endpoint = 'http://127.0.0.1:8000/api/products/'
category_endpoint = 'http://127.0.0.1:8000/api/products/category/'
prod_by_category = 'http://127.0.0.1:8000/api/products/prod-by-category/'
cart_endpoint = 'http://127.0.0.1:8000/api/products/cart_bill/'
cart_add_remove = 'http://127.0.0.1:8000/api/products/add-remove-cart/'


################ methods for CRUD operation on employee ################
def post_emp():
    emp = {
            'first_name': 'Aishwarya',
            'last_name': 'Bachhan',
            'email': 'ash@gmail.com',
            'username': 'ash',
            'password': 'ash123',
            'role':2
        }
    resp = requests.post(emp_endpoint , data = json.dumps(emp))
    print(resp.status_code)
    print(resp.json())



def get_emp_by_same_endpoint(id = None):
    data = {}
    print(f'data from get_emp {data}')
    if id:
        data['id'] = id
    resp = requests.get(emp_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for CRUD operation on employee ################
################ methods for CRUD operation on product ################

def get_prod_by_same_endpoint(id = None):
    data = {}
    if id:
        data['id'] = id
    resp = requests.get(product_endpoint , data = json.dumps(data))
    print(resp.status_code)
    for elem in resp.json():
        print(f'id : {elem.get("pk")}\n')
        for key,value in elem.get("fields").items():
            if key == 'category':
                data = {'id':value}
                cat_resp = requests.get(category_endpoint , data = json.dumps(data))
                print(f"{key} : {cat_resp.json()[0].get('fields').get('category_name')}\ncategory id : {value}\n")
            else:
                print(f'{key} : {value}\n')
        print('\n\n')
    # print(resp.json())

def post_prod():
    prod = {
            'product_name': 'Samsung TV',
            'category': 'Electronics',
            'description': 'samsung samsung samsung samsungsamsung samsung samsung samsung samsung samsung samsung samsung samsung samsung samsung samsung',
            'price': 5000,
        }
    resp = requests.post(product_endpoint , data = json.dumps(prod))
    print(resp.status_code)
    print(resp.json())

def delete_prod_by_same_endpoint(id = None):
    data = {'id': id}
    resp = requests.delete(product_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

def put_prod_by_same_endpoint(id = None):
    data = {'id': id}
    resp = requests.put(product_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for CRUD operation on product ################

################ methods for CRUD operation on category ################
def get_cat_by_same_endpoint(id = None):
    data = {}
    print(f'data from get_cat {data}')
    if id:
        data['id'] = id
    resp = requests.get(category_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

def post_cat():
    prod = {
            'product_name': 'Samsung TV',
            'category': 'Electronics',
            'description': 'samsung samsung samsung samsungsamsung samsung samsung samsung samsung samsung samsung samsung samsung samsung samsung samsung',
            'price': 5000,
        }
    resp = requests.post(category_endpoint , data = json.dumps(prod))
    print(resp.status_code)
    print(resp.json())

def delete_cat_by_same_endpoint(id = None):
    data = {'id': id}
    resp = requests.delete(category_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

def put_cat_by_same_endpoint(id = None):
    data = {'id': id}
    resp = requests.put(category_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for CRUD operation on category ################

################ methods for getting all products by category name/id ################

def get_prod_by_category(id):
    data = {}
    data['id'] = id
    resp = requests.get(prod_by_category , data = json.dumps(data))
    print(f"All products that comes under {requests.get(category_endpoint , data = json.dumps(data)).json()[0].get('fields').get('category_name')}\n\n")
    print(resp.status_code)
    for elem in resp.json():
        print(f'id : {elem.get("pk")}\n')
        for key,value in elem.get("fields").items():
            if key == 'category':
                continue
            else:
                print(f'{key} : {value}\n')
        print('\n\n')
    # print(resp.json())


############# Login Logout ################
def post_login():
    prod = {
            'username': 'shreyash',
            'password': '123',
        }
    resp = requests.post(login_logout , data = json.dumps(prod))
    print(resp.status_code)
    print(resp.json())
    session = resp.json().get('session')
    print(f'session ===== {session}')
    return session

def get_logout():
    data = {}
    resp = requests.get(login_logout , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

############# Login Logout ################


################ methods for getting cart of user  ################
def get_cart(user = None):
    data = {}
    print(f'data from get_emp {data}')
    if user:
        data['user'] = user
    resp = requests.get(cart_endpoint , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for adding product in cart ################
def post_add_to_cart(id,user):
    data = {'id':id,
            'user':user,
            }
    resp = requests.post(cart_add_remove , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for removing product from cart ################
def delete_item_from_cart(id,user):
    data = {'id': id,
            'user': user}
    resp = requests.delete(cart_add_remove , data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())

################ methods for getting cart bill ################
def get_bill(user,session):
    data = {"user":user,"session":session}
    print(f"session from partner app ===== {session}")
    cookies = {'enwiki_session': session}
    resp = requests.get(cart_add_remove , data = json.dumps(data),cookies = cookies)
    print(resp.status_code)
    print(resp.json())


# get_emp_by_same_endpoint()
# delete_by_same_endpoint(10)
# post_data()
# post_data()
# get_prod_by_same_endpoint()
# get_cat_by_same_endpoint(id = 6)

# get_prod_by_category(id = 6)

session = post_login()
# get_cart('shreyash')
# get_prod_by_same_endpoint(11)
# post_add_to_cart(9,'shreyash')
# delete_item_from_cart(9,'shreyash')
# get_cart('shreyash')
# get_bill('shreyash',session)
get_logout()