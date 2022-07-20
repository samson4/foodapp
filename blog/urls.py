from django.urls import path
from django.views import View
from . import views
from .views import (
    addcomment,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    ResCreateView,
    RestaurantListView
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('order_details/', views.order_details, name='order_details'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('restaurantreg/',ResCreateView.as_view(),name='res-reg'),
    # path('register/',CustomerCreateView.as_view(),name='reg'),
    path('cart/',views.get_cart_items,name='cart'),
    path('restaurants/',RestaurantListView.as_view() ,name='restaurants'),
    path('post/<int:pk>/comment/', views.addcomment, name='addcomment'),

]
