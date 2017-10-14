from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken import views as auth_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins

from .serializers import UserSerializer


class UserListRetrieveViewSet(mixins.ListModelMixin, 
                              mixins.RetrieveModelMixin, 
                              viewsets.GenericViewSet):
    """
    View that provides 'list' and 'retrieve' actions 
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ObtainAuthToken(auth_view.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Authorization Token': token.key})


def api_docs(request):
    current_site = get_current_site(request)
    context = {'domain': current_site}

    return render(request, 'api/api_docs.html', context)


# class UserList(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetailsView(generics.RetrieveAPIView):
#     """This class handles the http GET requests."""
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer