from django.conf.urls import url, patterns


urlpatterns = patterns(
    "phoneconfirmation.views",
    url(r"^$", "phone_list", name="phone_list"),
    url(r"^confirm_phone/(\w+)/$", "confirm_phone", name="phone_confirm"),
    url(r"^action/$", "action", name="phone_action"),
    url(r"^get-country-for-code/$", "get_country_for_code", name="get_country_for_code")
)
