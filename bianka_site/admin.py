from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Category, Comment, Like
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin


class PostAdminForm(forms.ModelForm):
    main_text_pl = forms.CharField(widget=CKEditorUploadingWidget())
    main_text_ru = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(TranslationAdmin):
    prepopulated_fields = {"url": ("name",)}


class PostAdmin(TranslationAdmin):
    list_display = ('publication_date', 'id', 'title', 'is_published')
    list_display_links = ('publication_date', 'id', 'title')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('publication_date', 'is_published')
    prepopulated_fields = {"slug": ("publication_date", "title")}
    readonly_fields = ('get_image',)
    form = PostAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "category",),)
        }),
        (None, {
            "fields": ("publication_date",)
        }),
        (None, {
            "fields": (("main_photo", "get_image",),)
        }),
        (None, {
            "fields": ("intro_text", ("main_text",))
        }),
        (None, {
            "fields": ("slug",)
        }),
        (None, {
            "fields": ("is_published",)
        }),
    )

    def get_image(self, post):
        return mark_safe(f'<img src={post.main_photo.url} height=100')

    get_image.short_description = 'preview'


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Like)

admin.site.site_title = 'Bianka'
admin.site.site_header = 'Bianka'
