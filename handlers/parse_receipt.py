import requests

BASE_URL = "https://verifyapi.leulzenebe.pro"

def verify_telebirr(reference: str, api_key: str) -> dict:
    """
    Verify a Telebirr transaction.
    request: { "reference": "CE626EJRNS" }
    """
    url = f"{BASE_URL}/verify-telebirr"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {"reference": reference}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def verify_cbe(reference: str, account_suffix: str, api_key: str) -> dict:
    """
    Verify a CBE transaction.
    request: { "reference": "TXN123456789", "accountSuffix": "12345678" }
    """
    url = f"{BASE_URL}/verify-cbe"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "reference": reference,
        "accountSuffix": account_suffix
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


# Example usage
if __name__ == "__main__":
    api_key = "Y21leHR0eG9nMDAwb25xMGtqOG9qdmhsbS0xNzU2NTMyMDYyMjUzLTBxbHNqbWwxYTBy"  # replace with your real key

    # 🔹 Telebirr
    try:
        tele_result = verify_telebirr("CHQ9FIR7HF", api_key)
        print("✅ Telebirr result:\n", tele_result)
    except Exception as e:
        print("⚠️ Telebirr error:", e)

    # 🔹 CBE
    try:
        cbe_result = verify_cbe("FT252495TBF9", "90706431", api_key)
        print("✅ CBE result:\n", cbe_result)
    except Exception as e:
        print("⚠️ CBE error:", e)
