from django.shortcuts import get_object_or_404
from rest_framework import generics
from ..models import News
from .serializers import NewsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
#
# class NewsDetailView(generics.RetrieveAPIView):
#     queryset = News.objects.get()
#     serializer_class = NewsSerializer

class DetailedView(APIView):

    def get(self, request, pk):
        queryset = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(queryset)
        return Response(serializer.data)

class CreateNewsView(APIView):

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)