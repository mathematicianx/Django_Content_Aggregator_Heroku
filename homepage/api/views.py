<<<<<<< HEAD
<<<<<<< HEAD
from datetime import datetime
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from ..models import News, SimpleAd
from .serializers import NewsSerializer, SimpleAdSerializer
from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
=======
=======
from django.views import View
from django.http import HttpResponse, JsonResponse
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import News, SimpleAd
from .serializers import NewsSerializer, SimpleAdSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
>>>>>>> 59119d1 (Create news from existing JSON data functionality added)
=======
from rest_framework.permissions import IsAuthenticated
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


<<<<<<< HEAD

class DetailedView(APIView):

    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

class CreateNewsView(APIView):
    permission_classes = (IsAuthenticated,)
=======
class DetailedView(APIView):

    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

class CreateNewsView(APIView):
<<<<<<< HEAD

>>>>>>> 59119d1 (Create news from existing JSON data functionality added)
=======
    permission_classes = (IsAuthenticated,)
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
        return Response(serializer.data)

class UpdateNewsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class DeleteNewsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

    def delete(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        queryset.delete()
        return Response('Succesfully deleted news!')
#
#
#
class AdListView(View):

    def get(self, request):
        simple_ads = SimpleAd.objects.all()
        serializer = SimpleAdSerializer(simple_ads, many=True)
        return JsonResponse(serializer.data, safe=False)


class SimpleAdDetailedView(View):

    def get(self, request, pk):
        queryset = get_object_or_404(SimpleAd, pk=pk)
        serializer = SimpleAdSerializer(queryset)
        return JsonResponse(serializer.data, safe=False)

class CreateSimpleAdView(APIView):
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated,)
<<<<<<< HEAD

    def post(self, request):
        serializer = SimpleAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.data)

    # def perform_create(self, request serializer):
    #     serializer = SimpleAdSerializer(data=request.data)
    #     serializer.save(author=self.request.user)
=======
        return Response(serializer.data)
>>>>>>> 59119d1 (Create news from existing JSON data functionality added)
=======
    def post(self, request):
        user = request.user
        serializer = SimpleAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
>>>>>>> bda6e54 (basic functionality of rest api for Simple Advertisements, without using generics)
