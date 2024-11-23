from django.http import HttpResponse
from django.shortcuts import render, redirect
import bcrypt
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from twilio.rest import Client


# Create your views here.


def login_page(request):
    # TODO MOVE THIS TO ENVIROMENT
    account_sid = "AC43065e552467653c7090ba1b33e581fb"
    auth_token = "1c3c0cf76b6d8725a77d50a3ccd424b9"
    verification_service = "VA97f28e44c48ab30c1df8e245ced27eab"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user is not None:
            if not (
                bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
            ):
                return HttpResponse(
                    b"Authentication failed! Invalid username or password", status=401
                )

            client = Client(account_sid, auth_token)
            _ = client.verify.v2.services(verification_service).verifications.create(
                to=user.phoneNumber, channel="sms"
            )

            request.session["2fa_user_id"] = user.id

            return redirect("/auth/twofa")
        else:
            return HttpResponse(
                b"Authentication failed! Invalid username or password", status=401
            )
    else:
        return render(request, "login.html")


def twoFactorAuth(request):
    # TODO MOVE THIS TO ENVIROMENT
    account_sid = "AC43065e552467653c7090ba1b33e581fb"
    auth_token = "1c3c0cf76b6d8725a77d50a3ccd424b9"
    verification_service = "VA97f28e44c48ab30c1df8e245ced27eab"

    if request.method == "POST":
        form_code = request.POST.get("twoFA")
        user_id = request.session["2fa_user_id"]

        if not user_id:
            return HttpResponse(b"Internal server error lost user_id", status=500)

        user = User.objects.filter(id=user_id).first()
        twillio_client = Client(account_sid, auth_token)

        verification_check = twillio_client.verify.v2.services(
            verification_service
        ).verification_checks.create(to=user.phoneNumber, code=form_code)

        if verification_check.status != "approved":
            return HttpResponse(b"Authentication failed!", status=401)

        del request.session["2fa_user_id"]
        login(request, user)
        return redirect("/auth/home")

    else:
        return render(request, "twofa.html")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    name = request.POST.get("name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_pass = request.POST.get("password2")
    phonenumber = request.POST.get("phonenumber")

    user = User.objects.filter(username=username)

    if user:
        return HttpResponse(b"User already exists", status=400)

    if password != confirm_pass:
        return HttpResponse(b"Passwords do not match", status=400)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User(
        name=name,
        username=username,
        email=email,
        password=hashed.decode("utf-8"),
        phoneNumber=phonenumber,
    )
    user.save()

    return redirect("/auth/login")


@login_required(login_url="/auth/login")
def home_page(request):
    return render(request, "home.html")
