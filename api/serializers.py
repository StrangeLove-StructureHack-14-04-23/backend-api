from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models import User, BusinessCard


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'description', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, 
                password=password
            )
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    

class BusinessCardCreateSerializer(serializers.Serializer):
    
    class Meta:
        model = BusinessCard
        fields = [
            "user_id", "role", "phone", "own_site", "linkedin_url", "telegram_url"
        ]
    
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        card_owner = User.objects.filter(id=validated_data.get("user_id")).first()
        instance.owner = card_owner
        instance.save()
        return instance


class BusinessCardSerializer(serializers.Serializer):

    class Meta:
        model = BusinessCard
        fileds = [
            "id",  "role", "phone", "own_site", "linkedin_url", "telegram_url"
        ]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
