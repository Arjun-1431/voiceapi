from django.conf import settings
from django.http import JsonResponse
from twilio.jwt.access_token import AccessToken  # ✅ Import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant  # ✅ Import VoiceGrant
from django.conf import settings

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from twilio.rest import Client
import urllib.parse



def make_outbound_call(request):
    """Initiates an outbound call to a real phone number using Twilio API."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    to_number = request.GET.get("to")  # ✅ Get the number from the request
    if not to_number:
        return JsonResponse({"error": "Missing 'to' phone number"}, status=400)

    try:
        # ✅ Make sure Twilio sends the call to the correct endpoint
        twiml_url = f"http://91.108.104.12:8000/calls/handle_call/?to={urllib.parse.quote(to_number)}"

        call = client.calls.create(
            url=twiml_url,  # ✅ Twilio will fetch call instructions from this URL
            to=to_number.strip(),
            from_=settings.TWILIO_PHONE_NUMBER
        )
        return JsonResponse({"message": "Call initiated!", "call_sid": call.sid})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse, Dial
@csrf_exempt  # ✅ Disable CSRF protection for Twilio Webhooks
def handle_call(request):
    """Handles Twilio incoming calls and connects to an outbound number."""
    
    # ✅ Check if request is POST (Twilio sends POST requests)
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=400)
    
    response = VoiceResponse()
    
    # ✅ Twilio sends phone number in "to" parameter (GET or POST)
    to_number = request.GET.get("to") or request.POST.get("To")
    
    if not to_number:
        return HttpResponse("Missing 'to' phone number", status=400)

    # ✅ Connect the WebRTC caller to the entered phone number
    dial = Dial(callerId=settings.TWILIO_PHONE_NUMBER)
    dial.number(to_number)
    response.append(dial)

    return HttpResponse(str(response), content_type="text/xml")

import os
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from django.http import JsonResponse

def get_twilio_token(request):
    """Generates Twilio token for WebRTC calls in the browser using direct Twilio credentials."""

    # ✅ Directly using Twilio credentials
    account_sid = "AC210ec7eba66580e3e0c826715e953b30"
    api_key = "SK30fb5275625bae99a33b99d75f73ff8f"
    api_secret = "2pmbSG4pBdMGAgnGbUM08dfQTuB8lrwi"
    twilio_app_sid = "AP4156881fa24b686a853b0664ca8a382e"

    identity = "+13139216344"  # Using Twilio number as identity

    # ✅ Generate Twilio WebRTC Token
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)
    voice_grant = VoiceGrant(outgoing_application_sid=twilio_app_sid)
    token.add_grant(voice_grant)

    return JsonResponse({"token": token.to_jwt()})

def call_page(request):
  return render(request, "call.html")
