from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from . import serializers
import datetime
import jwt
from api.models import User, BusinessCard, Hotspot

def welcome(request):
    return HttpResponse("<h1>Welcome's Page!</h1>")


class RegisterView(APIView):
    def post(self, request) -> Response:
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request) -> Response:
        serializer = serializers.LoginSerializer(
            data=self.request.data,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        payload = {
			"id": user.id,
			"exp": datetime.datetime.utcnow() + datetime.timedelta(days=60),
			"iat": datetime.datetime.utcnow()
		}
        
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
			"jwt": token
		}
        
        return response


class GetUser(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        if not request.data.get("id"):
            request.data.update({"id": payload['id']})
        
        user = User.objects.filter(id=request.data["id"]).first()
        if not user:
            return Response({})
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class GetCardByID(APIView):

    def get(self, request):
        
        if not request.data.get("id"):
            return Response({"id": "required"})
        
        card = BusinessCard.objects.filter(id=request.data["id"]).first()
        if not card:
            return Response({"error": "no card???"})

        serializer = serializers.BusinessCardSerializer(card)
        serializer.data._mutable = True
        serializer.data.update({"first_name": card.first_name})
        return Response(serializer.data)


class CreateCard(APIView):

    def post(self, request):
        if not request.data.get("owner_id"):
            return Response({"owner_id": "No user id"})
        serializer = serializers.BusinessCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetUserCards(APIView):

    def get(self, request):
        if not request.data.get("id"):
            return Response({"id": "required"})

        bcs = BusinessCard.objects.filter(owner_id=request.data["id"])
        serializer = serializers.BusinessCardSerializer(bcs, many=True)
        return Response(serializer.data)


class ConnectToHotspot(APIView):

    def post(self, request):

        if not request.data.get("ip"):
            return Response({"ip": "required"})

        if not request.data.get("user_id"):
            return Response({"user_id": "required"})

        hot = Hotspot.objects.filter(ip=request.data["ip"]).first()
        if not hot:
            hot = Hotspot()
            hot.ip = request.data['ip']
            hot.peoples = hot.add_to_people(request.data['user_id'])
            hot.save()
            return Response({"status": "created new hot"})
        
        print(request.data['user_id'], hot.check_user_in_hotspot(int(request.data['user_id'])))
        if not hot.check_user_in_hotspot(int(request.data['user_id'])):
            hot.peoples = hot.add_to_people(request.data['user_id'])
            hot.save()
            return Response({"status": "added to hotspot"})
        else:
            return Response({"status": "you're already in hotspot"})
        