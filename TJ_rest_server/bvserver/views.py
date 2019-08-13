from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render

PAGESIZE = 10

class pdListAPI(APIView):
    def get(self,request,format = None):
        pdList = models.Products.objects.all().order_by('-updated_at')
        searchWord = request.GET.get('name')
        if searchWord:
            pdList = pdList.filter(name__icontains=searchWord)
            paginator = PageNumberPagination()
            paginator.page_size = PAGESIZE
            print(searchWord)
            result_page = paginator.paginate_queryset(pdList, request)
            serializer = serializers.productSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            print("no search word")
            return Response(data=[],status=status.HTTP_400_BAD_REQUEST)



class productSPecAPI(ListAPIView):
    def get(self,request,format = None):
        searchWord = request.GET.get('title')
        #이름으로 필터하는 부분 구현할것
        if searchWord:
            try:
                print(searchWord)
                pdImage = models.ProductImages.objects.all().filter(title=searchWord)

            except:
                print("No Such Product")
                return Response(data=[], status=status.HTTP_400_BAD_REQUEST)

            pdMat = models.ProductMaterial.objects.all().filter(product_id=1)
            Img_serializer = serializers.productSpecSerializer(pdImage, many=True)
            Mat_serializer = serializers.productMaterialSerializer(pdMat, many=True)


        else:
            print("wrong Access")
            return Response(data=[],status=status.HTTP_400_BAD_REQUEST)

        content = {'Img':Img_serializer.data,'Mat':Mat_serializer.data}
        return Response(data=content)

# Create your views here.
def post_list(request):
    return render(request,'bvserver/post_list.html',{})
