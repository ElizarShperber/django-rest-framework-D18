from django.contrib import admin

from newsportal.models import Author, Category, Post, PostCategory, Comment, Subscriber


class PostAdmin(admin.ModelAdmin):
    #
    # for field in Post._meta.get_fields():
    #     print(type(field))

    list_display = ('type_of_post', 'author', 'date_time_create', 'title', 'rating')
    list_filter = ('type_of_post', 'author')
    search_fields = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'date_time_create', 'rating')
    list_filter = ('rating', 'user')

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber)
