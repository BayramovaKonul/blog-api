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
    