// MigraSL: rank-picker.js: dropdown darajooyin oo raadin leh, oo loo kala qaybiyay saddex koox
(function () {
  const ORDER = ['enlisted', 'officer', 'general'];
  const GROUP_BADGE = {
    enlisted: 'background:rgba(59,130,246,.18);color:#93c5fd;',
    officer:  'background:rgba(245,158,11,.18);color:#fcd34d;',
    general:  'background:rgba(244,63,94,.18);color:#fda4af;'
  };
  const CSS = `
  .rp{position:relative;width:100%;}
  .rp-btn{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 16px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);color:#fff;cursor:pointer;text-align:left;font:inherit;}
  .rp-btn:focus{outline:none;border-color:#3b82f6;background:rgba(59,130,246,.1);}
  .rp-panel{position:absolute;z-index:60;left:0;right:0;top:calc(100% + 6px);max-height:380px;display:none;flex-direction:column;background:#0f172a;border:1px solid rgba(255,255,255,.12);border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.5);padding:10px;}
  .rp.open .rp-panel{display:flex;}
  .rp-search{width:100%;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);color:#fff;font:inherit;margin-bottom:8px;}
  .rp-search:focus{outline:none;border-color:#3b82f6;}
  .rp-list{overflow-y:auto;padding-right:4px;}
  .rp-head{padding:8px 6px 4px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#9ca3af;}
  .rp-item{width:100%;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 10px;border:0;border-radius:10px;background:transparent;color:#fff;cursor:pointer;text-align:left;font:inherit;}
  .rp-item:hover{background:rgba(255,255,255,.06);}
  .rp-item.sel{background:rgba(59,130,246,.18);}
  .rp-so{display:block;font-size:14px;}
  .rp-en{display:block;font-size:12px;color:#9ca3af;}
  .rp-lvl{font-size:11px;padding:4px 8px;border-radius:999px;white-space:nowrap;}
  .rp-sub{font-size:12px;color:#9ca3af;}
  .rp-empty{padding:24px;text-align:center;font-size:13px;color:#9ca3af;}
  `;

  const esc = v => String(v == null ? '' : v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);

  let ranksPromise = null;
  let cacheList = [];

  function loadRanks() {
    if (!ranksPromise) {
      const base = window.MIGRASL_API_URL || 'http://127.0.0.1:8000';
      const token = localStorage.getItem('access_token') || '';
      ranksPromise = fetch(base + '/ranks/', { headers: { Authorization: 'Bearer ' + token } })
        .then(r => {
          if (!r.ok) throw new Error('Darajooyinka lama soo akhrin karo (' + r.status + ')');
          return r.json();
        })
        .then(d => { cacheList = d.ranks || []; return cacheList; })
        .catch(err => { ranksPromise = null; throw err; });
    }
    return ranksPromise;
  }

  function injectCss() {
    if (document.getElementById('rp-style')) return;
    const s = document.createElement('style');
    s.id = 'rp-style';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function mount(containerId, opts) {
    opts = opts || {};
    const box = typeof containerId === 'string' ? document.getElementById(containerId) : containerId;
    if (!box) throw new Error('RankPicker: container lama helin: ' + containerId);
    injectCss();

    box.innerHTML = `
      <div class="rp">
        <input type="hidden" class="rp-value" value="" />
        <button type="button" class="rp-btn">
          <span class="rp-label"><span class="rp-sub">Dooro darajada...</span></span>
          <i class="fas fa-chevron-down rp-sub"></i>
        </button>
        <div class="rp-panel">
          <input type="text" class="rp-search" placeholder="Raadi darajo (Af-Soomaali ama Ingiriis)..." autocomplete="off" />
          <div class="rp-list"></div>
        </div>
      </div>`;

    const root = box.querySelector('.rp');
    const hidden = root.querySelector('.rp-value');
    const btn = root.querySelector('.rp-btn');
    const label = root.querySelector('.rp-label');
    const search = root.querySelector('.rp-search');
    const list = root.querySelector('.rp-list');
    let ranks = [];
    let current = null;

    function show(code, emit) {
      current = ranks.find(r => r.code === code) || null;
      hidden.value = current ? current.code : '';
      label.innerHTML = current
        ? `<span style="color:#fff">${esc(current.so)}</span> <span class="rp-sub">· ${esc(current.en)}</span>`
        : '<span class="rp-sub">Dooro darajada...</span>';
      if (emit) {
        hidden.dispatchEvent(new Event('change', { bubbles: true }));
        if (opts.onChange) opts.onChange(current);
      }
    }

    function render() {
      const q = search.value.trim().toLowerCase();
      const byGroup = {};
      ranks.forEach(r => {
        const hay = (r.so + ' ' + r.en + ' ' + r.group_so + ' ' + r.level).toLowerCase();
        if (q && hay.indexOf(q) === -1) return;
        (byGroup[r.group] = byGroup[r.group] || []).push(r);
      });
      const html = ORDER.filter(g => byGroup[g]).map(g => `
        <div class="rp-head">${esc(byGroup[g][0].group_so)}</div>
        ${byGroup[g].map(r => `
          <button type="button" class="rp-item${current && current.code === r.code ? ' sel' : ''}" data-code="${esc(r.code)}">
            <span>
              <span class="rp-so">${esc(r.so)}</span>
              <span class="rp-en">${esc(r.en)}</span>
            </span>
            <span class="rp-lvl" style="${GROUP_BADGE[g]}">#${esc(r.level)}</span>
          </button>`).join('')}`).join('');
      list.innerHTML = html || '<div class="rp-empty">Daraja lama helin</div>';
    }

    function open() { root.classList.add('open'); search.focus(); render(); }
    function close() { root.classList.remove('open'); search.value = ''; }

    btn.addEventListener('click', () => (root.classList.contains('open') ? close() : open()));
    search.addEventListener('input', render);
    search.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    list.addEventListener('click', e => {
      const item = e.target.closest('.rp-item');
      if (!item) return;
      show(item.dataset.code, true);
      close();
    });
    document.addEventListener('click', e => { if (!root.contains(e.target)) close(); });

    label.innerHTML = '<span class="rp-sub">Darajooyinka waa la soo raryaa...</span>';
    loadRanks().then(list => {
      ranks = list;
      show(opts.value || '', false);
    }).catch(err => {
      label.innerHTML = `<span style="color:#fca5a5">${esc(err.message)}</span>`;
    });

    return {
      getValue: () => hidden.value,
      getRank: () => current,
      setValue: code => show(code, false),
      reset: () => show('', false)
    };
  }

  window.RankPicker = {
    mount,
    preload: () => loadRanks(),
    byCode: code => cacheList.find(r => r.code === code) || null
  };
})();
