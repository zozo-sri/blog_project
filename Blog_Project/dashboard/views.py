from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post

@login_required
def dashboard(request):
    # Superuser → see all posts
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(author=request.user)

    return render(request, 'dashboard/dashboard.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user
        )
        return redirect('dashboard')

    return render(request, 'dashboard/create_post.html')


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # 🔐 SECURITY
    if post.author != request.user and not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()
        return redirect('dashboard')

    return render(request, 'dashboard/edit_post.html', {'post': post})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    # 🔐 SECURITY
    if post.author != request.user and not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == "POST":
        post.delete()
        return redirect('dashboard')

    return render(request, 'dashboard/delete_post.html', {'post': post})