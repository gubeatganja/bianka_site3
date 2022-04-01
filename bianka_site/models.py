from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.TextField(max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.url})

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]


class Post(models.Model):
    title = models.TextField("title", max_length=150)
    category = models.ManyToManyField(Category, related_name="posts")
    main_photo = models.ImageField("main photo", upload_to="photos/", blank=True)
    publication_date = models.DateField("date of publication", max_length=20)
    intro_text = models.TextField("intro", max_length=2000)
    main_text = models.TextField("main text", max_length=10000, blank=True)
    is_published = models.BooleanField("published", default=True)
    slug = models.SlugField(max_length=130, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-publication_date"]


class Comment(models.Model):
    email = models.EmailField()
    name = models.TextField("user name", max_length=100)
    text = models.TextField("comment", max_length=2000)
    parent = models.ForeignKey("self", verbose_name="komentarz nadrzędny", on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return '%s / %s' % (self.post, self.name)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"


class Like(models.Model):
    ip = models.CharField("IP address", max_length=15)
    like = models.BooleanField("like", default=False)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}, {self.ip}'

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
