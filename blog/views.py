from django.http import Http404
from django.shortcuts import render
from .models import Post, Comment, SubComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def all_posts(request):
    blog_posts = Post.objects.filter(publish=True)
    all_posts = Paginator(blog_posts, per_page=2)
    page = request.GET.get('page')

    try:
        posts = all_posts.page(page)
    except PageNotAnInteger:
        posts = all_posts.page(1)
    except EmptyPage:
        raise Http404()
    context = {
        'posts': posts
    }
    return render(request, "blog.html", context)


def blog_single(request, slug):
    try:
        post = Post.objects.filter(slug=slug).first()
        post.views += 1
        post.save()
        if request.method == 'POST':
            comment = request.POST.get('comment')
            comm_id = request.POST.get('comm_id')
            name = request.POST.get('name')
            email = request.POST.get('email')
            if comm_id:
                SubComment(post=post,
                           user=name,
                           email=email,
                           message=comment,
                           comment=Comment.objects.get(id=int(comm_id))
                           ).save()
            else:
                Comment(post=post,
                        user=name,
                        email=email,
                        message=comment
                        ).save()
                post.save()
        comments = []
        post_comments = Comment.objects.filter(post=post)
        for c in post_comments:
            sc = SubComment.objects.filter(comment=c)
            comments.append([c, sc])
        context = {
            'post': post,
            'comments': comments
        }
    except:
        raise Http404("No such blog post.")

    return render(request, "blogviews.html", context)


def search(request):
    search_query = request.GET.get('search-query')
    posts = Post.objects.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query)
    ).distinct()
    context = {
        'search_query': search_query,
        'search_results': posts,
    }
    return render(request, 'blog_search.html', context)
