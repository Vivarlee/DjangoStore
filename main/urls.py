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
    path('calculator', views.calculator, name='gauss'),
    path('calc/gauss',views.calc_gauss, name='calc_gauss'),
    path('newton', views.newton, name='newton'),
    path('calc/newton', views.calc_newton, name='calc_newton'),
    path('jacobi', views.jacobi, name='jacobi'),
    path('calc/jacobi', views.calc_jacobi, name='calc_jacobi'),
    path('seidel', views.seidel, name='seidel'),
    path('calc/seidel', views.calc_seidel, name='calc_seidel')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)