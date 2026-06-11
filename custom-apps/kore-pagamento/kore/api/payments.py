import frappe
from frappe import _
from kore.api._auth import require_api_key
from kore.api._happypay import HappyPayClient


@frappe.whitelist(allow_guest=False)
def create_pix_charge(amount, description, correlation_id=None):
    """Cria uma cobrança PIX via HappyPay.
    
    POST /api/method/kore.api.payments.create_pix_charge
    Body: { amount, description, correlation_id }
    """
    require_api_key()
    
    amount = frappe.utils.flt(amount)
    if amount <= 0:
        frappe.throw(_("Amount must be greater than zero"), frappe.ValidationError)
    
    client = HappyPayClient()
    result = client.create_pix_charge(amount, description, correlation_id)
    
    # Salvar no DocType Kore Charge
    charge = frappe.new_doc("Kore Charge")
    charge.charge_id = result.get("id") or result.get("correlationID")
    charge.amount = amount
    charge.description = description
    charge.status = "Pending"
    charge.raw_response = frappe.as_json(result)
    charge.insert(ignore_permissions=True)
    
    return {
        "charge_name": charge.name,
        "charge_id": charge.charge_id,
        "pix_copy_paste": result.get("brCode") or result.get("pixCopyPaste"),
        "qr_code": result.get("qrCodeImage"),
        "status": "Pending",
    }


@frappe.whitelist(allow_guest=False)
def get_charge(charge_id):
    """Consulta status de uma cobrança."""
    require_api_key()
    client = HappyPayClient()
    return client.get_charge(charge_id)


@frappe.whitelist(allow_guest=False)
def cancel_charge(charge_id):
    """Cancela uma cobrança."""
    require_api_key()
    client = HappyPayClient()
    result = client.cancel_charge(charge_id)
    
    frappe.db.set_value("Kore Charge", {"charge_id": charge_id}, "status", "Cancelled")
    return result


@frappe.whitelist(allow_guest=False)
def mark_paid(charge_id):
    """Marca uma cobrança como paga (webhook interno)."""
    require_api_key()
    frappe.db.set_value("Kore Charge", {"charge_id": charge_id}, "status", "Paid")
    return {"ok": True, "charge_id": charge_id, "status": "Paid"}
