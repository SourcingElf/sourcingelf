import json, re

content = open(r'C:\Projects\sourcingelf\frontend\Supplier Dashboard - Home.html', 'r', encoding='utf-8').read()

# ── 1. Change const/let declarations to var in the bundle template ────────────
# These appear JSON-encoded in the template string (actual \n chars, \" for quotes)
content = content.replace(
    'const PER_PAGE = 5;\\n    let currentPage = 1;\\n    const totalPages = Math.ceil(leads.length / PER_PAGE);',
    'var PER_PAGE = 5;\\n    var currentPage = 1;\\n    var totalPages = Math.ceil(leads.length / PER_PAGE);'
)

# Change const leads = [ to var leads = [
# The leads array declaration appears as:  ...];  const PER_PAGE...
# We need to find it a bit further back
# Search for 'const leads = [\\n' in the bundle area
old_leads_decl = 'const leads = [\\n'
if old_leads_decl in content:
    content = content.replace(old_leads_decl, 'var leads = [\\n', 1)
    print('Changed const leads to var leads')
else:
    print('WARNING: could not find const leads declaration')

# ── 2. Build the new renderLeads function as normal JS, then JSON-encode it ───
new_render_js = r"""function renderLeads() {
      var c = document.getElementById('leadsContainer');
      if (!c) return;
      var start = (currentPage - 1) * PER_PAGE;
      var page = leads.slice(start, start + PER_PAGE);
      if (!page.length) {
        c.innerHTML = '<div style="text-align:center;padding:60px 20px;color:#9ca3af;font-size:14px;">No buying leads available at the moment.</div>';
        var ind2 = document.getElementById('pageIndicator');
        if (ind2) ind2.textContent = 'Page 1 of 1';
        return;
      }
      c.innerHTML = page.map(function(lead) {
        var isApplied = lead.applied || (window.appliedLeadIds && window.appliedLeadIds.has(lead.id));
        var pills = (lead.market ? '<span class="pill pill-blue">' + lead.market + '</span>' : '') +
          (lead.buyerType ? '<span class="pill pill-navy">' + lead.buyerType + '</span>' : '') +
          (lead.isNew && !isApplied ? '<span class="pill pill-red">NEW</span>' : '');
        var svgCal = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;margin-right:3px"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>';
        var expClass = lead.urgentExpiry ? 'lead-expiry urgent' : 'lead-expiry normal';
        var expLabel = 'Valid until ' + (lead.expiry || '') + (lead.urgentExpiry ? ' · Expiring soon' : '');
        var viewOnclick = "(function(b){var n=b.closest('.lead-card').querySelector('.lead-notes');if(n){n.style.display=n.style.display==='none'?'block':'none';b.textContent=n.style.display==='none'?'View Details':'Hide Details';}})(this)";
        var applyFooter = isApplied
          ? '<span class="apply-link applied">Applied ✓</span>'
          : '<a href="#" class="apply-link" data-lead-id="' + lead.id + '" onclick="(window.applyToLead||function(){})(this.dataset.leadId);return false;">Apply to this lead →</a>';
        return '<div class="lead-card">' +
          '<div class="lead-card-body">' +
            '<div class="lead-info">' +
              '<div class="lead-pills">' + pills + '</div>' +
              '<div class="lead-company">' + (lead.company || lead.title || '') + '</div>' +
              '<div class="lead-products">' + (lead.products || '') + '</div>' +
              '<div class="lead-details">' +
                (lead.moq ? '<div class="detail-item"><strong>MOQ:</strong> ' + lead.moq + '</div>' : '') +
                (lead.budget ? '<div class="detail-item"><strong>Price Range:</strong> ' + lead.budget + '</div>' : '') +
              '</div>' +
              '<div class="' + expClass + '">' + svgCal + expLabel + '</div>' +
            '</div>' +
            '<div style="display:flex;flex-direction:column;align-items:flex-end;gap:12px;flex-shrink:0;">' +
              '<button class="view-details-btn" onclick="' + viewOnclick + '">View Details</button>' +
            '</div>' +
          '</div>' +
          (lead.notes ? '<div class="lead-notes" style="display:none;padding:10px 16px;font-size:13px;color:#555;border-top:1px solid #eee">' + lead.notes + '</div>' : '') +
          '<div class="lead-card-footer">' + applyFooter + '<span class="lead-id">' + lead.id + '</span></div>' +
        '</div>';
      }).join('');
      var ind = document.getElementById('pageIndicator');
      if (ind) ind.textContent = 'Page ' + currentPage + ' of ' + totalPages;
      var pb = document.getElementById('prevBtn');
      var nb = document.getElementById('nextBtn');
      if (pb) pb.disabled = currentPage === 1;
      if (nb) nb.disabled = currentPage === totalPages;
    }"""

# JSON-encode the function (without surrounding quotes) so it fits in the bundle template string
# json.dumps adds surrounding quotes and escapes \n, \", etc.
json_encoded = json.dumps(new_render_js)[1:-1]  # strip surrounding "..."

# Replace the no-op in the bundle
old_noop = 'function renderLeads() {}'
if old_noop in content:
    content = content.replace(old_noop, json_encoded, 1)
    print('Replaced renderLeads no-op with full renderer')
else:
    print('WARNING: could not find renderLeads no-op')

# ── 3. Update the injected script: after browseLeads(), map API leads → bundle format ──
# Find the section from 'const leadsContainer' to 'window.applyToLead = ...'
injected_script_idx = content.rfind('<script>')

# The section to replace starts at 'const leadsContainer = document.getElementById'
OLD_SECTION_START = "    const leadsContainer = document.getElementById('leadsContainer');"
OLD_SECTION_END_MARKER = "    window.applyToLead = function(leadId) {"

start_pos = content.find(OLD_SECTION_START, injected_script_idx)
end_pos = content.find(OLD_SECTION_END_MARKER, injected_script_idx)

if start_pos == -1 or end_pos == -1:
    print('WARNING: could not find section markers in injected script')
    print('start_pos:', start_pos, 'end_pos:', end_pos)
else:
    # Build the replacement section
    new_section = r"""    // Map API leads to bundle field format, expose as global for renderLeads()
    window.leads = (leads || []).map(function(l) {
      var items = l.items || [];
      var first = items[0] || {};
      var name = l.buyer_company || '';
      var spaceIdx = name.indexOf(' ');
      var masked = name ? (name[0] + '**' + (spaceIdx > 0 ? ' ' + name.slice(spaceIdx + 1) : '')) : '';
      var exp = l.expires_at ? new Date(l.expires_at) : null;
      var daysLeft = exp ? Math.ceil((exp - new Date()) / 86400000) : null;
      return {
        id: l.id,
        market: l.buyer_country || '',
        buyerType: (l.buyer_positioning && l.buyer_positioning.length) ? l.buyer_positioning[0] : '',
        isNew: !!(l.created_at && (Date.now() - new Date(l.created_at)) < 86400000),
        company: masked || l.title || '',
        products: items.map(function(i) { return i.product_name; }).join(', '),
        moq: first.quantity ? (first.quantity + ' pcs/style') : '',
        budget: first.price_range || '',
        expiry: exp ? exp.toLocaleDateString('en-GB', {day:'numeric',month:'short',year:'numeric'}) : '',
        urgentExpiry: daysLeft !== null && daysLeft <= 7,
        applied: appliedLeadIds.has(l.id),
        notes: l.notes || ''
      };
    });
    window.totalPages = window.leads.length > 0 ? Math.ceil(window.leads.length / (window.PER_PAGE || 5)) : 1;
    window.currentPage = 1;
    window.appliedLeadIds = appliedLeadIds;
    if (typeof renderLeads === 'function') { renderLeads(); }

"""
    content = content[:start_pos] + new_section + content[end_pos:]
    print('Updated injected script section')

# Write the file
open(r'C:\Projects\sourcingelf\frontend\Supplier Dashboard - Home.html', 'w', encoding='utf-8').write(content)
print('Done.')
