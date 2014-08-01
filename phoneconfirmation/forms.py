import re

from django import forms
from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext_lazy as _

from .models import PhoneCountryCode, PhoneNumber


class SelectDropdownWidget(forms.Select):
    allow_multiple_selected = False

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ""

        option_label_trans = get_template("phoneconfirmation/_country_label.html").render(
            Context({"option_label": option_label})
        )

        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label_trans)))


class CountryCodeCharField(forms.CharField):

    def clean(self, value):
        if value is None:
            return value

        value = re.sub("[\W]+", "", value)
        if value:
            try:
                PhoneCountryCode.objects.get(country_code=value)
            except:
                raise forms.ValidationError(_("Please specify a valid country code"))
        return value


class PhoneConfirmationForm(forms.Form):

    confirm_code = forms.CharField(_("confirmation code"))


class PhoneNumberForm(forms.Form):

    country_code = forms.ChoiceField(
        label=_("Country code"),
        choices=((c.pk, "%s +%s" % (c.country_name, c.country_code)) for c in PhoneCountryCode.objects.all()),
        initial=111,  # pk for Kuwait
        required=False,
        widget=SelectDropdownWidget,
    )
    country_code_other = CountryCodeCharField(required=False)
    phone_number = forms.IntegerField(_("phone number"))

    def country_code_obj(self):
        country_code_pk = self.cleaned_data.get("country_code")
        country_code_number = self.cleaned_data.get("country_code_other")
        if country_code_pk:
            country_code = PhoneCountryCode.objects.get(pk=country_code_pk)
        else:
            country_code = PhoneCountryCode.objects.filter(country_code=country_code_number)[0]
        return country_code

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"]
        if value:
            if PhoneNumber.objects.number_exists(phone=value, country_code=self.country_code_obj()):
                raise forms.ValidationError(_("A user is registered with this phone number."))
        return value
