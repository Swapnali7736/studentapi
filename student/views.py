from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from student.serializers import UserSerializer
from student.serializers import StudentSerializer
from rest_framework.authentication import TokenAuthentication
from student.models import Student
from student.permissions import IsSuperuserOrReadOnly


class Register(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        request.user.authtoken.delete()  
        return Response({"logout successfully"},status=status.HTTP_204_NO_CONTENT)      



class SLC(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsSuperuserOrReadOnly]

    def get(self,request):
        s=Student.objects.all()
        serializer=StudentSerializer(s,many=True)  
        return Response(serializer.data,status=status.HTTP_200_OK)  

    def post(self,request):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_superuser=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SRUD(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsSuperuserOrReadOnly]

    def get(self,request,i):
        s=get_object_or_404(Student,id=i)
        serializer=StudentSerializer(s)
        return Response(serializer.data,status=status.HTTP_200_OK)     

    def put(self,request,i):
        s=get_object_or_404(Student,id=i)
        self.check_object_permissions(request,s)
        serializer=StudentSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,i):
        s=get_object_or_404(Student,id=i)
        self.check_object_permissions(request,s)
        s.delete()
        return Response({"deleted successfully"},status=status.HTTP_204_NO_CONTENT) 
        
           