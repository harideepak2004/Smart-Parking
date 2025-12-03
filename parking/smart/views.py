from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import ParkingUser, CompanyDetail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import json

@login_required
def detail_view(request):
    floors = list(range(1, 13))
    slots  = list(range(1, 13))
    return render(request, "detail.html", {"floors": floors, "slots": slots})

def user(request):
    if request.method == "POST":
        # Handle both JSON and form POST
        if request.content_type == "application/json":
            data = json.loads(request.body)
            name = data.get("name")
            car_number = data.get("car_number")
            email = data.get("email")
            phone = data.get("phone")
            slot = data.get("slot", "Not Assigned")
        else:
            name = request.POST.get("name")
            car_number = request.POST.get("car_number")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            slot = request.POST.get("slot", "Not Assigned")

        if not slot:
            return HttpResponse("Error: Slot not received")

        user = ParkingUser.objects.create(
            name=name,
            car_number=car_number,
            email=email,
            phone=phone,
            slot=slot,
            login_time=timezone.now(),
            is_active=True
        )

        # Return JSON if requested
        if request.content_type == "application/json":
            return JsonResponse({"success": True, "user_id": user.id})

        return redirect("slot")

    return render(request, "user.html")

def user_details(request, user_id):
    try:
        user = ParkingUser.objects.get(id=user_id)

        return JsonResponse({
            "id": user.id,
            "name": user.name,
            "car_number": user.car_number,
            "email": user.email,
            "phone": user.phone,
            "slot": user.slot,
            "login_time": user.login_time.strftime('%Y-%m-%d %H:%M:%S'),
            "logout_time": user.logout_time.strftime('%Y-%m-%d %H:%M:%S') if user.logout_time else "Not Logged Out",
            "is_active": user.is_active,
        })

    except ParkingUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@csrf_exempt
def save_slot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            slot = data.get('slot')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid JSON: {e}'})

        if not slot:
            return JsonResponse({'status': 'error', 'message': 'No slot provided'})

        SelectedSlot.objects.create(slot=slot)
        return JsonResponse({'status': 'success', 'slot': slot})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def remove_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(ParkingUser, id=user_id)
        user.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

from datetime import timedelta



from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def logout_user(request, user_id):
    try:
        user = ParkingUser.objects.get(id=user_id)

        user.logout_time = timezone.now()
        user.is_active = False
        user.save()

        duration = user.logout_time - user.login_time
        hours = round(duration.total_seconds() / 3600, 2)
        price = user.price_per_hour
        total_amount = round(hours * price, 2)

        html_message = render_to_string(
            'email_bill.html',
            {
                'user': user,
                'duration_hours': hours,
                'price_per_hour': price,
                'total_amount': total_amount,
            }
        )

        email = EmailMessage(
            subject=f"Smart Parking Bill for {user.car_number}",
            body=html_message,
            from_email=None,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()

        return JsonResponse({
            "status": "success",
            "logout_time": user.logout_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_hours": hours,
            "price_per_hour": price,
            "total_amount": total_amount,
            "email_sent": True
        })

    except ParkingUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)




def available(request):
    company = CompanyDetail.objects.first()
    return render(request, "available.html", {"company": company})

def outpass(request):
    users = ParkingUser.objects.all()
    return render(request, "outpass.html", {"users": users})

def home(request):
    return render(request, "home.html")

def qr(request):
    return render(request, "qr.html")

def slot(request):
    return render(request, "slot.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def logout(request):
    return render(request, "logout.html")
