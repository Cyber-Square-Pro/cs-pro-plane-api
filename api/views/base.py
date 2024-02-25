class TokenResponseMixin:
    def handle_token_response(self, request):
        print('//////////////', request)
        if hasattr(request, 'new_access_token') and hasattr(request, 'new_refresh_token'):
            new_access_token = request.new_access_token
            new_refresh_token = request.new_refresh_token
            print('rrrrrrrrr')
            return {'access_token': new_access_token, 'refresh_token': new_refresh_token}
        else:
            print('noooo')
        return {}
 