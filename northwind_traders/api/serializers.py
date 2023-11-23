from rest_framework import serializers
from api.models import *

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class CustomerdemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customerdemographics
        fields = '__all__'


class CustomercustomerdemoSerializer(serializers.ModelSerializer):
    customerid = CustomersSerializer(many=False)
    customertypeid = CustomerdemographicsSerializer(many=False)
    class Meta:
        model = Customercustomerdemo
        fields = '__all__'


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'
    

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class TerritoriesSerializer(serializers.ModelSerializer):
    regionid = RegionSerializer(many=False)
    class Meta:
        model = Territories
        fields = '__all__'


class EmployeeterritoriesSerializer(serializers.ModelSerializer):
    employeeid = EmployeesSerializer(many=False)
    territoryid = TerritoriesSerializer(many=False)
    class Meta:
        model = Employeeterritories
        fields = '__all__'

class ShippersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shippers
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    customerid = CustomersSerializer(many=False)
    employeeid = EmployeesSerializer(many=False)
    shipvia = ShippersSerializer(many=False)

    class Meta:
        model = Orders
        fields = '__all__'


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    supplierid = SuppliersSerializer(many=False)
    categoryid = CategoriesSerializer(many=False)
    class Meta:
        model = Products
        fields = '__all__'



class OrderdetailsSerializer(serializers.ModelSerializer):
    orderid = OrdersSerializer(many=False)
    productid = ProductsSerializer(many=False)
    class Meta:
        model = Orderdetails
        fields = '__all__'
