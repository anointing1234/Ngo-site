from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from pypaystack2 import Paystack
import uuid
import requests
from django.http import JsonResponse
import logging
import re
from datetime import datetime
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.conf import settings
import os
import json, requests, logging
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)

def home(request):  
    return render(request, 'index.html', {
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY
    })


def about_us(request):  
    return render(request, 'about_us.html',)


def projects(request):
    return render(request,'projects.html')


def contact(request):
    return render(request,'contact.html')

def donate(request):
    return render(request,'donate.html')




def process_donation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        donor_name = data.get("donor_name")
        donor_email = data.get("donor_email")
        donor_phone = data.get("donor_phone")
        donation_amount = data.get("donation_amount")
        donor_message = data.get("donor_message")
        paystack_ref = data.get("paystack_reference")

        # Professional email to admin
        subject = f"New Donation Received from {donor_name}"

        message = f"""
A new donation has been successfully recorded.

========================================
          DONOR INFORMATION
========================================
Name: {donor_name}
Email: {donor_email}
Phone Number: {donor_phone}

========================================
          DONATION DETAILS
========================================
Amount Donated: NGN {donation_amount}
Payment Reference: {paystack_ref}

========================================
          DONOR MESSAGE
========================================
{donor_message or "No message provided."}

You may log in to the admin dashboard for further details.
"""

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

        # Email to Donor
        donor_subject = "Thank You for Your Donation"
        donor_message = f"""
Dear {donor_name},

Thank you for your generous donation to our foundation.
We sincerely appreciate your support and commitment to our mission.

========================================
          DONATION RECEIPT
========================================
Donor Name: {donor_name}
Amount: NGN {donation_amount}
Payment Reference: {paystack_ref}

Your support helps us continue our charitable work and transform lives.

If you have any questions, feel free to reach out anytime.

Warm regards,
Akajiugo Charity Foundation
"""

        send_mail(
            donor_subject,
            donor_message,
            settings.DEFAULT_FROM_EMAIL,
            [donor_email],
            fail_silently=True
        )

        return JsonResponse({"status": "success", "message": "Donation processed successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request"})



def contact_send(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")
            subject = data.get("subject")
            message = data.get("message")

            if not all([name, email, subject, message]):
                return JsonResponse({"status": "error", "message": "All fields are required."})

            # Email to admin
            admin_subject = f"New Contact Message: {subject}"
            admin_message = f"""
            You have received a new message from your website contact form.

            Name: {name}
            Email: {email}
            Subject: {subject}
            Message:
            {message}
            """
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

            # Optional: Confirmation email to user
            user_subject = "Thank you for contacting us"
            user_message = f"""
            Hi {name},

            Thank you for reaching out to us. We have received your message:

            Subject: {subject}
            Message:
            {message}

            Our team will get back to you shortly.

            Best regards,
            [Your Organization Name]
            """
            send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [email])

            return JsonResponse({"status": "success", "message": "Your message has been sent successfully."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method."})