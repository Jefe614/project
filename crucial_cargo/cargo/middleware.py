class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.user.is_authenticated:
            if not hasattr(response.context_data, 'profile_name'):
                response.context_data['profile_name'] = request.user.username
        return response