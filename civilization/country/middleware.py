class PoliticalInfluenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.political_context = {
            "influence_detected": True,
            "message": (
                "This visible output has passed through "
                "an underlying influence environment."
            ),
        }

        response = self.get_response(request)
        return response


        