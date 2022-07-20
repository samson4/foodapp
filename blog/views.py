from datetime import datetime
from urllib import request
from django import forms
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    
)
from blog.models import Post,rregister,Comment,OrderItem,Order,register
from django.db.models import Sum
from .forms import CommentForm,RestaurantRegisterForm


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    success_url = '/'


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
       

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/'

    fields = ['title', 'content' ,'price', 'image','image2']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content','price','image','image2']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class ResCreateView(CreateView):
    model = rregister
    fields = ['restaurant_name', 'restaurant_logo' ,'phone', 'email','location']
    template_name = 'blog/rregister_form.html'
    form = RestaurantRegisterForm()
    success_url = '/restaurants/'

# class CustomerCreateView(CreateView):
#     model = register
#     fields = ['customer_name', 'image' ,'phone', 'email','location']
#     template_name = 'blog/register.html'
#     form = CustomerRegisterForm()
#     success_url = '/restaurants/'    

class RestaurantListView(ListView):  
    model = rregister
    template_name = 'blog/restaurant_list.html'
    context_object_name = 'restaurants'
    # ordering = ['-date_posted']
    # paginate_by = 5


@login_required
def get_cart_items(request):
    cart_items = OrderItem.objects.filter(user=request.user,ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    number = cart_items.aggregate(Sum('quantity'))
    pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    total_pieces = pieces.get("item__pieces__sum")
    context = {
        'cart_items':cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'blog/cart.html', context)

# def add_to_cart(request, product_id, quantity):
#     product = Product.objects.get(id=product_id)  
#     cart = Cart(request) 
#     cart.add(product, product.unit_price, quantity)  
# def remove_from_cart(request, product_id): 
#     product = Product.objects.get(id=product_id) 
#     cart = Cart(request) 
#     cart.remove(product)    

# def get_cart(request): 
#     return render_to_response('cart.html', dict(cart=Cart(request)))    

@login_required
def addcomment(request,pk):
    eachfood= Post.objects.get(id=pk)
    form = CommentForm(instance=eachfood)
    # no_of_comments = Comment.objects.filter(id).count()
    
    if request.method == 'POST':
        form = CommentForm(request.POST,instance=eachfood)
        # id=request.POST.get(id=pk)
        if form.is_valid():
            name=request.user.username
            body=form.cleaned_data['review']
            commnets= Comment(post=eachfood,name=name,review=body,posted_on=datetime.now())
            commnets.save()
            return redirect (f'/post/{pk}') 
        else:
            print('form is invalid')    

    else:
        form=CommentForm()
    context={
        'form':form,
        # 'no_of_comments':no_of_comments
    }

    return render(request,'blog/add_comment.html',context)    

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
