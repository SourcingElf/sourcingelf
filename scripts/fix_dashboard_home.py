"""
One-shot fix for Supplier Dashboard - Home.html:
  R1: replace 5 hardcoded fake lead cards with a loading placeholder
  R2: ourRenderLeads handles empty + error states (no static fallback anymore)
  R3: buildLeadCard maps to real API fields (title / items[0] / no region/buyer_type pills)
  R4: confirmApply selector switched from onclick-match to data-lead-id (UUID-safe)

Reads/writes UTF-8 with default newline translation, so CRLF on disk is preserved.
Each step asserts the OLD block is found before replacing.
"""
import sys

PATH = 'frontend/Supplier Dashboard - Home.html'
with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()
orig_len = len(text)

# ============================================================
# R1: Replace static lead cards with a loading placeholder
# ============================================================
old1_start_anchor = '  <div class="leads-feed" id="leadsFeed">'
old1_end_anchor = '  <!-- PAGINATION -->'
s = text.find(old1_start_anchor)
e = text.find(old1_end_anchor, s)
assert s >= 0 and e > s, 'R1 anchors not found'
old1 = text[s:e]
new1 = (
    '  <div class="leads-feed" id="leadsFeed">\n'
    '    <div class="leads-loading" style="padding:40px;text-align:center;color:#9ca3af;font-size:14px;">Loading buying leads…</div>\n'
    '  </div>\n\n'
)
text = text[:s] + new1 + text[e:]
print(f'R1 leadsFeed: {len(old1)} -> {len(new1)} bytes')

# ============================================================
# R2: ourRenderLeads — handle empty + error states
# ============================================================
old2 = """  // ── Load real leads from API, bypassing bundle placeholder ──
  async function ourRenderLeads() {
    try {
      if (typeof SourcingElf === 'undefined' || !SourcingElf.LeadsAPI) return;
      const result = await SourcingElf.LeadsAPI.browseLeads();
      const leads = Array.isArray(result) ? result : (result.leads || result.data || []);
      if (!leads.length) return;
      const html = leads.map(buildLeadCard).join('');
      const lc = document.getElementById('leadsFeed');
      lc.__allowOurRender = true;
      lc.innerHTML = html;
      lc.__allowOurRender = false;
    } catch (e) {
      // keep static leads on API error
    }
  }"""
new2 = """  // ── Load real leads from API, bypassing bundle placeholder ──
  async function ourRenderLeads() {
    const lc = document.getElementById('leadsFeed');
    try {
      if (typeof SourcingElf === 'undefined' || !SourcingElf.LeadsAPI) return;
      const result = await SourcingElf.LeadsAPI.browseLeads();
      const leads = Array.isArray(result) ? result : (result.leads || result.data || []);
      const html = leads.length
        ? leads.map(buildLeadCard).join('')
        : '<div class="leads-empty" style="padding:40px;text-align:center;color:#9ca3af;font-size:14px;">No active buying leads at the moment.</div>';
      lc.__allowOurRender = true;
      lc.innerHTML = html;
      lc.__allowOurRender = false;
    } catch (e) {
      lc.__allowOurRender = true;
      lc.innerHTML = '<div class="leads-error" style="padding:40px;text-align:center;color:#dc2626;font-size:14px;">Failed to load buying leads. Please refresh.</div>';
      lc.__allowOurRender = false;
    }
  }"""
assert old2 in text, 'R2 ourRenderLeads block not found'
text = text.replace(old2, new2)
print(f'R2 ourRenderLeads: {len(old2)} -> {len(new2)} bytes')

# ============================================================
# R3: buildLeadCard — real API field mapping
# ============================================================
old3 = """  function buildLeadCard(lead) {
    const isApplied = lead.applied || lead.has_applied;
    const isNew = lead.is_new;
    const soon = lead.expires_at && (new Date(lead.expires_at) - Date.now() < 7 * 864e5);
    const expDate = lead.expires_at
      ? new Date(lead.expires_at).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
      : '';
    const pills = [
      lead.region ? `<span class="pill pill-blue">${lead.region}</span>` : '',
      lead.buyer_type ? `<span class="pill pill-navy">${lead.buyer_type}</span>` : '',
      isNew ? '<span class="pill pill-new">NEW</span>' : ''
    ].join('');
    const moqSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>`;
    const priceSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
    const arrowSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`;
    const imgPlaceholder = `<div class="lead-image-placeholder"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>`;
    const footer = isApplied
      ? `<span class="applied-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>Applied ✓</span>`
      : `<a href="javascript:void(0)" class="apply-link" onclick="applyLead(${lead.id})">Apply to this lead ${arrowSvg}</a>`;
    return `<div class="lead-card">
  <div class="lead-card-body">
    <div class="lead-info">
      <div class="lead-pills">${pills}</div>
      <div class="lead-company">${lead.company_name || lead.buyer_name || '—'}</div>
      <div class="lead-products">${lead.product_description || lead.products || ''}</div>
      <div class="lead-details">${lead.moq ? `<span>${moqSvg}MOQ: ${lead.moq}</span>` : ''}${lead.price_range ? `<span>${priceSvg}${lead.price_range}</span>` : ''}</div>
      ${expDate ? `<div class="lead-expiry${soon ? ' amber' : ''}">Valid until ${expDate}${soon ? ' — expires soon' : ''}</div>` : ''}
    </div>
    <div class="lead-image-wrap">${imgPlaceholder}<button class="view-btn" onclick="viewLead(${lead.id})">View Details</button></div>
  </div>
  <div class="lead-card-footer">${footer}<span class="lead-id">#${lead.lead_ref || lead.id}</span></div>
</div>`;
  }"""
new3 = """  function buildLeadCard(lead) {
    const isApplied = lead.applied || lead.has_applied;
    const isNew = lead.is_new;
    const item = (lead.items && lead.items[0]) || {};
    const productName = item.product_name || '';
    const moq = item.quantity ? (item.quantity + ' pcs') : '';
    const priceRange = item.price_range || '';
    const soon = lead.expires_at && (new Date(lead.expires_at) - Date.now() < 7 * 864e5);
    const expDate = lead.expires_at
      ? new Date(lead.expires_at).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
      : '';
    const pills = isNew ? '<span class="pill pill-new">NEW</span>' : '';
    const moqSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>`;
    const priceSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>`;
    const arrowSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`;
    const imgPlaceholder = `<div class="lead-image-placeholder"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>`;
    const footer = isApplied
      ? `<span class="applied-label"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>Applied ✓</span>`
      : `<a href="javascript:void(0)" class="apply-link" data-lead-id="${lead.id}" onclick="applyLead(&quot;${lead.id}&quot;)">Apply to this lead ${arrowSvg}</a>`;
    return `<div class="lead-card">
  <div class="lead-card-body">
    <div class="lead-info">
      <div class="lead-pills">${pills}</div>
      <div class="lead-company">${lead.title || ''}</div>
      <div class="lead-products">${productName}</div>
      <div class="lead-details">${moq ? `<span>${moqSvg}MOQ: ${moq}</span>` : ''}${priceRange ? `<span>${priceSvg}${priceRange}</span>` : ''}</div>
      ${expDate ? `<div class="lead-expiry${soon ? ' amber' : ''}">Valid until ${expDate}${soon ? ' — expires soon' : ''}</div>` : ''}
    </div>
    <div class="lead-image-wrap">${imgPlaceholder}<button class="view-btn" onclick="viewLead(&quot;${lead.id}&quot;)">View Details</button></div>
  </div>
  <div class="lead-card-footer">${footer}<span class="lead-id">#${lead.lead_ref || (lead.id ? lead.id.slice(0, 8) : '')}</span></div>
</div>`;
  }"""
assert old3 in text, 'R3 buildLeadCard block not found'
text = text.replace(old3, new3)
print(f'R3 buildLeadCard: {len(old3)} -> {len(new3)} bytes')

# ============================================================
# R4: confirmApply selector — onclick match -> data-lead-id match
# ============================================================
old4 = "var link = document.querySelector('.apply-link[onclick=\"applyLead(' + id + ')\"]');"
new4 = "var link = document.querySelector('.apply-link[data-lead-id=\"' + id + '\"]');"
assert old4 in text, 'R4 confirmApply selector not found'
text = text.replace(old4, new4)
print(f'R4 confirmApply: selector switched to data-lead-id')

# ============================================================
# Write back (UTF-8, default newline translation preserves CRLF on Windows)
# ============================================================
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)
print(f'WROTE {PATH}: {orig_len} -> {len(text)} chars')
