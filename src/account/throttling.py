from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class UserRegisterThrottle(AnonRateThrottle):
    rate = '3/min'

class AdminOrUserThrottle(UserRateThrottle):  # To differentiate admin and regular users
    scope='regular_user'

    def allow_request(self, request, view):
        if request.user.is_staff:
            self.scope='admin'
        else:
            self.scope='regular_user'
        return super().allow_request(request, view)
    
class AddFollowerThrottle(UserRateThrottle):
    
    def allow_request(self, request, view):
        # Apply throttle only for POST requests, not DELETE
        if request.method == 'POST':
            self.scope = 'adding_follower'
        return super().allow_request(request, view)
    

class ContactUsThrottle(UserRateThrottle):
    rate='10/hour'

class AddorDeleteBookMark(UserRateThrottle):  # To differentiate adding/deleting bookmarks

    def allow_request(self, request, view):
        if request.method=="POST":
            self.scope='add_bookmark'

        elif request.method=="DELETE":
            self.scope='delete_bookmark'

        return super().allow_request(request, view)