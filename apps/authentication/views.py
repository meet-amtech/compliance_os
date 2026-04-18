from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers import UserSerializer
from .serializers import LoginSerializer


class LoginAPIView(APIView):
    """
    User login endpoint.
    Returns JWT tokens with tenant info embedded.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TenantLoginAPIView(APIView):
    """
    Tenant login endpoint.
    Returns JWT token with tenant context.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TenantLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MeAPIView(RetrieveUpdateAPIView):
    """
    Get or update current authenticated user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user