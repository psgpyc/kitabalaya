from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from coreaccounts.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


