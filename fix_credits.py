with open('C:/Projects/sourcingelf/routers/credits.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '    }).execute()\n    return created.data[0]'
new = '    }).execute()\n    if created and created.data:\n        return created.data[0]\n    result2 = db.table("credits").select("*").eq("supplier_id", supplier_id).maybe_single().execute()\n    return result2.data if result2 else {}'

content = content.replace(old, new)

with open('C:/Projects/sourcingelf/routers/credits.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')