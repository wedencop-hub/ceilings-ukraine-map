// MAP MINI APP PROTECTION V2
// Telegram WebView hardening: crypto fallback + Supabase timeout/retry + add-form safety.
(function () {
  try {
    if (window.crypto && !window.crypto.randomUUID && window.crypto.getRandomValues) {
      window.crypto.randomUUID = function () {
        const a = window.crypto.getRandomValues(new Uint8Array(16));
        a[6] = (a[6] & 15) | 64;
        a[8] = (a[8] & 63) | 128;
        return Array.from(a).map((b, i) =>
          ([4, 6, 8, 10].includes(i) ? '-' : '') + b.toString(16).padStart(2, '0')
        ).join('');
      };
    }
  } catch (e) {
    console.warn('MAP CRYPTO FALLBACK', e);
  }

  const originalFetch = window.fetch.bind(window);
  const SUPABASE_RPC = /https?:\/\/[^/]+\.supabase\.co\/rest\/v1\/rpc\//i;

  window.fetch = async function (input, init) {
    let url = '';
    try { url = typeof input === 'string' ? input : (input && input.url) || ''; } catch (_) {}
    if (!SUPABASE_RPC.test(url)) return originalFetch(input, init);

    let lastError;
    for (let attempt = 1; attempt <= 3; attempt++) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 12000);
      try {
        const options = Object.assign({}, init || {}, { signal: controller.signal });
        return await originalFetch(input, options);
      } catch (e) {
        lastError = e;
        if (attempt < 3) await new Promise(r => setTimeout(r, 500 * attempt));
      } finally {
        clearTimeout(timer);
      }
    }
    throw lastError || new Error('Supabase request failed');
  };

  // The address input was removed from the Add Point form, but an older
  // clearForm() still tried to access #addressResults. On Telegram iOS that
  // exception stopped openAdd(), making the ＋ Додати button appear dead.
  function installSafeClearForm() {
    if (typeof window.clearForm !== 'function') return false;
    if (window.clearForm.__safeAddForm) return true;

    const safeClearForm = function () {
      try {
        selectedLat = null;
        selectedLng = null;
        selectedAddress = '';

        ['newName','newPhone','newTelegram','newWebsite','newDescription'].forEach(function(id){
          const el = document.getElementById(id);
          if (el) el.value = '';
        });

        const logo = document.getElementById('newLogo');
        if (logo) logo.value = '';

        const coords = document.getElementById('coords');
        if (coords) coords.textContent = '📍 Координати не вибрані';

        if (temporaryMarker) {
          temporaryMarker.setMap(null);
          temporaryMarker = null;
        }
      } catch (e) {
        console.warn('SAFE CLEAR FORM', e);
      }
    };

    safeClearForm.__safeAddForm = true;
    window.clearForm = safeClearForm;
    return true;
  }

  let tries = 0;
  const timer = setInterval(function () {
    tries++;
    if (installSafeClearForm() || tries > 200) clearInterval(timer);
  }, 50);
})();
