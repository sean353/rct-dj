from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView


# Create your views here.

from django.http import JsonResponse
from rest_framework import serializers

from .models import Product




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



def index(req):
    return JsonResponse('hello', safe=False)


@api_view(['GET'])
def getImages(request):
    res=[] #create an empty list
    for img in Product.objects.all(): #run on every row in the table...
        res.append({"desc":img.desc,
                "price":img.price,
                "completed":False,
               "image":str( img.image)
                }) #append row by to row to res list
    return Response(res) #return array as json response

# upload image method (with serialize)


class APIViews(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=ProductSerializer(data=request.data)
       
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors)
        










@api_view(['GET'])
def getproducts(req,id=-1):
    if req.method =='GET':
        if id > -1:
            try:
                temp_task=Product.objects.get(id=id)
                return Response (ProductSerializer(temp_task,many=False).data)
            except Product.DoesNotExist:
                return Response ("not found")
        all_tasks=ProductSerializer(Product.objects.all(),many=True).data
        return Response ( all_tasks)
    

    
    
@api_view(['POST'])
def addproducts(req):
    if req.method =='POST':
        tsk_serializer = ProductSerializer(data=req.data)
        if tsk_serializer.is_valid():
            tsk_serializer.save()
            return Response ("post...")
       
        




@api_view(['DELETE'])
def delproducts(req,id=-1):
    if req.method =='DELETE':
        try:
            temp_task=Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")    
       
        temp_task.delete()
        return Response ("del...")
    


@api_view(['PUT'])
def updproducts(req, id=-1):
    if req.method == 'PUT':
        try:
            # Get the existing product object
            existing_product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response("Product not found")

        # Serialize the updated data
        serializer = ProductSerializer(existing_product, data=req.data)

        if serializer.is_valid():
            # Update the existing product object with the validated data
            serializer.save()
            return Response("Product updated successfully")
        



