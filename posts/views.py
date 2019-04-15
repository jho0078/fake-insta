from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Post, Image
from .forms import PostForm, ImageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {'posts': posts,}
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        # 업로드 이미지는 request.FILES에 들어있다
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)     #게시글 내용 처리 끝
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)

@login_required   
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 게시글을 작성한 유저와 현재 유저가 다를 경우 수정 불가능
    if post.user != request.user:
        return redirect('posts:list')
    
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
    
    if post.user != request.user:
        return redirect('posts:list')
    
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    
            