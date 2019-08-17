from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
import json
PAGESIZE = 10

class productListAPI(APIView):
    def get(self,request,format = None):
        searchWord = request.GET.get('name')
        if searchWord:
            try:
                pdImage = models.ProductImages.objects.filter(title__icontains=searchWord).order_by('-updated_at')#.filter(name__icontains=searchWord).order_by('-updated_at')
            except:
                print("Error Occured During Pulling DB")
                return Response(data=[],status=status.HTTP_400_BAD_REQUEST)
            if pdImage.count() == 0:
                print('No Matched Product')
                return Response(data=[],status=status.HTTP_404_NOT_FOUND)
            paginator = PageNumberPagination()
            paginator.page_size = PAGESIZE

            result_page = paginator.paginate_queryset(pdImage, request)
            productImageserializer = serializers.productImageSerializer(result_page,many=True)
            #content = {'img':productImageserializer.data,'product':}
            return paginator.get_paginated_response(productImageserializer.data)
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
                pdImage = models.ProductImages.objects.filter(title=searchWord)
                for a in pdImage:
                    pdnum = a.product
                    break
                    #상세 페이지에 들어갈 제품의 products의 id를 가져온다.
            except:
                print("No Such Product")
                return Response(data=[], status=status.HTTP_400_BAD_REQUEST)
            pdMat = models.ProductMaterial.objects.filter(product_id=pdnum)
            jsonMat = {}
            for mat in pdMat:
                jsonMat[mat.material.name] = mat.material.vcategory
            jsonMat = json.dumps(jsonMat,ensure_ascii=False)
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
