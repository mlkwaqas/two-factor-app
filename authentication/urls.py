from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^verify$', views.verify, name='verify'),
    url(r'^home$', views.home, name='home'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^authy/callback', views.authy_callback, name='authy_callback'),
]