from rest_framework import serializers
from authentication.models import User




class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    #profile = AccountProfileSerializer(required=False, read_only=False)
    #profile_pic = AccountProfilePicSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['uuid','full_name','email', 'username','phone_number','password', 'password2',
        'date_joined']
        read_only_fields = ['id','uuid','date_joined']
        extra_kwargs = {
            'password':{'write_only':True}
            
        }
    

    def create(self, validated_data):
        account = User(
            full_name = self.validated_data['full_name'],
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            phone_number=self.validated_data['phone_number'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error':'passwords must match'})
        account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data, partial=True):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance 




