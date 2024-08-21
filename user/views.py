from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,authentication,permissions
from .models import UserDetails
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.settings import api_settings
#from user import permissions
from user.permissions import UpdateOwnProfile



class RecruiterSignupView(APIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message='Your account has been created successfully'
            return Response({'message':message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeekerSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            message='Your account has been created successfully'
            return Response({'message':message}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key})

# class RecruiterProfileView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserDetails.objects.all()
#     serializer_class = RecruiterSerializer
#     #authentication_classes= (TokenAuthentication,)
#     permission_classes = [IsAuthenticated,permissions.UpdateOwnProfile]
#
#     def get_queryset(self):
#         return UserDetails.objects.filter(id=self.request.user.id)



class RecruiterProfileView(generics.RetrieveDestroyAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        # Ensure that the user can only access their own profile
        return UserDetails.objects.get(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        # Overriding to handle the response with authentication check
        if not request.user.is_authenticated:
            print('FROM Recruiter Profile view')
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)

class SeekerProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDetails.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDetails.objects.filter(id=self.request.user.id)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "You've been logged out successfully"})

class CreateTokenView(ObtainAuthToken):
    """create new Auth Token view"""
    serializer_class=AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user"""
    queryset = UserDetails.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        # For example, filter based on the current authenticated user

        user = self.request.user
        return UserDetails.objects.filter(email=self.request.user.email)
def get_object(self):
    """Retrieve and return authenticated user"""
    return self.request.user
