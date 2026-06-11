import requests
import frappe
from frappe import _


class HappyPayClient:
    """Cliente HTTP para a API HappyPay.
    
    Configurar em site_config.json:
        happypay_api_key: chave fornecida pela HappyPay
        happypay_base_url: https://api.happypay...
    """

    def __init__(self):
        self.base_url = frappe.conf.get("happypay_base_url", "").rstrip("/")
        self.api_key = frappe.conf.get("happypay_api_key", "")
        
        if not self.base_url or not self.api_key:
            frappe.throw(
                _("HappyPay not configured. Set happypay_base_url and happypay_api_key in site_config.json"),
                frappe.ValidationError
            )

    def _headers(self):
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            resp = requests.request(method, url, headers=self._headers(), timeout=30, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            frappe.log_error(f"HappyPay HTTP error: {e}", "HappyPay")
            frappe.throw(_(f"HappyPay error: {e}"), frappe.ValidationError)
        except Exception as e:
            frappe.log_error(f"HappyPay request failed: {e}", "HappyPay")
            frappe.throw(_(f"HappyPay request failed: {e}"), frappe.ValidationError)

    def create_pix_charge(self, amount, description, correlation_id=None):
        return self._request("POST", "/pix/charge", json={
            "amount": amount,
            "description": description,
            "correlationID": correlation_id,
        })

    def get_charge(self, charge_id):
        return self._request("GET", f"/charge/{charge_id}")

    def cancel_charge(self, charge_id):
        return self._request("DELETE", f"/charge/{charge_id}")
