
from operator import ge
from turtle import pos
from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
# Create your views here.


##############################   Function Based List View   #################################
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method=='GET':
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many = True)
        return Response(serializer.data)

    elif(request.method == 'POST'):
        serializer = PostSerializer(data=request.data)
        print('***********88')
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
################################################################################################

############################ Class based List view #############################################
class PostView(APIView):
    permission_classes = (AllowAny,)
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk  = pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#######################################################################################


################# generic List view #######################################
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes=(AllowAny,)

#_---------------------------------------------------------------------------------------------#


# ######################function based Detail view ###################

@api_view(['GET', 'PUT','DELETE'])
@permission_classes([AllowAny])
def post_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#################################################################################################

##################################### Classed based Detail View #####################################

class DetailPostView(APIView):
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise HttpResponse(status=404)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer =PostSerializer(post)
        return Response(serializer.data)

################################################################################################

###### ################Generic Class Detail View ##################################################


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes=(AllowAny,)

