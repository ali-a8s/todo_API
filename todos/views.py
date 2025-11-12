from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializer import TodoSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle



class TodosListView(APIView):
    '''
        Display list of todos
    '''
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get(self, request):
        todos = Todo.objects.all()
        ser_data = TodoSerializer(instance= todos, many=True)
        return Response(ser_data.data, status= status.HTTP_200_OK)
    

class TodoDetailView(APIView):
    '''
        Display a todo
    '''
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        ser_data = TodoSerializer(instance= todo)
        return Response(ser_data.data, status= status.HTTP_200_OK)
    

class TodoCreateView(APIView):
    '''
        Create new todo
    '''
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        ser_data = TodoSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user)  # ← Key change: set user here
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TodoUpdateView(APIView):
    '''
        Update a todo
    '''
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def put(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        self.check_object_permissions(request, todo)
        ser_data = TodoSerializer(instance=todo, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status= status.HTTP_200_OK)
        return Response(ser_data.errors, status= status.HTTP_400_BAD_REQUEST)


class TodoDeleteView(APIView):
    '''
        Delete a todo
    '''
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return Response({'message': 'todo deleted successfully'}, status= status.HTTP_200_OK)
    

