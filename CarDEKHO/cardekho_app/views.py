from django.shortcuts import render
from .models import Carlist
from django.http import JsonResponse
from .api_file.serializers import CarSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
        cars = Carlist.objects.all()
        serializer = CarSerializer(cars , many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET', 'PUT'])
def car_detail_view(request, pk):
    
    if request.method == 'GET':
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        car = Carlist.objects.get(pk=pk)
        serializer = CarSerializer(car,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    if request.method == 'DELETE':
        try:
            car = Carlist.objects.get(pk=pk)
            car.delete()
            return Response({'status': 'Car deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        except Carlist.DoesNotExist:
            return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)
        

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_serializer.data
                })
        else:
            return Response({'detail': 'Invalid credentials'}, status=401)
        

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user =  request.user
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'welcome to dashboard',
            'user' : user_serializer.data
        },200)
    

class UserDetailView(generics.RetrieveAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'id'

    def get_object(self):
        id = self.kwargs.get('id')
        return User.objects.get(id=id)
    

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' 

    def delete(self, request, *args, **kwargs):
        
        user = self.get_object()
        if user != request.user:
            return Response({'detail': 'You do not have permission to delete this user.'}, status=status.HTTP_403_FORBIDDEN)

        return self.destroy(request, *args, **kwargs)
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


