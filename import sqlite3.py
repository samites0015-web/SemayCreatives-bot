import httpx
from lxml import html


def fetch_transaction_details(transaction_id):
    url = f"https://transactioninfo.ethiotelecom.et/receipt/{transaction_id}"

    with httpx.Client(http2=True) as client:
        response = client.get(url)
        if response.status_code != 200:
            print("Failed to fetch receipt.")
            return None

        tree = html.fromstring(response.content)

        data = {
            "invoice_no": None,
            "payment_date": None,
            "settled_amount": None,
            "total_paid_amount": None,
            "credited_party_name": None,
            "credited_party_account": None,
            "payer_name": None,
            "payer_telebirr_no": None,
            "transaction_status": None,
            "payment_mode": None,
            "payment_reason": None,
            "service_fee": None,
        }

        # --- Extract from general table rows ---
        for row in tree.xpath("//tr"):
            cells = row.xpath(".//td")
            if len(cells) != 2:
                continue

            label = cells[0].text_content().strip().lower()
            value = cells[1].text_content().strip()

            if "payer name" in label:
                data["payer_name"] = value
            elif "payer telebirr" in label:
                data["payer_telebirr_no"] = value
            elif "credited party name" in label:
                data["credited_party_name"] = value
            elif "credited party account" in label:
                data["credited_party_account"] = value
            elif "transaction status" in label:
                data["transaction_status"] = value
            elif "payment mode" in label:
                data["payment_mode"] = value
            elif "payment reason" in label:
                data["payment_reason"] = value

        # --- Extract invoice details ---
        invoice_table = None
        for table in tree.xpath("//table"):
            if "Invoice details" in table.text_content():
                invoice_table = table
                break

        if invoice_table is not None:
            rows = invoice_table.xpath(".//tr")
            for i, row in enumerate(rows):
                cells = row.xpath(".//td")
                if len(cells) == 3 and "Invoice No." in cells[0].text_content():
                    values = rows[i + 1].xpath(".//td")
                    data["invoice_no"] = values[0].text_content().strip()
                    data["payment_date"] = values[1].text_content().strip()
                    data["settled_amount"] = values[2].text_content().strip()
                elif len(cells) == 3:
                    label = cells[1].text_content().strip().lower()
                    val = cells[2].text_content().strip()
                    if "service fee" in label and "vat" not in label:
                        data["service_fee"] = val
                    elif "total paid" in label:
                        data["total_paid_amount"] = val

        return data


if __name__ == "__main__":
    transaction_id = input("Enter the transaction ID: ").strip()
    result = fetch_transaction_details(transaction_id)
    if result:
        print("\n📄 Transaction Summary:")
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print("❌ No transaction data found.")
