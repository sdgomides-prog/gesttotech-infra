import frappe
from frappe import _
from kore import __version__


@frappe.whitelist(allow_guest=False)
def status():
    """Health check endpoint.
    
    GET /api/method/kore.api.health.status
    Header: X-API-Key: <kore_api_key>
    """
    from kore.api._auth import require_api_key
    require_api_key()
    
    return {
        "ok": True,
        "version": __version__,
        "app": "kore-pagamento",
        "site": frappe.local.site,
    }
