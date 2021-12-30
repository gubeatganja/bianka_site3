from django.contrib import admin
from django.utils.safestring import mark_safe
from bianka_site.models import Post, Category, Comment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}

#
# class PostAdminForm(forms.ModelForm):
#     intro_text = forms.CharField(widget=CKEditorUploadingWidget())
#     main_text = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Post
#         fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    list_display = ('publication_date', 'id', 'title', 'is_published')
    list_display_links = ('publication_date', 'id', 'title')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('publication_date', 'is_published')
    prepopulated_fields = {"slug": ("publication_date", "title")}
    # form = PostAdminForm
    readonly_fields = ('get_image',)
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

admin.site.site_title = 'Bianka'
admin.site.site_header = 'Bianka'
