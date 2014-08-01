from django.test import TestCase

from django.contrib.auth.models import User

from phoneconfirmation.models import PhoneNumber, PhoneCountryCode


class login(object):
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class PhoneNumberTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("dhume", "david@hume.net", "is-ought")

    def test_digits_only_arabic(self):
        number = "615-555-1212"
        expected_digits_only = "16155551212"
        self.user1.phonenumber_set.create(
            phone_number=number,
            country_code=PhoneCountryCode.objects.get(country_short="US")
        )
        self.assertEquals(self.user1.phonenumber_set.all()[0].digits_only, expected_digits_only)

    def test_creation_in_form(self):
        with login(self, "dhume", "is-ought"):
            response = self.post("phone_list", data={
                "country_code": 227,
                "country_code_other": "",
                "phone_number": "6035551212",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(PhoneNumber.objects.count(), 1)

            response = self.post("phone_list", data={
                "country_code": "",
                "country_code_other": "247",
                "phone_number": "4125551781",
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(PhoneNumber.objects.count(), 2)
