from django.http import JsonResponse

class ApiHandler:
    def handleReq(request):
        # Log API request
        print("Handling API request")
        # Test vvv
        return JsonResponse({
            "name": "Knight who says Ni",
            "favourite_colour": "red",
        })
