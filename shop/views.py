from rest_framework import viewsets, filters
from .models import Category, Brand, Product, ProductImage
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductImageSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsUserReadOnly
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsUserReadOnly]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsUserReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsUserReadOnly]

    search_fields = ["name", "description"]
    filter_backends = [filters.SearchFilter]


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsUserReadOnly]
