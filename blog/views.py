from django.shortcuts import render, HttpResponse
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from pathlib import Path
from django.http import JsonResponse
from django.contrib import auth


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
    def get_random_color():
        """
        Generate random color

        Returns:
            tuple : tuple of 3 numbers (0-255) to present a color
        """
        temp = []
        for i in range(3):
            temp.append(random.randint(0, 255))
        return tuple(temp)

    # Draw background image
    width = 420
    height = 47
    img = Image.new("RGB", (width, height), get_random_color())
    draw = ImageDraw.Draw(img)

    # Define font & size
    project_path = Path(__file__).parent.parent
    haiskey_font = ImageFont.truetype(
        f"{project_path}/static/blog/font/Chocolate_Covered _Raindrops_BOLD.ttf",
        50)

    # Draw random verification code (letters & numbers)
    verification_code_str = ""
    for i in range(5):
        random_letter_lower = chr(random.randint(97, 122))
        random_letter_upper = chr(random.randint(65, 90))
        random_num = str(random.randint(0, 9))
        random_char = random.choice(
            [random_num, random_letter_lower, random_letter_upper])
        draw.text((i * 50 + 100, 0),
                  random_char,
                  get_random_color(),
                  font=haiskey_font)
        verification_code_str += random_char

    # Draw lines
    for i in range(15):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    # Draw points
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=get_random_color())
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # Save & get image
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    # Save verification code in session
    request.session["verification_code_str"] = verification_code_str

    return HttpResponse(data)


def index(request):
    """
    Index page after successed login
    """
    return render(request, "index.html")
