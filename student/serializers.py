
from rest_framework import serializers
from student.models import Student
from django.contrib.auth.models import User
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"



 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","email","first_name","last_name"]


    def create(self,validated_data):
        u=User.objects.create_user(**validated_data)
        u.save()
        return u

