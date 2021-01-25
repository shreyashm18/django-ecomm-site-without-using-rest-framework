from .models import Cartitems

def items_count(request):
    count = Cartitems.objects.filter(cart_name=request.user)
    print(count.count())
    count = count.count()
    print("Items count - ", count)
    return {"items_count": count}