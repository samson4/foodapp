from datetime import datetime
from multiprocessing import context
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
from blog.models import Post,rregister,Comment,OrderItem,Order,register,Address
from django.db.models import Sum,Max,Min,Avg
from .forms import CommentForm,RestaurantRegisterForm


def home(request,Post_id):


    if 'recently_viewed' in request.session:
        if Post_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(Post_id)
        recently_viewed_post=Post.objects.filter(pk__in=request.session['recently_viewed'])
        request.session['recently_viewed'].insert(0,Post_id)

        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
         request.session['recently_viewed']= [Post_id]

    request.session.modified=True  

    
    average=Comment.objects.filter(user=request.user).aggregate(Avg('rating'))
        
    context = {
        'posts': Post.objects.all(),
        'recently_viewed_post':recently_viewed_post,
        'average':average
    }  
   
 

    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


def get_fasting_foods(request):
    fasting=Post.objects.filter(labels='Fasting Food')
    context={
        'fasting':fasting
    }
    return render(request,'blog/labels.html',context)

def get_cultural_foods(request):
    cultural = Post.objects.filter(labels='Cultural Food')
    context={
        'cultural':cultural
    }
    return render(request,'blog/labels.html',context)


def get_new_foods(request):
    new = Post.objects.filter(labels='New Food')
    context={-
        'new':new
    }
    return render(request,'blog/labels.html',context)


def recommended(request):
    com = Comment.objects.all()
    Average=com.aggregate(Avg('rating'))
    context={
        'Average':Average
    }
    return render(request,'blog/labels.html',context)


def get_best_selling_foods(request):
    
    best=Post.objects.filter(labels='Best Selling Foods')
    context={
        'best':best
    }
    return render(request,'blog/labels.html',context)


def get_spicy_foods(request):
    
    spicy=Post.objects.filter(labels='Spicy Foods')
    context={
        'spicy':spicy
    }
    return render(request,'blog/labels.html',context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    success_url = '/'



    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class UserCartListView(ListView):
    model = Order
    template_name = 'blog/cart.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'carts'
    paginate_by = 5
    success_url = '/cart'
    
class PostDetailView(DetailView):
    model = Post
       

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/'

    fields = ['title', 'content' ,'labels','price', 'image','image2']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)    


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
    fields = ['restaurant_name','restaurant_logo' ,'phone', 'email','location']
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
def Cart(request):
    customer = request.user
    # order, created = Order.objects.get_or_create(Customer=customer,order__complete=False)
    # items = order.orderitem_set.all()
    Item = OrderItem.objects.filter(Customer=customer,status='Active',order__complete=False)
    number_of_orders = Item.count()
    bill = Item.aggregate(Sum('product__price'))
    number = Item.aggregate(Sum('quantity'))
    pieces = Item.aggregate(Sum('product__pieces'))
    total = bill.get("product__price__sum")
    count = number.get("quantity__sum")
    total_pieces = pieces.get("product__pieces__sum")
    # sun = total*total_pieces
    # print=(Item.Post.price)*(total_pieces)
    context = {
        'total': total,
        'count': count,
        'number_of_orders': number_of_orders,
        'number':number,
        'total_pieces': total_pieces,
        'Item' : Item,
        
    }
    return render(request, 'blog/cart.html', context)

def all_orders(request,*args,**kwargs):
    customer=request.user
    orders=Order.objects.all()
    # complete_orders=OrderItem.objects.filter(orders__complete=True)
    # Order.objects.update(complete=True)
    choices = OrderItem.objects.all()
    pending = OrderItem.objects.filter(Customer=customer,status='Active')
    complete=OrderItem.objects.filter(Customer=customer,status='Delivered')
    context={
        'pending':pending,
        'complete':complete,
        'choices':choices
    }
    if request.method =='POST':
            OrderItem.objects.update(Customer=request.user,status='Delivered')
    return render(request,'blog/order_detail.html',context)

def add_to_cart(request,pk):
    customer = request.user
    product = Post.objects.get(id=pk)
    order=Order.objects.get(customer=customer)
    # cart = Cart(request) 
    # cart.add(product, product.unit_price, quantity)  
    OrderItem.objects.create(Customer=customer,product=product,order=order,quantity=product.pieces,status='Active')
    return redirect('/cart/')

class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderItem
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.Customer:
            return True
        return False

# def remove_from_cart(request, product_id): 
#     customer=request.user
#     order=Order.objects.get(customer=customer)
#     product = OrderItem.objects.get(pk=product_id) 
#     # cart = OrderItem(request) 

#     item=OrderItem.objects.get(Customer=customer,product=product,order=order,quantity=order.quantity,status='Active')
#     OrderItem.remove(item)    
#     return redirect('/cart/')
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
            rating = form.cleaned_data['rating']
            commnets= Comment(post=eachfood,name=name,review=body,rating=rating,posted_on=datetime.now())
           
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

class AddressView(ListView):
    model = Address    
    template_name = 'blog/location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.all()
        return context

def payment(request):
    customer = request.user
    Item = OrderItem.objects.filter(Customer=customer,status='Active',order__complete=False)
    bill = Item.aggregate(Sum('product__price'))
    total = bill.get("product__price__sum")
    pieces = Item.aggregate(Sum('product__pieces'))
    total_pieces = pieces.get("product__pieces__sum")
    context={
        'Item':Item,
        'total':total,
        'total_pieces':total_pieces
    }
    return render(request,'blog/payment.html',context)

