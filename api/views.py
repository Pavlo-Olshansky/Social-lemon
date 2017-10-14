from django.shortcuts import render

from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


def user_list(request):
    permission_classes = (IsAuthenticated,)
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)

# class UserList(APIView):
# 	def get(self, request, format=None):
# 		users = User.objects.all()
# 		serializer = UserSerializer(users, many=True)
# 		return Response(serializer.data)


class UserList(generics.ListAPIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    """This class handles the http GET requests."""
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

def api_docs(request):
    current_site = get_current_site(request)
    context = {'domain': current_site}

    return render(request, 'api/api_docs.html', context)
