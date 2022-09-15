from rest_framework import serializers

from newsportal.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'rating', 'title', 'body','type_of_post' ]
