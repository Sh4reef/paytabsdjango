from rest_framework.views import APIView
from rest_framework.response import Response
from .paytabs import PayTabsAPIClient, CreatePayPage

from .serializers import ValidateSecretKeySerializer, CreatePayPageSerializer


class ValidateSecretKeyAPIView(APIView):

    def get(self, request):
        serializer = ValidateSecretKeySerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = ValidateSecretKeySerializer(data=request.data)
        serializer.is_valid()
        client = PayTabsAPIClient(**serializer.data)
        res = client.validate_secret_key()
        return Response(res)

class CreatePayPageAPIView(APIView):

    def get(self, request):
        serializer = CreatePayPageSerializer()
        return Response(serializer.data)

    @staticmethod
    def get_persoanl_data(data):
        return {
            'cc_first_name': data.get('cc_first_name', 'John'),
            'cc_last_name': data.get('cc_last_name', 'Doe'),
            'cc_phone_number': data.get('cc_phone_number', 505555555),
            'phone_number': data.get('phone_number', 505555555),
        }

    @staticmethod
    def get_billing_address(data):
        return {
            'billing_address': data.get('billing_address', 'Flat 11 Building 222 Block333 Road 444 Manama Bahrain'),
            'state': data.get('state', 'Makkah'),
            'city': data.get('city', 'Makkah'),
            'postal_code': data.get('postal_code', 24238),
            'country': data.get('country', 'SAU'),
        }

    @staticmethod
    def get_shipping_address(data):
        return {
            'shipping_first_name': data.get('shipping_first_name', 'John'),
            'shipping_last_name': data.get('shipping_last_name', 'Doe'),
            'address_shipping': data.get('address_shipping', 'Flat abc road 123'),
            'city_shipping': data.get('city_shipping', 'Makkah'),
            'state_shipping': data.get('state_shipping', 'Makkah'),
            'postal_code_shipping': data.get('postal_code_shipping', 24238),
            'country_shipping': data.get('country_shipping', 'SAU'),
        }

    @staticmethod
    def get_pay_page_params(data):
        return {
            'site_url': data.get('site_url'),
            'email': data.get('email', 'jd@gmail.com'),
            'amount': data.get('amount', 19.00),
            'discount': data.get('discount', 0.00),
            'reference_no': data.get('reference_no', 'SSN-6677'),
            'currency': data.get('currency', 'SAR'),
            'title': data.get('title', 'BlackBox'),
            'ip_customer': data.get('ip_customer', '127.0.0.9'),
            'ip_merchant': data.get('ip_merchant', '127.0.0.6'),
            'return_url': data.get('return_url', 'https://test.com/thankyou'),
            'quantity': data.get('quantity', 1),
            'unit_price': data.get('unit_price', 19.00),
            'other_charges': data.get('other_charges', 0.00),
            'products_per_title': data.get('products_per_title', 'BlackBox'),
            'msg_lang': data.get('msg_lang', 'English'),
            'cms_with_version': 'paytabs-python v1.0'
        }

    def post(self, request):
        serializer = CreatePayPageSerializer(data=request.data)
        serializer.is_valid()

        merchant_email = serializer.data.get('merchant_email')
        secret_key = serializer.data.get('secret_key')
        personal_data = self.get_persoanl_data(serializer.data)
        billing_address = self.get_billing_address(serializer.data)
        shipping_address = self.get_shipping_address(serializer.data)
        pay_page_params = self.get_pay_page_params(serializer.data)

        client = CreatePayPage(merchant_email=merchant_email, secret_key=secret_key)
        client.fill_personal_data(**personal_data)
        client.fill_billing_address(**billing_address)
        client.fill_shipping_address(**shipping_address)

        res = client.create_pay_page(**pay_page_params)

        return Response(res)

