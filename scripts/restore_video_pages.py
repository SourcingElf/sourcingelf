"""D3: restore Video + Video Submit pages from clean backup, inject client.js,
inject D3 init scripts that wire bundle UI to real VideoAPI endpoints.

This is a one-shot script. Idempotent: re-running overwrites the frontend
files with the same backup-derived content. Same approach as D0's
restore of Connected.html and Credits.html.
"""
import os
import sys
sys.stdout.reconfigure(encoding="utf-8")

BACKUP_DIR = r"C:\Projects\Claude Design Backup\standalone"
FRONTEND_DIR = "frontend"

CLIENT_JS_INJECT = '  <script src="api/client.js"></script>\n'

VIDEO_INIT = """  <!-- D3 live integration: load real video status, override bundle stubs -->
  <script>
  (async function() {
    var SE = window.SourcingElf;
    if (!SE) return;

    await new Promise(function(r) { setTimeout(r, 300); });

    if (SE.RouteGuard && SE.RouteGuard.requireSupplier) SE.RouteGuard.requireSupplier();

    function pickState(status) {
      if (!status || status === 'none') return 1;
      if (status === 'materials_submitted' || status === 'in_production' || status === 'revision_requested') return 2;
      if (status === 'draft_ready') return 3;
      if (status === 'published' || status === 'unpublished') return 4;
      return 1;
    }

    var currentVideo = null;

    window.confirmPublish = async function() {
      if (!currentVideo) return;
      var btn = document.getElementById('confirmPublishBtn');
      if (btn) { btn.disabled = true; btn.textContent = 'Publishing\\u2026'; }
      try {
        await SE.VideoAPI.approveVideo(currentVideo.id);
        if (typeof closeLegalModal === 'function') closeLegalModal();
        SE.NotificationHelper.success('Video approved and published!');
        setTimeout(function() { window.location.reload(); }, 1200);
      } catch (e) {
        if (btn) { btn.disabled = false; btn.textContent = 'Confirm Publish'; }
        SE.NotificationHelper.error(e.message || 'Failed to publish');
      }
    };

    window.submitRevision = async function() {
      if (!currentVideo) return;
      var notesEl = document.getElementById('revisionNotes');
      var notes = notesEl ? notesEl.value.trim() : '';
      if (!notes) { SE.NotificationHelper.error('Please describe the revision needed'); return; }
      var btn = document.getElementById('revisionBtn');
      if (btn) { btn.disabled = true; btn.textContent = 'Submitting\\u2026'; }
      try {
        await SE.VideoAPI.requestRevision(currentVideo.id, { notes: notes });
        SE.NotificationHelper.success('Revision request submitted');
        setTimeout(function() { window.location.reload(); }, 1200);
      } catch (e) {
        if (btn) { btn.disabled = false; btn.textContent = 'Submit Revision Request'; }
        SE.NotificationHelper.error(e.message || 'Failed to submit revision');
      }
    };

    function applyState(stateNum) {
      // Bundle's showState(n, btn) requires a button arg; if button missing, do it manually.
      var btn = document.querySelectorAll('.state-btn')[stateNum - 1];
      if (btn && typeof showState === 'function') {
        showState(stateNum, btn);
        return;
      }
      var panels = document.querySelectorAll('.state-panel');
      panels.forEach(function(p) { p.classList.remove('visible'); });
      var panel = document.getElementById('state' + stateNum);
      if (panel) panel.classList.add('visible');
    }

    try {
      var videos = await SE.VideoAPI.getMyVideos();
      currentVideo = (videos && videos.length) ? videos[0] : null;
      applyState(pickState(currentVideo && currentVideo.status));
    } catch (e) {
      console.error('Video load error:', e);
      applyState(1);
    }
  })();
  </script>

</body>"""

VIDEO_SUBMIT_INIT = """  <!-- D3 live integration: replace bundle's file-upload UI with URL inputs (K11 MVP), wire real submitMaterials -->
  <script>
  (async function() {
    var SE = window.SourcingElf;
    if (!SE) return;

    await new Promise(function(r) { setTimeout(r, 300); });

    if (SE.RouteGuard && SE.RouteGuard.requireSupplier) SE.RouteGuard.requireSupplier();

    // K11 MVP: replace bundle's photo file-upload UI with URL textareas.
    // Important: also clear the parent div's onclick (it referenced #photoInput
    // which we're removing — leaving the onclick would null.click() on every
    // mousedown).
    var photoArea = document.getElementById('photoUploadArea') || document.getElementById('photoGrid');
    if (photoArea) {
      photoArea.removeAttribute('onclick');
      photoArea.onclick = null;
      photoArea.style.cursor = 'default';
      photoArea.innerHTML = '<div style="padding:18px;border:1px dashed rgba(26,39,68,0.25);border-radius:10px;background:rgba(26,39,68,0.02);">' +
        '<label style="display:block;font-size:13px;font-weight:600;color:#1a2744;margin-bottom:6px;">Product photo URLs</label>' +
        '<textarea id="photoUrlsInput" rows="3" placeholder="One URL per line. Public Google Drive / Dropbox / Imgur links work." style="width:100%;padding:10px 12px;border:1px solid rgba(26,39,68,0.15);border-radius:7px;font-family:inherit;font-size:13px;resize:vertical;"></textarea>' +
        '<label style="display:block;font-size:13px;font-weight:600;color:#1a2744;margin:14px 0 6px;">Reference video URLs (optional)</label>' +
        '<textarea id="videoUrlsInput" rows="2" placeholder="One URL per line." style="width:100%;padding:10px 12px;border:1px solid rgba(26,39,68,0.15);border-radius:7px;font-family:inherit;font-size:13px;resize:vertical;"></textarea>' +
        '<div style="font-size:11px;color:#9ca3af;margin-top:8px;">File upload coming later. For now, paste public URLs.</div>' +
        '</div>';
    }

    function collectPayload() {
      var photoTxt = (document.getElementById('photoUrlsInput') || {}).value || '';
      var videoTxt = (document.getElementById('videoUrlsInput') || {}).value || '';
      var photo_urls = photoTxt.split(/\\r?\\n/).map(function(s) { return s.trim(); }).filter(Boolean);
      var video_urls = videoTxt.split(/\\r?\\n/).map(function(s) { return s.trim(); }).filter(Boolean);

      var mainProductsEl = document.getElementById('mainProducts');
      var mainProductsDesc = mainProductsEl ? mainProductsEl.value.trim() : '';

      // MOQ: the only <input type="number"> on the page
      var moqInput = document.querySelector('input[type="number"]');
      var min_order_qty = moqInput && moqInput.value ? parseInt(moqInput.value, 10) : null;

      // MOQ unit: the only <select> on the page
      var unitSel = document.querySelector('select');
      var min_order_unit = unitSel && unitSel.value ? unitSel.value : 'pcs';

      // Buyer Nature: .checkbox-group <input type="checkbox"> checked, label text from sibling <span>
      var buyerNature = Array.prototype.slice.call(document.querySelectorAll('.checkbox-group input[type="checkbox"]'))
        .filter(function(cb) { return cb.checked; })
        .map(function(cb) {
          var sp = cb.parentElement.querySelector('span');
          return sp ? sp.textContent.trim() : '';
        })
        .filter(Boolean);

      // Positioning: .toggle-btn.selected NOT inside #marketToggles (markets share the class)
      var positioning = Array.prototype.slice.call(document.querySelectorAll('.toggle-btn.selected'))
        .filter(function(b) { return !b.closest('#marketToggles'); })
        .map(function(b) { return b.textContent.trim(); })
        .filter(Boolean);

      // Selling points: every input inside #sellingPoints with a value
      var sellingPoints = Array.prototype.slice.call(document.querySelectorAll('#sellingPoints input'))
        .map(function(el, idx) { return { description: (el.value || '').trim(), sort_order: idx }; })
        .filter(function(sp) { return sp.description; });

      // Additional notes: the textarea whose placeholder starts with "Anything else"
      var notesEl = Array.prototype.slice.call(document.querySelectorAll('textarea'))
        .filter(function(t) { return /^Anything else/i.test(t.placeholder || ''); })[0];
      var additional_notes = notesEl ? notesEl.value.trim() : '';

      return {
        main_products_desc: mainProductsDesc,
        additional_notes: additional_notes || null,
        target_positioning: positioning.length ? positioning : null,
        target_buyer_nature: buyerNature.length ? buyerNature : null,
        min_order_qty: min_order_qty,
        min_order_unit: min_order_unit,
        photo_urls: photo_urls,
        video_urls: video_urls,
        selling_points: sellingPoints.length ? sellingPoints : null,
      };
    }

    // Override bundle's handleSubmit. Preserve its 2-stage legal flow:
    //   click 1 -> show #legalPanel + change button text + disable
    //   user ticks #legalCheck -> bundle's toggleFinalSubmit re-enables button
    //   click 2 -> actually call submitMaterials
    var legalShown = false;
    window.handleSubmit = async function() {
      if (!legalShown) {
        // Validate before showing legal panel
        var mp = document.getElementById('mainProducts');
        if (!mp || !mp.value.trim()) {
          SE.NotificationHelper.error('Please describe your main products');
          return;
        }
        legalShown = true;
        var panel = document.getElementById('legalPanel');
        if (panel) {
          panel.classList.add('open');
          var y = panel.getBoundingClientRect().top + window.scrollY - 80;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
        var btn1 = document.getElementById('submitBtn');
        if (btn1) {
          btn1.textContent = 'Confirm & Submit \\u2192';
          btn1.disabled = true;
        }
        return;
      }

      var legalCheck = document.getElementById('legalCheck');
      if (!legalCheck || !legalCheck.checked) return;

      var payload = collectPayload();
      var btn = document.getElementById('submitBtn');
      if (btn) { btn.disabled = true; btn.textContent = 'Submitting\\u2026'; }
      try {
        await SE.VideoAPI.submitMaterials(payload);
        SE.NotificationHelper.success('Materials submitted! Our team will start production.');
        setTimeout(function() { window.location.href = '/Supplier%20Dashboard%20-%20Video.html'; }, 1200);
      } catch (e) {
        if (btn) { btn.disabled = false; btn.textContent = 'Confirm & Submit \\u2192'; }
        SE.NotificationHelper.error(e.message || 'Submission failed');
      }
    };
  })();
  </script>

</body>"""


def restore_one(filename: str, init_script: str) -> dict:
    backup_path = os.path.join(BACKUP_DIR, filename)
    target_path = os.path.join(FRONTEND_DIR, filename)

    with open(backup_path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8-sig")  # strip BOM if present

    # Inject client.js script tag before </head>
    head_idx = text.lower().find("</head>")
    text = text[:head_idx] + CLIENT_JS_INJECT + text[head_idx:]

    # Inject init script before </body>
    text = text.replace("</body>", init_script, 1)

    with open(target_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Verify
    with open(target_path, "rb") as f:
        chk = f.read()
    chk_text = chk.decode("utf-8")
    return {
        "size": len(chk),
        "bom": chk.startswith(b"\xef\xbb\xbf"),
        "crlf": b"\r\n" in chk,
        "mojibake": sum(chk_text.count(m) for m in ["鈥", "鉭", "路 5", "锛", "锟"]),
        "has_client_js": 'src="api/client.js"' in chk_text,
        "has_init": "VideoAPI" in chk_text,
    }


if __name__ == "__main__":
    r1 = restore_one("Supplier Dashboard - Video.html", VIDEO_INIT)
    r2 = restore_one("Supplier Dashboard - Video Submit.html", VIDEO_SUBMIT_INIT)
    print("Video.html:", r1)
    print("Video Submit.html:", r2)
