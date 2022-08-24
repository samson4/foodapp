from django.urls import path
from django.views import View
from . import views
from .views import (
    addcomment,
    Cart,
    add_to_cart,
    CartDeleteView,
    all_orders,
    createres,
    payment,
    recommended,
    get_cultural_foods,
    get_fasting_foods,
    get_best_selling_foods,
    get_spicy_foods,
    suggest_address,
    get_new_foods,
    dashbord,
    AddressView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    RestaurantListView
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('order_details/', views.all_orders, name='order_details'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('Dashboard/', views.dashbord, name='dashboard'),
    path('restaurantreg/',views.createres,name='res-reg'),
    path('Fasting Food/',views.get_fasting_foods,name='fasting'),
    path('New Food/',views.get_new_foods,name='new'),
    path('Cultural Food/',views.get_cultural_foods,name='cultural'),
    path('Best Selling Foods/',views.get_best_selling_foods,name='best'),
    path('recommended/',views.recommended,name='recommended'),
    path('Spicy Foods/',views.get_spicy_foods,name='spicy'),
    path('cart/',views.Cart,name='cart'),
    path('restaurants/',RestaurantListView.as_view() ,name='restaurants'),
    path('post/<int:pk>/comment/', views.addcomment, name='addcomment'),
    path('post/<int:pk>/cart',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>/',views.CartDeleteView.as_view(),name='remove_from_cart'),
    path('remove_from_order/<int:pk>/',views.OrderDeleteView.as_view(),name='remove_from_order'),
    path('payment/',views.payment,name='payment'),
    path('Nearby_Services/',views.AddressView.as_view(),name='location'),
    path('Address/',views.suggest_address,name='address')
    

]
