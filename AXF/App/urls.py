from django.conf.urls import url
from .views import *



urlpatterns = [
    url(r'^home/',home,name='home'),
    url(r'^market/',market,name='market'),
    url(r'^marketwithparams/(\d+)/(\d+)/(\d+)/',market_with_params,name='marketwithparams'),

    url(r'^cart/',cart,name='cart'),
    url(r'^cart_add/', cart_add, name='cart_add'),

    url(r'^cart_num_add/',cart_num_add,name='cart_num_add'),
    url(r'^cart_num_reduce/',cart_num_reduce,name='cart_num_reduce'),
    url(r'^cart_num_del/', cart_num_del, name='cart_num_del'),

    url(r'^cart_select/', cart_select, name='cart_select'),
    url(r'^cart_allselect/', cart_allselect, name='cart_allselect'),

    url(r'^mine/',mine,name='mine'),

    url(r'^register/',register,name='register'),
    url(r'^registerhandle/',register_handle,name='register_handle'),
    url(r'^check_username/',check_username,name='check_username'),

    url(r'^logout/',logout,name='logout'),
    url(r'^login/',login,name='login'),
    url(r'^login_handle/',login_handle,name='login_handle'),

    url(r'^order/(\d+)/',order,name='order'),
    url(r'^order_add/',order_add,name='order_add'),
    url(r'^order_change_status/',order_change_status,name='order_change_status'),
    url(r'^order_unpay/', order_unpay, name='order_unpay'),
    url(r'^order_unreceive/', order_unreceive, name='order_unreceive'),

]