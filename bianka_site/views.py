from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Post, Like
from .forms import CommentForm, LikeForm


def home(request):
    return render(request, "base.html")


def test(request):
    return render(request, "test.html")


class PostView(View):
    """List of posts"""
    model = Post

    def get(self, request):
        posts = Post.objects.filter(is_published=True)
        p = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        context = {'posts': posts,
                   'page_obj': page_obj,
                   }
        return render(request, 'base.html', context)


class PostDetailView(DetailView):
    """Full description of single post"""
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        current_post = self.get_object()
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['like_form'] = LikeForm()
        context['posts'] = Post.objects.filter(is_published=True).order_by('-publication_date').\
            filter(publication_date__lte=current_post.publication_date)[:3]
        return context


def is_valid(value):
    if value != '' and value is not None:
        return value


class FilterPostView(View):
    model = Post

    def get(self, request):
        qs = Post.objects.filter(is_published=True)
        order_by_query = request.GET.get('order_by')
        year_query = request.GET.getlist('year')
        year_query = list(map(int, year_query))
        category_query = request.GET.getlist('category')
        print(year_query)
        print(category_query)
        if is_valid(year_query):
            qs = qs.filter(publication_date__year__in=year_query)
        if is_valid(category_query):
            qs = qs.filter(category__name__in=category_query).distinct()
        if order_by_query == 'oldest':
            qs = qs.order_by('publication_date')
        number_of_posts = qs.count()
        p = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        context = {'page_obj': page_obj,
                   'number_of_posts': number_of_posts,
                   'year_query': year_query,
                   'category_query': category_query,
                   }
        return render(request, 'filtered.html', context)


class Search(ListView):
    paginate_by = 10
    template_name = 'search.html'

    def get_queryset(self):
        queryset = Post.objects.filter(Q(title__icontains=self.request.GET.get('search')) |
                                   Q(main_text__icontains=self.request.GET.get('search'))).distinct()
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search')
        return context


class FilterCategoryView(ListView):
    def get(self, request):
        category_query = request.GET.getlist('category')
        qs = Post.objects.filter(is_published=True).filter(category__name__in=category_query)



class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        print(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())


class AddLike(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def post(self, request):
        form = LikeForm(request.POST)
        if form.is_valid():
            Like.objects.update_or_create(
                ip=self.get_client_ip(request),
                post_id=int(request.POST.get("post")),
                defaults={"like": request.POST.get("add_like")}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
