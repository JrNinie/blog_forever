from django.shortcuts import render, HttpResponse
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from pathlib import Path


def login(request):
    """
    Login page
    """
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
        temp =[]
        for i in range(3):
            temp.append(random.randint(0,255))
        return tuple(temp)

    # Draw background image
    width = 420
    height = 47
    img = Image.new("RGB", (width,height), get_random_color())
    draw = ImageDraw.Draw(img)

    # Define font & size
    project_path = Path(__file__).parent.parent
    haiskey_font = ImageFont.truetype(f"{project_path}/static/blog/font/Chocolate_Covered _Raindrops_BOLD.ttf", 50)
    
    # Draw random letters & numbers
    for i in range(5):
        random_letter_lower = chr(random.randint(97,122))
        random_letter_upper = chr(random.randint(65, 90))
        random_num = str(random.randint(0,9))
        char = random.choice([random_num, random_letter_lower, random_letter_upper])
        draw.text((i*50+100,0), char, get_random_color(),font=haiskey_font)

    # Draw lines
    for i in range(15):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1,y1,x2,y2),fill=get_random_color())

    # Draw points
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x,y), fill=get_random_color())
        draw.arc((x,y, x+4, y+4), 0, 90, fill=get_random_color())

    # Save & get image
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    return HttpResponse(data)
