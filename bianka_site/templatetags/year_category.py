from django import template
from bianka_site.models import Post, Category
from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_years():
    print(Post.objects.filter(is_published=True).values('publication_date__year').annotate(num_post=Count('id')) \
        .distinct().order_by())
    return Post.objects.filter(is_published=True).values('publication_date__year').annotate(num_post=Count('id')) \
        .distinct().order_by()


@register.simple_tag
def get_categories():
    print(Category.objects.filter(posts__is_published=True).annotate(num_post=Count('id')).distinct().order_by('-name'))
    return Category.objects.filter(posts__is_published=True).annotate(num_post=Count('id')).distinct().order_by('-name')


""" This retrieve None category also of posts without categories """
# @register.simple_tag
# def get_categories():
#   return Post.objects.values('category__name').annotate(num_post=Count('id')).filter(is_published=True).distinct()
