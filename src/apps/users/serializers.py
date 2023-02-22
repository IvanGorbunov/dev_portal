from rest_framework import serializers


class ChangeUserMixin(serializers.Serializer):

    def validate(self, attrs):
        attrs.update({'change_last_user': self.get_request_user()})
        return super().validate(attrs)

    def get_request_user(self):
        return self.context['request'].user


class AuthorMixin(ChangeUserMixin):

    def validate(self, attrs):
        attrs.update({'author': self.get_request_user()})
        return super().validate(attrs)
