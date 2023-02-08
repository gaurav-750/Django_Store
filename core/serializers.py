from djoser.serializers import UserCreateSerializer as BaseUCS


class UserCreateSerializer(BaseUCS):
    class Meta(BaseUCS.Meta):
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]
