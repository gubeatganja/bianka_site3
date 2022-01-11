from django.db.models import Count
from bianka_site.models import Post


def extras(request):
    years = Post.objects.order_by().values('publication_date__year').annotate(num_post=Count('publication_date__year')).filter(is_published=True)
    categories = Post.objects.order_by().values('category__name').annotate(num_post=Count('id')).filter(is_published=True)
    context = {'years': years,
               'categories': categories,
               }
    return context
