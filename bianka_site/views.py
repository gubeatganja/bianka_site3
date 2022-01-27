from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Post
from .forms import CommentForm


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
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
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
        print(category_query)
        if is_valid(year_query):
            qs = qs.filter(publication_date__year__in=year_query)
        if is_valid(category_query):
            qs = qs.filter(category__name__in=category_query).distinct()
        if order_by_query == 'oldest':
            qs = qs.order_by('publication_date')
        number_of_posts = qs.count()
        p = Paginator(qs, 4)
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
        return Post.objects.filter(Q(title__icontains=self.request.GET.get('search')) |
                                   Q(main_text__icontains=self.request.GET.get('search'))).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search')
        return context


class AddComment(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())

