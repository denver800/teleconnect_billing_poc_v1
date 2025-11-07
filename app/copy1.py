#submit custmoer invoice payload
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <wd:Workday_Common_Header xmlns:wd="urn:com.workday/bsvc">
      <wd:Include_Reference_Descriptors_In_Response>true</wd:Include_Reference_Descriptors_In_Response>
    </wd:Workday_Common_Header>
  </soap:Header>
  <soap:Body>
    <wd:Submit_Customer_Invoice_Request xmlns:wd="urn:com.workday/bsvc" wd:Add_Only="true" wd:version="v44.2">
      <wd:Business_Process_Parameters>
        <wd:Auto_Complete>true</wd:Auto_Complete>
        <wd:Comment_Data>
          <wd:Comment>string</wd:Comment>
        </wd:Comment_Data>
      </wd:Business_Process_Parameters>
      <wd:Customer_Invoice_Data>
        <wd:Submit>true</wd:Submit>
        <wd:Locked_in_Workday>true</wd:Locked_in_Workday>

        <wd:Company_Reference wd:Descriptor="?">
          <wd:ID wd:type="Company_Reference_ID">Co_100</wd:ID>
        </wd:Company_Reference>

        <wd:Currency_Reference wd:Descriptor="string">
          <wd:ID wd:type="Currency_ID">CAD</wd:ID>
        </wd:Currency_Reference>

        <wd:Customer_Reference wd:Descriptor="string">
          <wd:ID wd:type="Customer_ID">CUST-000373</wd:ID>
        </wd:Customer_Reference>

        <wd:Sold_To_Customer_Reference wd:Descriptor="string">
          <wd:ID wd:type="Customer_ID">CUST-000373</wd:ID>
        </wd:Sold_To_Customer_Reference>

        <wd:Bill_To_Address_Reference wd:Descriptor="string">
          <wd:ID wd:type="Address_ID">ADDRESS_REFERENCE-6-3660</wd:ID>
        </wd:Bill_To_Address_Reference>

        <wd:Bill_To_Contact_Reference wd:Descriptor="string">
          <wd:ID wd:type="Business_Entity_Contact_ID">CON_1990</wd:ID>
        </wd:Bill_To_Contact_Reference>

        <wd:Delivery_Type_Reference wd:Descriptor="string">
          <wd:ID wd:type="Document_Delivery_Type_ID">DOCUMENT_DELIVERY_TYPE-3-1</wd:ID>
        </wd:Delivery_Type_Reference>

        <wd:Delivery_Type_Origin_Reference wd:Descriptor="string">
          <wd:ID wd:type="Interest_and_Late_Fee_Rule_Origination_Source_ID">CUSTOMER</wd:ID>
        </wd:Delivery_Type_Origin_Reference>

        <wd:Accounting_Date>2025-08-29Z</wd:Accounting_Date>
        <wd:From_Date>2025-08-29Z</wd:From_Date>
        <wd:To_Date>2025-08-29Z</wd:To_Date>
        <wd:Due_Date_Override>2025-08-29Z</wd:Due_Date_Override>

        <wd:Payment_Terms_Reference wd:Descriptor="string">
          <wd:ID wd:type="Payment_Terms_ID">Net_37</wd:ID>
        </wd:Payment_Terms_Reference>

        <wd:Payment_Type_Reference wd:Descriptor="string">
          <wd:ID wd:type="Payment_Type_ID">PAYMENT_TYPE-3-21</wd:ID>
        </wd:Payment_Type_Reference>

        <wd:Amount_Due>2170.95</wd:Amount_Due>

        <wd:Customer_Invoice_Type_Reference wd:Descriptor="string">
          <wd:ID wd:type="Customer_Invoice_Type_ID">Telesat_Canada</wd:ID>
        </wd:Customer_Invoice_Type_Reference>

        <wd:Customer_PO_Number>Contract# 3445-4</wd:Customer_PO_Number>
        <wd:Finance_Charge>false</wd:Finance_Charge>
        <wd:On_Hold>false</wd:On_Hold>
        <wd:Is_Excluded_from_Dunning_Letter>false</wd:Is_Excluded_from_Dunning_Letter>
        <wd:Memo>string</wd:Memo>

        <wd:Customer_Invoice_Line_Replacement_Data>
          <wd:Line_Order>00000001</wd:Line_Order>

          <wd:Intercompany_Affiliate_Reference wd:Descriptor="string">
            <wd:ID wd:type="Company_Reference_ID">Co_100</wd:ID>
          </wd:Intercompany_Affiliate_Reference>

          <wd:Revenue_Category_Reference wd:Descriptor="string">
            <wd:ID wd:type="Revenue_Category_ID">RC_Broadcast_Service_Revenue_-_Levy_Eligible</wd:ID>
          </wd:Revenue_Category_Reference>

          <wd:Line_Item_Description>Telesat Contract 3445-4
Monthly charge associated with the provision of 200 KHz Ku-band partial RF channel space segment.</wd:Line_Item_Description>

          <wd:Tax_Applicability_Reference wd:Descriptor="string">
            <wd:ID wd:type="Tax_Applicability_ID">TA_CA_GSTHST</wd:ID>
          </wd:Tax_Applicability_Reference>

          <wd:Tax_Code_Reference wd:Descriptor="string">
            <wd:ID wd:type="Tax_Code_ID">TC_CAN_ONT_LEVY_BROADCAST</wd:ID>
          </wd:Tax_Code_Reference>

          <wd:Quantity>0.2</wd:Quantity>

          <wd:Unit_of_Measure_Reference wd:Descriptor="string">
            <wd:ID wd:type="UN_CEFACI_Common_Code_ID">MHZ</wd:ID>
          </wd:Unit_of_Measure_Reference>

          <wd:Quantity_2>1</wd:Quantity_2>

          <wd:Unit_of_Measure_2_Reference wd:Descriptor="string">
            <wd:ID wd:type="UN_CEFACI_Common_Code_ID">MON</wd:ID>
          </wd:Unit_of_Measure_2_Reference>

          <wd:Unit_Cost>10790</wd:Unit_Cost>
          <wd:From_Date>2025-08-29Z</wd:From_Date>
          <wd:To_Date>2025-08-29Z</wd:To_Date>
          <wd:Extended_Amount>2158</wd:Extended_Amount>
          <wd:Deferred_Revenue>false</wd:Deferred_Revenue>
          <wd:Memo>string</wd:Memo>

          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Organization_Reference_ID">APP_Distribution</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Organization_Reference_ID">PRD_FT</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Organization_Reference_ID">RE_Canada</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Organization_Reference_ID">3rdParty</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Location_ID">LOC_ZBCK</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Custom_Worktag_1_ID">REP</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Custom_Worktag_3_ID">NA</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Custom_Worktag_5_ID">CF_Cash_transaction</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Custom_Worktag_2_ID">KUK</wd:ID>
          </wd:Worktags_Reference>
          <wd:Worktags_Reference wd:Descriptor="string">
            <wd:ID wd:type="Custom_Worktag_4_ID">BIT_RENEWAL</wd:ID>
          </wd:Worktags_Reference>
        </wd:Customer_Invoice_Line_Replacement_Data>

        <wd:Tax_Code_Data>
          <wd:Tax_Applicability_Reference wd:Descriptor="string">
            <wd:ID wd:type="Tax_Applicability_ID">TA_CA_GSTHST</wd:ID>
          </wd:Tax_Applicability_Reference>
          <wd:Tax_Code_Reference wd:Descriptor="string">
            <wd:ID wd:type="Tax_Code_ID">TC_CAN_ONT_LEVY_BROADCAST</wd:ID>
          </wd:Tax_Code_Reference>
          <wd:Tax_Amount>12.95</wd:Tax_Amount>

          <wd:Tax_Rate_Data>
            <wd:Tax_Rate_Reference wd:Descriptor="string">
              <wd:ID wd:type="Tax_Rate_ID">TR_CAN_LEVY_BROADCAST</wd:ID>
            </wd:Tax_Rate_Reference>
            <wd:Tax_Amount>12.95</wd:Tax_Amount>
            <wd:Tax_Point_Date_Type_Reference wd:Descriptor="string">
              <wd:ID wd:type="Tax_Point_Date_Type_ID">INVOICE/ADJUSTMENT_DATE</wd:ID>
            </wd:Tax_Point_Date_Type_Reference>
            <wd:Tax_Point_Date>2025-08-29Z</wd:Tax_Point_Date>
          </wd:Tax_Rate_Data>
        </wd:Tax_Code_Data>
      </wd:Customer_Invoice_Data>
    </wd:Submit_Customer_Invoice_Request>
  </soap:Body>
</soap:Envelope>


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
