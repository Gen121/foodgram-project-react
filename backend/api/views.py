from rest_framework import mixins

from users.models import User
from api.serializers import UserSerializer


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet, ):
    lookup_field = 'id'
    # # permission_classes = (AdminOrReadOnnly, )
    # # filter_backends = (filters.SearchFilter, )
    # search_fields = ('name', )


class UserViewSet(CreateListDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
