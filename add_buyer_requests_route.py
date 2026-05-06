with open(r"C:\Projects\sourcingelf\routers\suppliers.py", "r", encoding="utf-8") as f:
    content = f.read()

new_route = '''

# ── Buyer Requests received by this supplier ─────────────────────────────────

@router.get("/me/buyer-requests")
async def get_my_buyer_requests(
    status: str = None,
    current_user: dict = Depends(require_role("supplier")),
    db: Client = Depends(get_db),
):
    """Supplier views buyer requests they have received."""
    profile = _require_supplier_profile(current_user["id"], db)
    query = db.table("buyer_requests").select("*").eq("supplier_id", profile["id"])
    if status:
        query = query.eq("status", status)
    result = query.order("created_at", desc=True).execute()
    return result.data
'''

with open(r"C:\Projects\sourcingelf\routers\suppliers.py", "a", encoding="utf-8") as f:
    f.write(new_route)

print("SUCCESS - new route added to suppliers.py")