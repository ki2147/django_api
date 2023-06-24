import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from productapp.models import Product
from productapp.serializers import ProductSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_product():
    def _create_product(name, brand, description, price):
        return Product.objects.create(name=name, brand=brand, description=description, price=price)
    return _create_product


@pytest.mark.django_db
def test_get_all_products(api_client, create_product):
    # Create some sample products
    product1 = create_product(name="Product 1", brand="Brand 1", description="Description 1", price=10.99)
    product2 = create_product(name="Product 2", brand="Brand 2", description="Description 2", price=20.99)

    url = reverse('productapp:product-view')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    expected_data = ProductSerializer([product1, product2], many=True).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_get_single_product(api_client, create_product):
    product = create_product(name="Product 1", brand="Brand 1", description="Description 1", price=10.99)

    url = reverse('productapp:product-detail-view', kwargs={'pk': product.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = ProductSerializer(product).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_get_single_product_nonexistent(api_client, create_product):
    non_existent_pk = 999
    url = reverse('productapp:product-detail-view', kwargs={'pk': non_existent_pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_product(api_client):
    url = reverse('productapp:product-view')
    data = {
        'name': 'New Product',
        'brand': 'Brand New',
        'description': 'New Product Description',
        'price': 9.99
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    product = Product.objects.get(pk=response.data['id'])
    expected_data = ProductSerializer(product).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_update_product(api_client, create_product):
    product = create_product(name="Product 1", brand="Brand 1", description="Description 1", price=10.99)
    url = reverse('productapp:product-detail-view', kwargs={'pk': product.pk})

    data = {
        'name': 'Updated Product',
        'brand': 'Updated Brand',
        'description': 'Updated Description',
        'price': 19.99
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK

    updated_product = Product.objects.get(pk=product.pk)
    expected_data = ProductSerializer(updated_product).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_delete_product(api_client, create_product):
    product = create_product(name="Product 1", brand="Brand 1", description="Description 1", price=10.99)
    url = reverse('productapp:product-detail-view', kwargs={'pk': product.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Product.objects.filter(pk=product.pk).exists()
