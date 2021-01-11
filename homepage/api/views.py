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
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import News
from .serializers import NewsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
>>>>>>> 59119d1 (Create news from existing JSON data functionality added)

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
#
# class NewsDetailView(generics.RetrieveAPIView):
#     queryset = News.objects.get()
#     serializer_class = NewsSerializer

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

>>>>>>> 59119d1 (Create news from existing JSON data functionality added)
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
<<<<<<< HEAD
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
