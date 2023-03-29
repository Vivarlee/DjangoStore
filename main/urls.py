from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('checkusername', views.checkusername, name='checkusername'),
    path('calculator', views.calculator, name='calc'),
    path('calc/gauss',views.calcGauss, name='Gauss'),
    # path('shop', views.shop, name='shop'),
    # path('editor', views.editor, name='editor'),
    # path('cart', views.cart, name='cart'),
    # path('deleteitem', views.delete_item, name='deleteitem'),
    # path('addtocart', views.add_to_cart, name="addtocart"),
    # path('removefromcart', views.remove_from_cart, name='removefromcart'),
    # path('deletefromcart', views.delete_from_cart, name="renivefromcart"),
    # path('placeanorder', views.place_order, name="placeorder"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)