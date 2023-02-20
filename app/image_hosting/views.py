# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import UploadedFile, User
from .serializers import UploadedFileSerializer, UserSerializer, validate_image_format


class ImageAPIView(APIView):
    name = "image_list_create_view"
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)


    def get(self, request,  format=None):
        """
        Method that lists all uploaded files for the authenticated user
        """
        model_object = UploadedFile.objects.filter(created_by__id=request.user.id)
        serializer = UploadedFileSerializer(model_object, context={"request": request}, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Method that creates a new uploaded file with the given data
        :param request: new file located at request.data
        """
        new_file = request.data.get('new_file')

        # validating the file format
        try:
            file_format = validate_image_format(new_file.content_type)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        new_data = {
            "name": new_file.name,
            "file_format": file_format,
            "file_size": new_file.size,
            "image_url": new_file
        }

        serializer = UploadedFileSerializer(data=new_data, context={"request": request})

        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


image_list_create_view = ImageAPIView.as_view()


class ImageDetailAPIView(APIView):
    name = "image_retrieve_update_delete_view"
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve the Uploaded image with given id (pk) for authenticated user.
        """
        image_instance = get_object_or_404(UploadedFile, pk=pk, created_by__id=request.user.id)

        serializer = UploadedFileSerializer(image_instance, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """
        Updates the Upload Image object with given id (pk) if exists for authenticated user.
        """
        image_instance = get_object_or_404(UploadedFile, pk=pk, created_by__id=request.user.id)

        updated_file = request.data.get('new_file')
        try:
            file_format = validate_image_format(updated_file.content_type)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        updated_data = {
            "name": updated_file.name,
            "file_format": file_format,
            "file_size": updated_file.size,
            "image_url": updated_file
        }

        serializer = UploadedFileSerializer(instance=image_instance, data=updated_data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deletes the Uploaded image object with given id (pk) if exists for authenticated user
        """
        image_instance = get_object_or_404(UploadedFile, pk=pk, created_by__id=request.user.id)

        image_instance.delete()
        return Response({"result": "Image deleted"}, status=status.HTTP_200_OK)


image_retrieve_update_delete_view = ImageDetailAPIView.as_view()


class UserList(generics.ListAPIView):
    """
    Generic View for listing the Users.
    Only accessible by admin users currently.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


user_list_view = UserList.as_view()


class UserDetail(generics.RetrieveAPIView):
    """
    Generic View for retrieving the selected User object.
    Only accessible by admin users currently.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


user_retrieve_view = UserDetail.as_view()
