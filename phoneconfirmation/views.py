import re

import anyjson

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.translation import gettext_lazy as _

from .forms import PhoneNumberForm
from .models import PhoneConfirmation, PhoneNumber, PhoneCountryCode


def confirm_phone(request, confirm_code):
    confirm_code = confirm_code.lower()
    phone_number = PhoneConfirmation.objects.confirm_phone(confirm_code)
    return render_to_response("phoneconfirmation/confirm_phone.html", {
        "phone_number": phone_number,
        "phone_confirm_code": confirm_code,
    }, context_instance=RequestContext(request))


@login_required
def action(request):
    if request.method == "POST":
        phone = get_object_or_404(
            PhoneNumber,
            user=request.user, phone_number=request.POST.get("phone_number")
        )
        the_action = request.POST.get("action")
        if the_action is None:
            raise Http404()

        if the_action == "primary":
            phone.set_as_primary()
        elif the_action == "send":
            for confirm in phone.phoneconfirmation_set.all():
                confirm.resend()
                break
            else:
                PhoneConfirmation.objects.send_confirmation(phone)
        elif the_action == "remove":
            # only let user delete phone if they have a verified phone or email
            verified_phones = request.user.phonenumber_set.filter(verified=True)
            if request.user.emailaddress_set.filter(verified=True).exists() or \
               verified_phones and (len(verified_phones) > 1 or verified_phones[0] != phone):
                phone.delete()
    return redirect("acct_email")


@login_required
def phone_list(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            country_code_pk = form.cleaned_data["country_code"]
            country_code_number = form.cleaned_data["country_code_other"]
            if country_code_pk:
                country_code = PhoneCountryCode.objects.get(pk=country_code_pk)
            else:
                country_code = PhoneCountryCode.objects.filter(country_code=country_code_number)[0]
            PhoneNumber.objects.add_phone(
                user=request.user,
                phone=form.cleaned_data["phone_number"],
                country_code=country_code,
            )
            return redirect("acct_email")
    else:
        form = PhoneNumberForm()

    phones = PhoneNumber.objects.filter(user=request.user)

    return render_to_response("phoneconfirmation/phone_list.html", {
        "phones": phones,
        "form": form
    }, context_instance=RequestContext(request))


@login_required
def get_country_for_code(request):
    is_valid = False
    possible_country_codes = []
    countries_str = ""

    if not request.is_ajax():
        raise Http404(_("This view only supports AJAX requests."))

    area_code = request.GET.get("code")
    if area_code:
        area_code = area_code.strip("+ ")
        if len(area_code) > 0:
            first_digit = area_code[0]
            try:
                first_digit = int(first_digit)
            except TypeError:
                first_digit = None

            if first_digit:
                possible_country_codes = PhoneCountryCode.objects.filter(starting_number=first_digit)
                countries = []
                for country_code in possible_country_codes:
                    if re.match(country_code.country_regex, area_code):
                        countries.append(country_code.country_name)
                        is_valid = True

                countries_str = " / ".join(countries)
    else:
        is_valid = False

    result = {
        "code": area_code,
        "is_valid": is_valid,
        "countries": countries_str,
    }

    return HttpResponse(
        anyjson.serialize(result),
        mimetype="application/json"
    )
