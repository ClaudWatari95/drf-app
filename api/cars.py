from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CarSerializer_Add, CarSerializer_View_Self, CarSerializer_View, UserSerializer_Authed
from base.models import Car

@api_view(['POST'])
def add_car(request):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    user_id = user.data.get('id')
    serialized = CarSerializer_Add(data=request.data)
    is_valid = serialized.is_valid()
    errors = serialized.errors
    try:
        if is_valid:
            model = request.data.get('model')
            registration_number = request.data.get('registration_number')
            hire_or_sale = request.data.get('hire_or_sale')
            description = request.data.get('description')
            hire = False
            sale = False
            if model is None or registration_number is None or hire_or_sale is None:
                res = {
                    "model": "this field is required",
                    "registration_number": "this field is required",
                    "hire_or_sale": "this field is required"
                }
                return Response(res, status=status.HTTP_409_CONFLICT)
            if not hire_or_sale == 'sale' and not hire_or_sale == 'hire':
                res = {
                    "hire_or_sale": "can be either 'hire' or 'sale'"
                }
                return Response(res, status=status.HTTP_409_CONFLICT)
            count_of_model = Car.objects.filter(model=model).count()
            if hire_or_sale == 'sale':
                sale = True
                hire = False
            else:
                sale = False
                hire = True
            if not description and description == '':
                description = 'No description available for this car'
            car = Car.objects.create(
                model=model, registration_number=registration_number, hire=hire, sale=sale,
                description=description, user_id=user_id, available=True
                )
            res = {
                "message": "added successfully",
                "id": car.pk
            }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "message": "something went wrong....",
                "error": errors
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_cars(request):
    authenticated = TokenAuthentication().authenticate(request=request)
    logged_in = authenticated[0]
    user = UserSerializer_Authed(logged_in)
    user_id = user.data.get('id')
    user_cars = Car.objects.filter(user_id=user_id).order_by('-id')
    cars = CarSerializer_View_Self(user_cars, many=True)
    res = {
        "data": cars.data
    }
    return Response(res, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_car_by_id(request, car_id):
    try:
        res = {
            "message": "invalid car id"
        }
        car_result: Car
        if car_id.isdigit():
            if not Car.objects.filter(id=car_id):
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                car_result = Car.objects.filter(id=car_id).get()
        else:
            if not Car.objects.filter(registration_number=car_id):
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                car_result = Car.objects.filter(registration_number=car_id).get()
        car = CarSerializer_View(car_result)
        res = {
            "data": car.data
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_by_model(request):
    model_name = request.data.get('model_name')
    if model_name is None or model_name == '':
        res = {
            "message": "search query can not be empty"
        }
        return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        car_result = Car.objects.filter(model__icontains=model_name).order_by('-id')
        cars = CarSerializer_View(car_result, many=True)
        res = {
            "data": cars.data
        }
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        res = {
            "message": "an error occured",
            "error": str(e)
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)