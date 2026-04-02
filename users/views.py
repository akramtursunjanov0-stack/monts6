from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegistrationSerializers
from .models import ConfirmationCode
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response(status=status.HTTP_200_OK)

        if not user.is_active:
            return Response(data={'erros': "Пользователь не зареган!"}, status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializers = RegistrationSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)

        username = request.data.get("username")
        password = request.data.get("password")

        user = CustomUser.objects.create_user(username=username, password=password, is_active=False)
        code = ConfirmationCode.generate_code()
        ConfirmationCode.objects.create(user=user, code=code)

        print(f"Код подтверждения для {username}: {code}")
        if user is not None:
            return Response(data={"user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    


class ConfrimationAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        if not username or not code:
            return Response(data={"errors": "Необходимо указать юзернейм или код"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(username=username)

            if user.is_active:
                return Response(data={'errors': 'Уже активировали код для этого пользователя!'})
            confirm = ConfirmationCode.objects.get(user=user, code=code)
            
            user.is_active = True
            user.save()

            confirm.delete()

            return Response(
                {"message": "Пользователь успешно активирован"},
                status=status.HTTP_200_OK
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except ConfirmationCode.DoesNotExist:
            return Response(
                {"errors": "Неверный код подтверждения"},
                status=status.HTTP_400_BAD_REQUEST
            )