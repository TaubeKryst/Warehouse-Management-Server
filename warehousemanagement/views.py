from rest_framework import permissions
from rest_framework import generics, mixins
from rest_framework.decorators import authentication_classes, permission_classes
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsManagerOrEmployee

import logging


class ProductListView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrEmployee]

    def get_queryset(self):
        all_products = Product.objects.all()
        manufacturer_name = self.request.GET.get("manufacturer_name")

        if manufacturer_name is not None:
            selected_products = all_products.filter(
                Q(manufacturer_name__icontains=manufacturer_name)
            ).distinct()
            return selected_products

        return all_products

    def perform_create(self, serializer):
        serializer.save(quantity=0)

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("info")
        logger.info(f"Post on: {request.path}; Manufacturer: {request.data['manufacturer_name']}; "
                    f"Model: {request.data['model_name']}; Price: {request.data['price']};")
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ProductRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrEmployee]

    def get_queryset(self):
        return Product.objects.all()

    def get_selected_object(self, product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return "no product"

    def post(self, request, pk):
        logger = logging.getLogger("info")
        logger.info(f"Post on: {request.path}; Mode: {request.data['op']}; Value: "
                    f"{request.data['quantity']}")

        product_object = self.get_selected_object(pk)
        if product_object == "no product":
            logger.info(f"The product id={pk} does not exist")
            return JsonResponse(status=404, data="The product does not exist", safe=False)

        serializer = ProductSerializer(product_object, data=request.data, partial=True)
        if 'quantity' in request.data and 'op' in request.data and serializer.is_valid():
            actual_quantity = getattr(product_object, 'quantity')

            if request.data['op'] == "inc" and int(request.data['quantity']) > 0:
                actual_quantity += int(request.data['quantity'])
                serializer.save(quantity=actual_quantity)
                return JsonResponse(status=200, data=serializer.data)
            elif request.data['op'] == "dec":
                actual_quantity -= int(request.data['quantity'])
                if actual_quantity >= 0:
                    serializer.save(quantity=actual_quantity)
                    return JsonResponse(status=200, data=serializer.data)

        logger.error("Incorrect quantity")
        return JsonResponse(status=400, data=serializer.data)

    def put(self, request, *args, **kwargs):
        logger = logging.getLogger("info")
        logger.info(f"Put on: {request.path}; Manufacturer: {request.data['manufacturer_name']}; "
                    f"Model: {request.data['model_name']}; Price: {request.data['price']};")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logger = logging.getLogger("info")
        logger.info(f"Delete on: {request.path};")
        return self.destroy(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


@authentication_classes([])
@permission_classes([])
class RegisterUserView(generics.CreateAPIView):

    serializer_class = []

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        email = request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']

        if len(username) == 0 or len(email) == 0:
            return JsonResponse(status=204, data="All fields must be completed", safe=False)
        if len(password1) < 6:
            return JsonResponse(status=204, data="Password must be > 5 characters", safe=False)
        if password1 != password2:
            return JsonResponse(status=204, data="Passwords are not equal", safe=False)

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        return JsonResponse(status=201, data="New user added", safe=False)
