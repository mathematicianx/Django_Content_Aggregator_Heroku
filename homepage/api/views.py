from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import News, SimpleAd
from .serializers import NewsSerializer, SimpleAdSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class DetailedView(APIView):

    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

class CreateNewsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        user = request.user
        serializer = SimpleAdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)