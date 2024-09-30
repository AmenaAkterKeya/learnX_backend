from rest_framework import serializers
from .models import Department, Course,Review,Comment,Balance,Enroll
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    # instructor = serializers.StringRelatedField(many=False)
    # department = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'created_on']
    def create(self, validated_data):
        request = self.context.get('request')
        instructor = request.user.instructor  
        validated_data['instructor'] = instructor
        return super().create(validated_data)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
        read_only_fields = ['student', 'created_on']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['student'] = request.user.student
        return super().create(validated_data)

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enroll
        fields = '__all__'
        read_only_fields = ['student', 'created_on']
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['student'] = request.user.student
        return super().create(validated_data)
  


