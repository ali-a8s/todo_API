from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializer import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User



class UserRegisterView(APIView):
    '''
        User Registration
    '''
    def post(self, request):
        ser_data = UserRegistrationSerializer(data= request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status= status.HTTP_201_CREATED)
        return Response(ser_data.errors, status= status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    '''
        User Login
    '''
    def post(self, request):
        ser_data = UserLoginSerializer(data= request.data)
        if ser_data.is_valid():
            user = ser_data.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogouView(APIView):
    '''
        User Logout
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"logout": "success"}, status=status.HTTP_200_OK)
    

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()

    def list(self, request): # GET
        '''
            Display list of users 
        '''
        ser_data = UserSerializer(instance=self.queryset, many=True)
        return Response(ser_data.data, status= status.HTTP_200_OK)

    def retrieve(self, request, pk=None): # GET
        '''
            Display specific user
        '''
        user = get_object_or_404(self.queryset, pk=pk)
        ser_data = UserSerializer(instance= user)
        return Response(ser_data.data, status= status.HTTP_200_OK)

    def partial_update(self, request, pk=None): # PATCH
        '''
            Update user info by account owner
        '''
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        ser_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status= status.HTTP_200_OK)    
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None): # DELETE
        '''
            Deactivate account
        '''
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        user.is_active = False
        user.save()
        return Response({'message': 'user deactivated'})