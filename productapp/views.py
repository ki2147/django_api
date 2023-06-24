import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.exceptions import NotFound
from .kinesis import get_kinesis_client
from decouple import config

# Create a Kinesis client
kinesis_client = get_kinesis_client()
stream_name = config('AWS_KINESIS_STREAM_NAME')


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        # Publish log message to Kinesis stream
        log_message = {
            'endpoint': 'ProductListAPIView GET',
            'message': 'Get all products'
        }
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(log_message),
            PartitionKey='get_all'
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()

            # Publish log message to Kinesis stream
            log_message = {
                'endpoint': 'ProductListAPIView POST',
                'message': 'Create a new product',
                'brand': product.brand,
                'name': product.name
            }
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(log_message),
                PartitionKey='add'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)

            # Publish log message to Kinesis stream
            log_message = {
                'endpoint': 'ProductDetailView GET',
                'message': f'Get product with ID: {pk}'
            }
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(log_message),
                PartitionKey='get_one'
            )

            return Response(serializer.data)

        except NotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Publish log message to Kinesis stream
            log_message = {
                'endpoint': 'ProductDetailView PUT',
                'message': f'Update product with ID: {pk}'
            }
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(log_message),
                PartitionKey='modify'
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)

        # Publish log message to Kinesis stream
        log_message = {
            'endpoint': 'ProductDetailView DELETE',
            'message': f'Delete product with ID: {pk}'
        }
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(log_message),
            PartitionKey='delete'
        )

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
