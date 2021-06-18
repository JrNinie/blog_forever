from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from .utils.verification_code import generate_verification_code_img


def login(request):
    """
    Login page
    """
    if request.method == "POST":
        response = {"user": None, "message": None}

        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        verification_code = request.POST.get('verification_code')

        verification_code_str = request.session.get("verification_code_str")
        if verification_code.upper() == verification_code_str.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                # use ajax, so no redirection here
                auth.login(request, user)  # so current user is request.user
                response["user"] = user.username
                response["message"] = "Login successed"
            else:
                response["message"] = "Username or password incorrect"
        else:
            response["message"] = "Verification code incorrect"
        return JsonResponse(response)

    return render(request, 'login.html')


def get_verification_code_img(request):
    """
    Generate verification code image for login page
    """
    verification_code_img = generate_verification_code_img(request)

    return HttpResponse(verification_code_img)


def index(request):
    """
    Index page after successed login
    """
    return render(request, "index.html")
