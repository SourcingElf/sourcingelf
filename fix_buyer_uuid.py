"""
修复 test.buyer 的 UUID 不匹配问题
old_id（users 表手动插入）: bae1599d-b815-4473-a248-52c76609a04d
new_id（Supabase Auth 实际 UUID）: dcc3f777-c350-4286-9436-af2081118958
"""
from database import supabase_admin as db

OLD_USER_ID  = 'bae1599d-b815-4473-a248-52c76609a04d'
NEW_USER_ID  = 'dcc3f777-c350-4286-9436-af2081118958'
BP_ID        = '8ea03203-0c55-44b6-acac-6f7085106aac'  # buyer_profiles.id 不变

# ── 1. 备份现有数据 ────────────────────────────────────────────
print("=== 备份现有数据 ===")

user_rec = db.table('users').select('*').eq('id', OLD_USER_ID).maybe_single().execute().data
print("user:", user_rec)

bp_rec = db.table('buyer_profiles').select('*').eq('id', BP_ID).maybe_single().execute().data
print("buyer_profile:", bp_rec)

leads = db.table('buying_leads').select('*').eq('buyer_id', BP_ID).execute().data
print("leads:", len(leads))

lead_items_all = []
for lead in leads:
    items = db.table('buying_lead_items').select('*').eq('lead_id', lead['id']).execute().data
    lead_items_all.append((lead['id'], items))
    print(f"  lead {lead['id']}: {len(items)} items")

# 买家发出的请求（buyer_requests 引用 buyer_profile_id）
# 检查 buyer_requests 是否有 buyer_profile_id 字段
try:
    buyer_reqs = db.table('buyer_requests').select('*').eq('buyer_profile_id', BP_ID).execute().data
except:
    buyer_reqs = []
print("buyer_requests referencing BP_ID:", len(buyer_reqs))

# ── 2. 按 FK 顺序删除 ──────────────────────────────────────────
print("\n=== 删除旧记录 ===")

# 2a. 删 buying_lead_items
for lead_id, items in lead_items_all:
    if items:
        r = db.table('buying_lead_items').delete().eq('lead_id', lead_id).execute()
        print(f"  deleted {len(r.data)} items for lead {lead_id}")

# 2b. 删 buying_leads
if leads:
    for lead in leads:
        db.table('buying_leads').delete().eq('id', lead['id']).execute()
    print(f"  deleted {len(leads)} leads")

# 2c. 删 buyer_requests referencing BP_ID
if buyer_reqs:
    db.table('buyer_requests').delete().eq('buyer_profile_id', BP_ID).execute()
    print(f"  deleted {len(buyer_reqs)} buyer_requests")

# 2d. 删 buyer_profiles
db.table('buyer_profiles').delete().eq('id', BP_ID).execute()
print("  deleted buyer_profile")

# 2e. 删旧 users 记录
db.table('users').delete().eq('id', OLD_USER_ID).execute()
print("  deleted old user")

# ── 3. 用正确 UUID 重新插入 ────────────────────────────────────
print("\n=== 重建记录 ===")

# 3a. 插入 users（正确 UUID）
new_user = {**user_rec, 'id': NEW_USER_ID}
db.table('users').insert(new_user).execute()
print("  inserted user with correct UUID")

# 3b. 插入 buyer_profiles（user_id 改为新 UUID，其余不变）
new_bp = {**bp_rec, 'user_id': NEW_USER_ID}
db.table('buyer_profiles').insert(new_bp).execute()
print("  inserted buyer_profile with correct user_id")

# 3c. 恢复 buying_leads
for lead in leads:
    db.table('buying_leads').insert(lead).execute()
    print(f"  restored lead {lead['id']}")

# 3d. 恢复 buying_lead_items
for lead_id, items in lead_items_all:
    if items:
        db.table('buying_lead_items').insert(items).execute()
        print(f"  restored {len(items)} items for lead {lead_id}")

# 3e. 恢复 buyer_requests
if buyer_reqs:
    db.table('buyer_requests').insert(buyer_reqs).execute()
    print(f"  restored {len(buyer_reqs)} buyer_requests")

print("\n=== 验证 ===")
verify = db.table('users').select('id, email, role').eq('id', NEW_USER_ID).maybe_single().execute()
print("users:", verify.data)
verify_bp = db.table('buyer_profiles').select('id, user_id, company_name').eq('id', BP_ID).maybe_single().execute()
print("buyer_profiles:", verify_bp.data)

print("\nDONE")
