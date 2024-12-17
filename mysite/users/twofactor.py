def twoFactorAuth(request):
    if request.method == "POST":
        form_code = request.POST.get("twoFA")
        user_id = request.session["2fa_user_id"]
        verf_service = os.getenv("VERIFICATION_SERVICE")
        if not verf_service:
            return HttpResponse(
                b"Internal server error verification service not found", status=500
            )

        if not user_id:
            return HttpResponse(b"Internal server error lost user_id", status=500)

        user = User.objects.filter(id=user_id).first()
        twilio_client = Client(os.getenv("ACCOUNT_SID"), os.getenv("auth_token"))

        verification_check = twilio_client.verify.v2.services(
            verf_service
        ).verification_checks.create(to=user.phoneNumber, code=form_code)

        if verification_check.status != "approved":
            return HttpResponse(b"Authentication failed!", status=401)

        del request.session["2fa_user_id"]
        login(request, user)
        return redirect("/auth/home")

    else:
        return render(request, "twofa.html")


def loginUser(request):
	if request.method == "GET":
		return render(request, "login.html")

	username = request.POST.get("username")
	password = request.POST.get("password")

	verf_service = os.getenv("VERIFICATION_SERVICE")
	if not verf_service:
		if request.headers.get("x-requested-with") == "XMLHttpRequest":
			return JsonResponse({"error": "Internal server error verification service not found"}, status=500)
		return HttpResponse(b"Internal server error verification service not found", status=500)
	user = User.objects.filter(username=username).first()
	if user is None:
		if request.is_ajax():
			return JsonResponse({"error": "Authentication failed! Invalid username or password"}, status=401)
		return HttpResponse(b"Authentication failed! Invalid username or password", status=401)
	elif not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
		if request.headers.get("x-requested-with") == "XMLHttpRequest":
			return JsonResponse({"error": "Authentication failed! Invalid username or password"}, status=401)
		return HttpResponse(b"Authentication failed! Invalid username or password", status=401)
	twilio_client = Client(os.getenv("ACCOUNT_SID"), os.getenv("auth_token"))
	_ = twilio_client.verify.v2.services(verf_service).verifications.create(to=user.phoneNumber, channel="sms")
	request.session["2fa_user_id"] = user.id
	if request.headers.get("x-requested-with") == "XMLHttpRequest":
		return JsonResponse({"message": "Two factor authentication required	"}, status=200)
	return redirect("/auth/twofa")