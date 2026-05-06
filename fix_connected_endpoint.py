TARGET = r"C:\Projects\sourcingelf\routers\suppliers.py"

NEW_ENDPOINT = '''

# ── Connected Buyers ─────────────────────────────────────────────────────────

@router.get("/me/connected-buyers")
async def get_connected_buyers(
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    profile = _require_supplier_profile(current_user["id"], db)
    connections = (
        db.table("connections")
        .select("*")
        .eq("supplier_id", profile["id"])
        .order("confirmed_at", desc=True)
        .execute().data
    )
    result = []
    for conn in connections:
        buyer = db.table("buyer_profiles").select("*").eq("id", conn["buyer_id"]).maybe_single().execute()
        if buyer.data:
            bp = buyer.data
            result.append({
                "connection_id": conn["id"],
                "confirmed_at": conn["confirmed_at"],
                "source": conn["source"],
                "buyer_id": bp["id"],
                "company_name": bp["company_name"],
                "business_nature": bp["business_nature"],
                "country": bp["country"],
                "main_products": bp["main_products"],
                "annual_volume": bp["annual_volume"],
                "given_name": bp["given_name"],
                "surname": bp["surname"],
            })
    return result
'''

content = open(TARGET, encoding='utf-8').read()
if '/me/connected-buyers' in content:
    print("ERROR: endpoint already exists, skipping.")
else:
    open(TARGET, 'w', encoding='utf-8').write(content + NEW_ENDPOINT)
    print("OK: endpoint added.")