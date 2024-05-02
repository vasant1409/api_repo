from django.http import JsonResponse
from .models import Movies
from .serializers import MoviesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(['GET','POST'])
def movies_list(request):
 #   if(validateApiKey(request) = True): 
  #      return ("Message")
 #   else:
 #       Response("Status_Code":status=status.HTTP_400_BAD_REQUEST)
    if request.method =='GET':
        movies=Movies.objects.all()
        serializer=MoviesSerializer(movies,many=True)
        if (validateApiKey(request) is True):
            return JsonResponse({"Staus_Code":"200 OK","Message":serializer.data},safe=False,status=status.HTTP_200_OK)
        else: 
            return Response({"Status": "400 Bad request","Message":"Invalid API Key"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer=MoviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if (validateApiKey(request) is True):
                return Response({"Status_Code":"200 OK","Message":serializer.data},status=status.HTTP_201_CREATED)
            else: 
                return Response({"Status": "400 Bad request","Message":"Invalid API Key"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def movies_detail(request,id):
 #   if(validateApiKey(request) != True): 
 #       return Response(status=status.HTTP_400_BAD_REQUEST)
    
    try:
        movie=Movies.objects.get(pk=id)
    except Movies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=MoviesSerializer(movie)
        if (validateApiKey(request) is True):
            return JsonResponse({"Staus_Code":"200 OK","Message":serializer.data},safe=False,status=status.HTTP_200_OK)
        else: 
            return Response({"Status": "400 Bad request","Message":"Invalid API Key"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method=='PUT':
            
        if (validateApiKey(request) is True):
            serializer=MoviesSerializer(movie,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Staus_Code":"200 OK","Message":serializer.data},safe=False,status=status.HTTP_200_OK)
            else: 

                return Response({"Status": "400 Bad request","Message":"Invalid API Key"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method=='DELETE':
        movie.delete()
        return Response({"Status_Code":"204_NO_CONTENT"},status=status.HTTP_204_NO_CONTENT)

def validateApiKey(request):
    actual_api_key = 'vas101'
    print(request.data.get('api_key'), actual_api_key)
    if request.data.get('api_key') is None:
        return False
    if (actual_api_key == request.data['api_key']):
        return True
    else:
        return False