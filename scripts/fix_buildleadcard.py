content = open(r'C:\Projects\sourcingelf\frontend\Supplier Dashboard - Home.html', 'r', encoding='utf-8').read()
idx = content.find('function buildLeadCard')
end_idx = idx
brace_count = 0
started = False
for i in range(idx, min(idx+10000, len(content))):
    c = content[i]
    if c == '{':
        brace_count += 1
        started = True
    elif c == '}':
        brace_count -= 1
        if started and brace_count == 0:
            end_idx = i + 1
            break

new_func = (
    "function buildLeadCard(lead) {\n"
    "      var items = lead.items || [];\n"
    "      var firstItem = items[0] || {};\n"
    "      var products = items.map(function(i) { return i.product_name; }).join(', ');\n"
    "      var moq = firstItem.quantity ? firstItem.quantity + ' ' + (firstItem.unit || 'pcs') + '/style' : '';\n"
    "      var priceRange = firstItem.price_range || '';\n"
    "      var expiry = lead.expires_at ? new Date(lead.expires_at) : null;\n"
    "      var nowTime = new Date();\n"
    "      var daysLeft = expiry ? Math.ceil((expiry - nowTime) / (1000 * 60 * 60 * 24)) : null;\n"
    "      var expiryStr = expiry ? expiry.toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'}) : '';\n"
    "      var expirySoon = daysLeft !== null && daysLeft <= 7;\n"
    "      var isNew = lead.created_at && (nowTime - new Date(lead.created_at)) < 86400000;\n"
    "      var isApplied = appliedLeadIds.has(lead.id);\n"
    "      var country = lead.buyer_country || '';\n"
    "      var positioning = (lead.buyer_positioning && lead.buyer_positioning.length) ? lead.buyer_positioning[0] : '';\n"
    "      function maskCompany(name) {\n"
    "        if (!name) return '';\n"
    "        var words = name.split(' ');\n"
    "        if (!words[0] || !words[0].length) return name;\n"
    "        return words[0][0] + '**' + (words.length > 1 ? ' ' + words.slice(1).join(' ') : '');\n"
    "      }\n"
    "      var maskedCompany = maskCompany(lead.buyer_company) || lead.title || '';\n"
    "      var pillsHtml = (country ? '<span class=\"pill pill-blue\">' + country + '</span>' : '') +\n"
    "        (positioning ? '<span class=\"pill pill-navy\">' + positioning + '</span>' : '') +\n"
    "        (isNew && !isApplied ? '<span class=\"pill pill-red\">NEW</span>' : '');\n"
    "      var expiryClass = expirySoon ? 'lead-expiry urgent' : 'lead-expiry normal';\n"
    "      var expiryLabel = 'Valid until ' + expiryStr + (expirySoon ? ' · Expiring soon' : '');\n"
    "      var svgCal = '<svg width=\"12\" height=\"12\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" style=\"display:inline-block;vertical-align:middle;margin-right:3px\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"18\" rx=\"2\" ry=\"2\"></rect><line x1=\"16\" y1=\"2\" x2=\"16\" y2=\"6\"></line><line x1=\"8\" y1=\"2\" x2=\"8\" y2=\"6\"></line><line x1=\"3\" y1=\"10\" x2=\"21\" y2=\"10\"></line></svg>';\n"
    "      var viewDetailsOnclick = \"(function(btn){var card=btn.closest('.lead-card');var notes=card&&card.querySelector('.lead-notes');if(notes){notes.style.display=notes.style.display==='none'?'block':'none';btn.textContent=notes.style.display==='none'?'View Details':'Hide Details';}})(this)\";\n"
    "      var applyFooter = isApplied\n"
    "        ? '<span class=\"apply-link applied\">Applied ✓</span>'\n"
    "        : '<a href=\"#\" class=\"apply-link\" data-lead-id=\"' + lead.id + '\" onclick=\"applyToLead(this.dataset.leadId);return false;\">Apply to this lead →</a>';\n"
    "      return '<div class=\"lead-card\">' +\n"
    "        '<div class=\"lead-card-body\">' +\n"
    "          '<div class=\"lead-info\">' +\n"
    "            '<div class=\"lead-pills\">' + pillsHtml + '</div>' +\n"
    "            '<div class=\"lead-company\">' + maskedCompany + '</div>' +\n"
    "            '<div class=\"lead-products\">' + products + '</div>' +\n"
    "            '<div class=\"lead-details\">' +\n"
    "              (moq ? '<div class=\"detail-item\"><strong>MOQ:</strong> ' + moq + '</div>' : '') +\n"
    "              (priceRange ? '<div class=\"detail-item\"><strong>Price Range:</strong> ' + priceRange + '</div>' : '') +\n"
    "            '</div>' +\n"
    "            '<div class=\"' + expiryClass + '\">' + svgCal + expiryLabel + '</div>' +\n"
    "          '</div>' +\n"
    "          '<div style=\"display:flex;flex-direction:column;align-items:flex-end;gap:12px;flex-shrink:0;\">' +\n"
    "            '<button class=\"view-details-btn\" onclick=\"' + viewDetailsOnclick + '\">View Details</button>' +\n"
    "          '</div>' +\n"
    "        '</div>' +\n"
    "        (lead.notes ? '<div class=\"lead-notes\" style=\"display:none;padding:10px 16px;font-size:13px;color:#555;border-top:1px solid #eee\">' + lead.notes + '</div>' : '') +\n"
    "        '<div class=\"lead-card-footer\">' + applyFooter + '<span class=\"lead-id\">' + lead.id + '</span></div>' +\n"
    "      '</div>';\n"
    "    }"
)

new_content = content[:idx] + new_func + content[end_idx:]
open(r'C:\Projects\sourcingelf\frontend\Supplier Dashboard - Home.html', 'w', encoding='utf-8').write(new_content)
print('Done. Old function was', end_idx - idx, 'chars, new is', len(new_func), 'chars')
