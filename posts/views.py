from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Post
from .forms import PostForm

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {'posts': posts,}
    return render(request, 'posts/list.html', context)

def create(request):
    if request.method == 'POST':
        # 업로드 이미지는 request.FILES에 들어있다
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    
    else:
        post_form = PostForm()
    context = {'post_form': post_form}
    return render(request, 'posts/form.html', context)

    
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    
    else:
        # post의 정보를 가져오기 위해 instance=post 사용
        post_form = PostForm(instance=post)
    context = {'post_form': post_form}
    return render(request, 'posts/form.html', context)
    
    
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    
            