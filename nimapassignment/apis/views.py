from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import ClientSerializer, ProjectSerializer, ClientDetailSerializer
from .models import Client, Project
from rest_framework import generics, status
from rest_framework.response import Response


class ClientList(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientCreate(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientReadUpdateDelete(APIView):
    serializer_class = ClientSerializer

    def get_client_by_id(self, pk):
        try:
            return Client.objects.get(pk=pk)

        except:
            return Response({
                "error": "Client doesn't exist"
            }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        clients = self.get_client_by_id(pk)
        serializer = ClientSerializer(clients)
        return Response(serializer.data)

    def put(self, request, pk):
        clients = self.get_client_by_id(pk)
        serializer = ClientSerializer(clients, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        clients = self.get_client_by_id(pk)
        clients.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCreate(APIView):

    def post(self, request, pk):
        client = get_object_or_404(Client, id=pk)
        data = request.data.copy()
        data['client'] = client.client_name
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save(client=client, created_by=request.user)
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectList(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ClientDelete(APIView):

    def get_client_by_pk(self, pk):
        try:
            return Client.objects.get(pk=pk)

        except:
            return Response({
                "error": "Client doesn't exist"
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        clients = self.get_client_by_pk(pk)
        clients.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientReadUpdateDeleteDetail(APIView):
    serializer_class = ClientDetailSerializer

    def get_client_by_id(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_client_by_id(pk)
        serializer = self.serializer_class(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_client_by_id(pk)
        serializer = self.serializer_class(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_client_by_id(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
