from .models import Student,Instructor
from . import serializers
from rest_framework import viewsets,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
class StudentForStudent(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        instructor_id = request.query_params.get("user_id")
        if instructor_id:
            return queryset.filter(user_id=instructor_id)
        return queryset   
class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [StudentForStudent]
class InstructorForInstructor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        instructor_id = request.query_params.get("user_id")
        if instructor_id:
            return queryset.filter(user_id=instructor_id)
        return queryset    
class InstructorViewset(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = serializers.InstructorSerializer
    filter_backends = [InstructorForInstructor]
class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://learnx-ldys.onrender.com/account/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://amenaakterkeya.github.io/learnX_frontend/login.html')
    else:
        return redirect('https://amenaakterkeya.github.io/learnX_frontend/registration.html')
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)

                login(request, user)
                role = None
                if hasattr(user, 'student'):
                    role = 'student'
                elif hasattr(user, 'instructor'):
                    role = 'instructor'

                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'role': role  # Include the role in the response
                })
            else:
                return Response({'error' : "Password is incorrect"})
        return Response(serializer.errors)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
