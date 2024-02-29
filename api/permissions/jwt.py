# permissions.py
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from jwt import ExpiredSignatureError
from db.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError

class CustomJWTPermission(BasePermission):
    def has_permission(self, request, view):
        print('permission')
        access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        # user_id =  UntypedToken(access_token)['user_id']
        # print('90900', user_id)
        # request.user_id = user_id
        print(access_token)
        if not access_token:
            print('no token')
            raise PermissionDenied(self.un_authorized('No access token'))
        else:
            print(' token')
            try:
                user_id =  UntypedToken(access_token)['user_id']
                request.user_id = user_id
            except TokenError:
                decoded_token = UntypedToken(access_token, verify=False)
                user_id = decoded_token['user_id']
                user = User.objects.get(id = user_id)
                refresh = RefreshToken.for_user(user)
                new_access_token = str(refresh.access_token)
                new_refresh_token = str(refresh)

                # Update the request with the new access token
                request.new_access_token = new_access_token
                request.new_refresh_token = new_refresh_token
                user_id =  UntypedToken(new_access_token)['user_id']
                print('90900', user_id)
                request.user_id = user_id
                # Continue processing the request with the new tokens
                # response = super().has_permission(request, view)
                # response = super().has_permission(request, view)
                print('====================================')
                # new_tokens_data = {'access_token': new_access_token, 'refresh_token': new_refresh_token}
                # print(new_tokens_data)
                return super().has_permission(request, view)

                # return Response({'new_access_token': new_access_token, 'new_refresh_token': new_refresh_token})
            
            except InvalidToken:
                print('heeee')
                raise PermissionDenied(self.un_authorized('Invalid token'))
         
        return super().has_permission(request, view)
        # try:
        #     data = UntypedToken(access_token)
        # except:
        #     raise PermissionDenied(self.un_authorized('invalid token'))

        # try:
        #     # Validate the access token
        #     result = super().has_permission(request, view)
        #     return result
        # except ExpiredSignatureError:
        #     # Access token has expired, generate new access and refresh tokens
        #     refresh = RefreshToken.for_user(request.user)
        #     new_access_token = str(refresh.access_token)
        #     new_refresh_token = str(refresh)

        #     # Update the request with the new access token
        #     request.access_token = new_access_token
        #     request.refresh_token = new_refresh_token
        #     user_id =  UntypedToken(new_access_token)['user_id']
        #     print('90900', user_id)
        #     request.user_id = user_id
        #     # Continue processing the request with the new tokens
        #     return super().has_permission(request, view)


    def un_authorized(self, error_msg):
            return {'error': error_msg, 'statusCode': 409}