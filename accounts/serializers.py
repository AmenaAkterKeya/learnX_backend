from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Instructor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = '__all__'

class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Instructor
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=['student', 'instructor'], required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'role']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        role = self.validated_data['role']
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords do not match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account = User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.is_active = False
        account.save()

        if role == 'student':
            Student.objects.create(user=account)
        elif role == 'instructor':
            Instructor.objects.create(user=account)
        
        return account

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    