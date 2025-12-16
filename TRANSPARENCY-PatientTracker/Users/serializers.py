from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()

# Serializer for Department model

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    # Show the department name in the user representation

    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'department', 'department_name', 'phone', 'email', 'password']

        # Hide password when reading data, but allow writing it when creating users
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Handle password hashing when creating a new user
        
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance