from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,  IsAdminUser, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from .pagination import CustomPagination
from django.db.models.aggregates import Count
from .permissions import ViewCustomerHistoryPermission,IsVendorOrAdmin,IsAdminOrReadOnly
from .models import *
from .serializers import *
# Create your views here.

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.user.is_authenticated:  
            try:
                customer = Customer.objects.get(user_id=request.user.id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer does not exist"}, status=404)

            if request.method == 'GET':
                serializer = CustomerSerializer(customer)
                return Response(serializer.data)
            elif request.method == 'PUT':
                serializer = CustomerSerializer(customer, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        else:
            return Response({"error": "User not authenticated"}, status=401)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes=[IsAdminUser]    
    
    def destroy(self,request,*args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error':'Collection have products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
 
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_id=user.id)
    
    def get_serializer_context(self):
        user = self.request.user.id
        return {'user_id': user}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateSerializer
        return OrderSerializer
               
        
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    search_fields = ['title', 'description']    
    filter_backends = [SearchFilter]

    
    def destroy(self, request, *args, **kwargs):
        if Order.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)