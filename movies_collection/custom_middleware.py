from  movielist.models import RequestCount


class RequestCountMiddleware:
    '''
    Request Count Middleware to Count the Number of Request made to all the Api
    to the server
    '''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if RequestCount.objects.all().count()==0:
            RequestCount.objects.create(requestCount=1)

        else:
            obj = RequestCount.objects.all().first()
            obj.requestCount += 1
            obj.save()

        response = self.get_response(request)
        return response


