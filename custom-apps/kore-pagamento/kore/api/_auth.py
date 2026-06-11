import hmac
import frappe
from frappe import _


def require_api_key():
    """Verifica X-API-Key contra frappe.conf.kore_api_key usando comparação constante."""
    api_key = frappe.request.headers.get("X-API-Key", "")
    expected = frappe.conf.get("kore_api_key", "")
    
    if not expected:
        frappe.throw(
            _("kore_api_key not configured in site_config.json"),
            frappe.AuthenticationError
        )
    
    if not hmac.compare_digest(
        api_key.encode("utf-8"),
        expected.encode("utf-8")
    ):
        frappe.throw(_("Invalid API Key"), frappe.AuthenticationError)
