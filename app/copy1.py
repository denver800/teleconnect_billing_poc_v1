#josn_to_workday.py
from datetime import datetime
from typing import Any, Dict, Tuple, List, Optional

# If you prefer, move this into config.settings
COMPANY_ID = "YOUR_COMPANY_GUID_HERE"  # the “InvoicingCompany …” value you said starts with 3 and ends with 2

def _get(d: Any, path: str) -> Any:
    """
    Safe getter: _get(obj, "a.b.c") -> value or None
    - ignores missing keys
    - supports simple list indexes like 'items.0.name' (optional)
    """
    cur = d
    for part in path.split("."):
        if cur is None:
            return None
        # list index support
        if isinstance(cur, list):
            try:
                idx = int(part)
                cur = cur[idx]
                continue
            except (ValueError, IndexError):
                return None
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur

def _norm_date(value: Optional[str]) -> Optional[str]:
    """
    Normalize date to YYYY-MM-DD if possible.
    Accepts 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS' formats.
    """
    if not value:
        return None
    v = value.strip()
    # fast path
    if len(v) >= 10 and v[4] == "-" and v[7] == "-":
        return v[:10]
    # try a couple formats
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d"):
        try:
            return datetime.strptime(v, fmt).strftime("%Y-%m-%d")
        except Exception:
            pass
    return v  # fallback: return as is

def build_workday_payload(record_json: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str], List[str]]:
    """
    Returns (payload, warnings, errors).
    Only builds 1 invoice line for now from the parProdBlock paths you provided.
    """
    warnings: List[str] = []
    errors: List[str] = []

    # ---- Top-level fields (bare minimum) ----
    customer_id = _get(record_json, "customerRef")
    currency_id = _get(record_json, "accCurrencyCode")
    invoice_date = _norm_date(_get(record_json, "invoiceActualDate"))

    if not COMPANY_ID:
        errors.append("Missing COMPANY_ID constant.")
    if not customer_id:
        errors.append("Missing required 'customerRef' for Customer.")
    if not currency_id:
        errors.append("Missing required 'accCurrencyCode' for Currency.")
    if not invoice_date:
        errors.append("Missing required 'invoiceActualDate' for Invoice Date.")

    # ---- Line data (first/only line for now) ----
    desc = _get(record_json, "parProdBlock.parprodtariffdescription")
    revenue_category = _get(record_json, "parProdBlock.parprodlabel")

    from_date = _norm_date(_get(record_json, "parProdBlock.parprodrecurBlock.parprodrecurfromdate"))
    to_date   = _norm_date(_get(record_json, "parProdBlock.parprodrecurBlock.parprodrecurtodate"))

    qty       = _get(record_json, "parProdBlock.parprodrecurBlock.parprodrectable.records.QTY")
    qty2      = _get(record_json, "parProdBlock.parprodrecurBlock.parprodrectable.records.QTY_2")
    unit_cost = _get(record_json, "parProdBlock.parprodrecurBlock.parprodrectable.records.UNITRATE")
    ext_amt   = _get(record_json, "parProdBlock.parprodrecurBlock.parprodrectotal.amount")
    tax_code  = _get(record_json, "parProdBlock.parprodrecurBlock.parprodrectable.records.TAX_CODE_ID")  # optional

    # minimal sanity checks for line
    if not desc:
        warnings.append("Line: missing description.")
    if qty is None:
        warnings.append("Line: missing Quantity.")
    if unit_cost is None:
        warnings.append("Line: missing Unit Cost.")
    # ext_amt often computed by WD, we pass if we have it
    # from/to dates optional but helpful
    if not from_date or not to_date:
        warnings.append("Line: missing period start/end dates.")

    if errors:
        return None, warnings, errors

    # ---- Build Workday payload (mirrors your POC shape) ----
    line: Dict[str, Any] = {
        "Line_Item_Description": desc,
        "Quantity": qty,
        "Unit_Cost": unit_cost,
    }
    if qty2 is not None:
        line["Quantity_2"] = qty2
    if ext_amt is not None:
        line["Extended_Amount"] = ext_amt
    if from_date:
        line["From_Date"] = from_date
    if to_date:
        line["To_Date"] = to_date
    if revenue_category:
        line["Revenue_Category_Reference"] = {
            "ID": {"_type": "Revenue_Category_ID", "_value_1": revenue_category}
        }
    if tax_code:
        line["Tax_Code_Reference"] = {
            "ID": {"_type": "Tax_Code_ID", "_value_1": tax_code}
        }

    payload: Dict[str, Any] = {
        "Customer_Invoice_Data": {
            "Company_Reference": {
                "ID": {"_type": "Company_Reference_ID", "_value_1": COMPANY_ID}
            },
            "Customer_Reference": {
                "ID": {"_type": "Customer_Reference_ID", "_value_1": customer_id}
            },
            "Currency_Reference": {
                "ID": {"_type": "Currency_ID", "_value_1": currency_id}
            },
            "Invoice_Date": invoice_date,
            "Customer_Invoice_Line_Replacement_Data": [line],
        },
        "Business_Process_Parameters": {"Auto_Complete": True},
    }

    return payload, warnings, errors


#blob_checker.py
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from config.settings import ACCOUNT_URL, ACCOUNT_KEY, CONTAINER_NAME, LOCAL_INCOMING_DIR
from src.db.operations import add_new_pair

def check_new_pairs():
    print("🔍 Checking Azure container for new .pb + control.json pairs...")

    os.makedirs(LOCAL_INCOMING_DIR, exist_ok=True)

    # Connect to Azure
    blob_service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=ACCOUNT_KEY)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    # List all blobs in container
    blobs = [b.name for b in container_client.list_blobs()]
    pb_files = [b for b in blobs if b.endswith(".pb")]
    json_files = [b for b in blobs if b.startswith("control_") and b.endswith(".json")]

    print(f"📦 Found {len(pb_files)} .pb files and {len(json_files)} control files in Azure.\n")

    for pb in pb_files:
        base_name = pb.replace(".pb", "")
        control_file = f"control_{base_name}.json"

        # Check if both files exist
        if control_file not in json_files:
            print(f"⚠️ Skipping {pb}: missing {control_file}")
            continue

        # Check if pair already exists in DB
        file_id, is_new = add_new_pair(pb, control_file)
        if not is_new:
            print(f"⏭️ Pair already exists in DB, skipping download: {pb}")
            continue

        # Download both files
        for blob_name in [pb, control_file]:
            local_path = os.path.join(LOCAL_INCOMING_DIR, blob_name)
            print(f"⬇️ Downloading {blob_name} ...")
            blob_client = container_client.get_blob_client(blob_name)
            with open(local_path, "wb") as f:
                f.write(blob_client.download_blob().readall())
            print(f"✅ Saved {blob_name} to {local_path}")

    print("\n✨ Blob pair check completed.\n")

if __name__ == "__main__":
    check_new_pairs()
