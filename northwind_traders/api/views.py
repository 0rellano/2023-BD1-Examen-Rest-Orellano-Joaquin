from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from api.models import Customers, Categories, Employees, Suppliers, Shippers, Orders, Orderdetails, Products
from api.serializers import CustomersSerializer, CategoriesSerializer, EmployeesSerializer, SuppliersSerializer, ShippersSerializer, OrdersSerializer, OrderdetailsSerializer, ProductsSerializer
def index(request):
    return HttpResponse("Hello, world. You're at dea hablaba en ingles el loco")


class BaseView(APIView):
    model = None
    serializer = None

    def get(self, request):
        queryset = self.model.objects.all()
        serializer = self.serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseIdView(APIView):
    model = None
    serializer = None
    field_pk = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(**{self.field_pk: pk})
        except self.model.DoesNotExist:
            raise Http404("Object does not exist.")
        
    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance)
        instance.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)


class customers(BaseView):
    model = Customers
    serializer = CustomersSerializer

class customers_id(BaseIdView):
    model = Customers
    serializer = CustomersSerializer
    field_pk = 'customerid'


class categories(BaseView):
    model = Categories
    serializer = CategoriesSerializer

class categories_id(BaseIdView):
    model = Categories
    serializer = CategoriesSerializer
    field_pk = 'categoryid'

class employyes(BaseView):
    model = Employees
    serializer = EmployeesSerializer

class employyes_id(BaseIdView):
    model = Employees
    serializer = EmployeesSerializer
    field_pk = 'employeeid'

class products(BaseView):
    model = Products
    serializer = ProductsSerializer

class products_id(BaseIdView):
    model = Products
    serializer = ProductsSerializer
    field_pk = 'productid'

class suppliers(BaseView):
    model = Suppliers
    serializer = SuppliersSerializer

class suppliers_id(BaseIdView):
    model = Suppliers
    serializer = SuppliersSerializer
    field_pk = 'supplierid'

class shippers(BaseView):
    model = Shippers
    serializer = ShippersSerializer

class shippers_id(BaseIdView):
    model = Shippers
    serializer = ShippersSerializer
    field_pk = 'shipperid'

class orders(BaseView):
    model = Orders
    serializer = OrdersSerializer

class orders_id(BaseIdView):
    model = Orders
    serializer = OrdersSerializer
    field_pk = 'orderid'

class orderdetails(BaseView):
    model = Orderdetails
    serializer = OrderdetailsSerializer

# esta funcion esta hecha asi porque mis vistas base no estan hechas para modelos con multiples pk
def orderdetail_id(request, orderid, productid):
    try:
        orderDetail = Orderdetails.objects.get(orderid=orderid, productid=productid)
    except Orderdetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderdetailsSerializer(orderDetail)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderdetailsSerializer(orderDetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        orderDetail.delete()
        return Response(status=status.HTTP_200_OK)
      
@api_view(['GET'])
def requestparamas(request):
	orders = Orders.objects.all()
	if request.GET.get('fechaMayor') and request.GET.get('fechaMenor'):
		orders = Orders.objects.filter(orderdate__range=(request.GET.get('fechaMenor'), request.GET.get('fechaMayor')))
	else:
		if request.GET.get('fechaMayor'):
			orders = orders.filter(orderdate__gt=request.GET.get('fechaMayor'))
		if request.GET.get('fechaMenor'):
			orders = orders.filter(orderdate__gt=request.GET.get('fechaMenor'))
	serializer = OrdersSerializer(orders, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def filtos(request):
	customers = Customers.objects.all()
	if request.GET.get('comienza'):
		customers.filter(contactname__startswith=request.GET.get('comienza'))
	if request.GET.get('termina'):
		customers.filter(contactname__endswith=request.GET.get('termina'))
	if request.GET.get('contiene'):
		customers.filter(contactname__contains=request.GET.get('contiene'))
	serializer = CustomersSerializer(customers, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def prueba_endpoint1(request):
     if request.method == 'GET':
        resultados = []
        idcategoria = int(request.GET.get('categoryid'))
        ventasmin = int(request.GET.get('ventasmin'))
        try:
             categoria = Categories.objects.get(categoryid=idcategoria)
        except Categories.DoesNotExist:
             return Response(status=status.HTTP_404_NOT_FOUND)
        
        for empleado in Employees.objects.all():
             totalempleado = empleado.calcular_total_ordenes()
             ordenes = empleado.get_ordenes()
             for orden in ordenes:
                detalles = orden.get_detalles()
                for detalle in detalles:
                     product = detalle.productid
                     if product.categoryid == categoria and totalempleado>ventasmin:
                          if not empleado in resultados:
                            resultados.append(empleado)
        if len(resultados) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serialize = EmployeesSerializer(resultados, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def prueba_endpoint2(request):
    fecha_inicio = int(request.GET.get('fechainicio'))
    id_categoria = int(request.GET.get('categoryid'))
    ventas_requeridas = int(request.GET.get('ventasrequeridas'))
    aumento = request.data['aumento']
    id_shipper = request.data['shipperid']

    try:
        categoria = Categories.objects.get(categoryid=id_categoria)
    except Categories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        

    productos = []

    # productos y punto f
    ordenes = Orders.objects.filter(orderdate__gt=fecha_inicio)
    for orden in ordenes:
        detalles = orden.get_detalles()
        for detalle in detalles:
            producto = detalle.productid
            if producto.categories_id == categoria:
                 productos.append(producto)

    # punto g y h
    for producto in productos:
        producto.unitprice = producto.unitprice + (producto.unitprice * aumento)

        ventas = int()
        detalle_ordenes  = Orderdetails.objects.filter(producto.productid)
        for detalle in detalle_ordenes:
            ventas += detalle.quantity
        if ventas >= ventas_requeridas*2:
            producto.unitprice = producto.unitprice + (producto.unitprice * aumento*2)
        else:
            producto.unitprice = producto.unitprice + (producto.unitprice * aumento)
            producto.discontinued = True
        producto.save()
    
    if len(producto) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = ProductsSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

     
          

