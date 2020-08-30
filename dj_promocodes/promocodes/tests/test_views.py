from django.utils import timezone
from rest_framework import status
from django.shortcuts import reverse
from rest_framework.test import APITestCase, APIClient
from dj_promocodes.users.tests.factories import UserFactory
from dj_promocodes.promocodes.tests.factories import PromocodeFactory


# Create your tests here.
class TestPay(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.payload = {
            "amount": 100,
            "promocode_code": "code",
            "user_id": self.user.id,
        }
        self.client = APIClient()
        self.url = reverse("promocodes:pay")

    def test_pay_with_inactive_promocode(self):
        now = timezone.localtime(timezone.now()).date()
        start_date = now - timezone.timedelta(days=1)
        end_date = now + timezone.timedelta(days=1)
        promocode = PromocodeFactory(
            code="code",
            start_date=start_date,
            end_date=end_date,
            is_active=False,
        )
        self.payload["promocode_code"] = promocode.code
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = {"promocode_code": ["This promocode isn't active!"]}
        self.assertEqual(response.json(), expected_error)

    def test_pay_with_promocode_ahead_start_date(self):
        now = timezone.localtime(timezone.now()).date()
        start_date = now + timezone.timedelta(days=1)
        end_date = now + timezone.timedelta(days=2)
        promocode = PromocodeFactory(
            code="code",
            start_date=start_date,
            end_date=end_date,
            is_active=True,
        )
        self.payload["promocode_code"] = promocode.code
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = {"promocode_code": ["This promocode isn't active!"]}
        self.assertEqual(response.json(), expected_error)

    def test_pay_with_promocode_behind_end_date(self):
        now = timezone.localtime(timezone.now()).date()
        start_date = now - timezone.timedelta(days=2)
        end_date = now - timezone.timedelta(days=1)
        promocode = PromocodeFactory(
            code="code",
            start_date=start_date,
            end_date=end_date,
            is_active=True,
        )
        self.payload["promocode_code"] = promocode.code
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = {"promocode_code": ["This promocode isn't active!"]}
        self.assertEqual(response.json(), expected_error)

    def test_pay_with_invalid_promocode_quantity(self):
        now = timezone.localtime(timezone.now()).date()
        start_date = now - timezone.timedelta(days=1)
        end_date = now + timezone.timedelta(days=1)
        promocode = PromocodeFactory(
            code="code",
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            quantity=1,
        )
        # this is a one-time redeem promocode
        self.payload["promocode_code"] = promocode.code
        self.client.post(self.url, self.payload, format="json")  # actual redeem

        response = self.client.post(
            self.url, self.payload, format="json"
        )  # can't redeem
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = {"promocode_code": ["This promocode is already sold!"]}
        self.assertEqual(response.json(), expected_error)

    def test_pay_with_invalid_promocode_frequency(self):
        now = timezone.localtime(timezone.now()).date()
        start_date = now - timezone.timedelta(days=1)
        end_date = now + timezone.timedelta(days=1)
        promocode = PromocodeFactory(
            code="code",
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            quantity=10,
            frequency_of_use=1,
        )
        # this is a one-time redeem promocode per user
        self.payload["promocode_code"] = promocode.code
        self.client.post(self.url, self.payload, format="json")  # actual redeem

        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = {"promocode_code": ["You already used this promocode before!"]}
        self.assertEqual(response.json(), expected_error)

        # but this new user can redeem this promocode
        another_user = UserFactory()
        self.payload["user_id"] = another_user.id
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        to_be_included = {
            "status": "SUCCESSFUL",
            "user_name": another_user.username,
            "promocode_title": promocode.title,
            "promocode_code": promocode.code,
        }
        self.assertDictContainsSubset(to_be_included, response.json())
