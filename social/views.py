from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View,TemplateView,DeleteView, UpdateView,RedirectView,DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post,Postcomment
from .forms import PostForm,PostcommentForm,feedbackForm
from profiles.models import Profiles
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

   
class PostView(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.all()
        paginator = Paginator(post, 25) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = PostForm()
        context={'form':form,'page_obj': page_obj}      
        return render(request,'posts/post.html',context)

    def post(self,request,*args,**kwargs):
        profile = Profiles.objects.get(user=request.user)
        form = PostForm(request.POST,request.FILES)        
        if form.is_valid():
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            content = form.cleaned_data['content']
            posts = Post(title = title, image = image, content = content,author = profile)
            posts.save()
        return HttpResponseRedirect('/')   


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    #context_object_name = 'post'
    template_name = "posts/update_post.html"
    success_url = reverse_lazy('posts:home')
    
    # def get_queryset(self):
    #     post = super().get_queryset()
    #     return post.filter(author = self.request.user)
    

    # def form_valid(self,form):
    #     instance = form.save()
    #     return redirect('posts:home')

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy('posts:home')


class PostDetail(LoginRequiredMixin,DetailView):
    model = Post
    template_name='posts/post_details.html'


class PostLikeToggle(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,slug=None,*args, **kwargs):
        #slug = self.kwargs.get("slug")
        #print(slug)
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.liked.all():
                post.liked.remove(user)
            else:
                post.liked.add(user)
        return url_
    
@login_required
def post_like(request):
    profile = Profiles.objects.get(user=request.user)
    if request.method == 'POST':
        user = request.user
        post_id= request.POST.get('post_id')
        post_obj= Post.objects.get(id=post_id)
        #print(post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
    return  redirect('posts:home') 

class PostdetailView(LoginRequiredMixin,View):
    def get(self, request,slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = Postcomment.objects.filter(post=post,reply=None)
        cmt_form = PostcommentForm()
        context={'form':cmt_form,
        'post':post,
        'comments':comments}        
        return render(request,'posts/post_details.html',context)

    def post(self, request,slug,*args,**kwargs):
        profile = Profiles.objects.get(user=request.user)
        post = get_object_or_404(Post, slug=slug)
        form = PostcommentForm(request.POST)
        if form.is_valid():
            #instance = form.save(commit=False)
            #instance.user = request.user
            #instance.post = Post.objects.get(id=request.POST.get('post_id'))
            #instance.save()
            #form =  PostcommentForm()
            comment = request.POST.get('comment')
            replys = request.POST.get('comment_id')
            reply_cmt = None
            if replys:
                reply_cmt =  Postcomment.objects.get(id=replys)
            comment= Postcomment.objects.create(user=profile,post=post,comment=comment,reply=reply_cmt)
            comment.save()
        return redirect('posts:post_details',slug=slug)    


class feedbackView(View):
    def get(self, request, *args, **kwargs):
        form = feedbackForm()
        context = {'form':form}
        return render(request,'posts/feedback.html',context)

    def post(self, request, *args, **kwargs):
        form = feedbackForm(request.POST or None)
        if form.is_valid():
           form.save()
           messages.success(request, 'Thanks for your feedback!')
        return redirect('posts:feedback')

def search(request):
    query = request.GET['q']
    searchs = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    users = User.objects.filter(
            Q(username__icontains=query)
        )
    context = {
        'searchs':searchs,
        'user':users,
        'query':query
    }
    return render(request,'posts/search.html',context)
    #return HttpResponse("this is search")


def error_404(request,exception):
    return render(request,'404.html')

def error_403(request,exception):
    return render(request,'403.html')

def error_400(request,exception):
    return render(request,'400.html')

def error_500(request,exception):
    return render(request,'500.html')