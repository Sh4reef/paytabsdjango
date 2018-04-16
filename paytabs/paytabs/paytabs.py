from requests import request


class PayTabsAPIClient(object):

    def __init__(self, **opts):
        self.auth = {
            'merchant_email': opts.get('merchant_email'),
            'secret_key': opts.get('secret_key')
        }
        self.site_url = opts.get('site_url', 'https://console.graph.cool/')
        self.personal_info = None
        self.billing_address = None
        self.shipping_address = None

    @staticmethod
    def get_headers():
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def validate_secret_key(self):
        endpoint = 'https://www.paytabs.com/apiv2/validate_secret_key'

        payload = {
            'merchant_email': None,
            'secret_key': None
        }

        payload = dict(payload, **self.auth)

        return request('POST', endpoint, data=payload, headers=self.get_headers()).json()

    def verify_payment(self, payment_reference):
        endpoint = 'https://www.paytabs.com/apiv2/verify_payment'
        payload = dict(self.auth, **{'payment_reference': payment_reference})
        return request('POST', endpoint, data=payload, headers=self.get_headers()).json()


class CreatePayPage(PayTabsAPIClient):

    def fill_personal_data(self, **opts):
        self.personal_info = {
            'cc_first_name': opts.get('cc_first_name', 'John'),
            'cc_last_name': opts.get('cc_last_name', 'Doe'),
            'cc_phone_number': opts.get('cc_phone_number', 505555555),
            'phone_number': opts.get('phone_number', 505555555),
        }

        return self

    def fill_billing_address(self, **opts):
        self.billing_address = {
            'billing_address': opts.get('billing_address', 'Flat 11 Building 222 Block333 Road 444 Manama Bahrain'),
            'state': opts.get('state', 'Makkah'),
            'city': opts.get('city', 'Makkah'),
            'postal_code': opts.get('postal_code', 24238),
            'country': opts.get('country', 'SAU'),
        }

        return self

    def fill_shipping_address(self, **opts):
        self.shipping_address = {
            'shipping_first_name': opts.get('shipping_first_name', 'John'),
            'shipping_last_name': opts.get('shipping_last_name', 'Doe'),
            'address_shipping': opts.get('address_shipping', 'Flat abc road 123'),
            'city_shipping': opts.get('city_shipping', 'Makkah'),
            'state_shipping': opts.get('state_shipping', 'Makkah'),
            'postal_code_shipping': opts.get('postal_code_shipping', 24238),
            'country_shipping': opts.get('country_shipping', 'SAU'),
        }

        return self

    def create_pay_page(self, **opts):
        endpoint = 'https://www.paytabs.com/apiv2/create_pay_page'

        paypage = {
            'site_url': self.site_url,
            'email': opts.get('email', 'jd@gmail.com'),
            'amount': opts.get('amount', 19.00),
            'discount': opts.get('discount', 0.00),
            'reference_no': opts.get('reference_no', 'SSN-6677'),
            'currency': opts.get('currency', 'SAR'),
            'title': opts.get('title', 'BlackBox'),
            'ip_customer': opts.get('ip_customer', '127.0.0.9'),
            'ip_merchant': opts.get('ip_merchant', '127.0.0.6'),
            'return_url': opts.get('return_url', 'https://test.com/thankyou'),
            'quantity': opts.get('quantity', 1),
            'unit_price': opts.get('unit_price', 19.00),
            'other_charges': opts.get('other_charges', 0.00),
            'products_per_title': opts.get('products_per_title', 'BlackBox'),
            'msg_lang': opts.get('msg_lang', 'English'),
            'cms_with_version': 'paytabs-python v1.0'
        }

        payload = dict(paypage, **self.auth, **self.personal_info, **self.billing_address, **self.shipping_address)

        return request('POST', endpoint, data=payload, headers=self.get_headers()).json()