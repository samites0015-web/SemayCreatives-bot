from ethiobank_receipts import extract_receipt
from pprint import pprint

def fetch_receipts(urls):
    """
    urls: dict -> {bank_name: transaction_id}
    Returns: dict -> {bank_name: receipt_data or error message}
    """
    """urls = {
    "cbe": "https://apps.cbe.com.et:100/?id=FT*************",
    "dashen": "https://receipt.dashensuperapp.com/receipt/**************",
    "awash": "https://awashpay.awashbank.com:8225/-*****************",
    "boa": "https://cs.bankofabyssinia.com/slip/?trx=****************",
    "zemen": "https://share.zemenbank.com/rt/****************/pdf",
    "tele": "CHQ0FJ403O"
    }
    """
    results = {}
    for bank, txn_id in urls.items():
        try:
            result = extract_receipt(bank, txn_id)
            results[bank] = result
        except Exception as e:
            results[bank] = f"Failed: {e}"
    return results

# Only run this if this file is executed directly, NOT when imported
if __name__ == "__main__":
    urls = {
        "tele": "CHQ0FJ403O",
    }
    receipts = fetch_receipts(urls)
    pprint(receipts)
