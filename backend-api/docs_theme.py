"""MigraSL API docs (/docs): Swagger UI oo leh muuqaal dashboard-ka u eg.

Isticmaal: app.py gudihiisa ku dar `docs_url=None` FastAPI(...) iyo
    from docs_theme import install_docs
    install_docs(app)
"""

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

# NB: CSS iyo JS waa raw strings (r"""...""") si aysan u jirin qalad f-string / backslash.

MIGRASL_DOCS_CSS = r"""
:root, html[data-theme="light"] {
  --bg:#f4f6f9; --card:#ffffff; --elev:#eef2f7; --line:#dbe2ea;
  --text:#111827; --muted:#5b6678; --accent:#059669; --accent2:#0284c7;
  --shadow:0 4px 14px rgba(15,23,42,.07);
}
html[data-theme="dark"] {
  --bg:#070d19; --card:#0f172a; --elev:#162033; --line:rgba(148,163,184,.18);
  --text:#f1f5f9; --muted:#94a3b8; --accent:#10b981; --accent2:#06b6d4;
  --shadow:0 8px 24px rgba(0,0,0,.35);
}
html, body { margin:0; background:var(--bg) !important; color:var(--text);
  font-family:'Segoe UI', system-ui, -apple-system, Roboto, sans-serif; }
.swagger-ui .topbar { display:none !important; }

/* ---------- Header ---------- */
.mig-flagbar { height:5px; background:linear-gradient(90deg,#006d21 0 33.3%,#fff 33.3% 66.6%,#d21034 66.6%); }
.mig-head { position:sticky; top:0; z-index:999; display:flex; flex-wrap:wrap; gap:12px;
  align-items:center; justify-content:space-between; padding:12px 24px;
  background:var(--card); border-bottom:1px solid var(--line); box-shadow:var(--shadow); }
.mig-brand { display:flex; align-items:center; gap:12px; }
.mig-logo { width:40px; height:40px; border-radius:11px; display:grid; place-items:center;
  font-weight:800; color:#fff; background:linear-gradient(135deg,var(--accent),var(--accent2)); }
.mig-brand h1 { margin:0; font-size:16px; font-weight:700; color:var(--text); }
.mig-brand p { margin:2px 0 0; font-size:12px; color:var(--muted); }
.mig-tools { display:flex; flex-wrap:wrap; gap:10px; align-items:center; }
.mig-input { background:var(--elev); border:1px solid var(--line); color:var(--text);
  border-radius:10px; padding:8px 12px; font-size:13px; min-width:230px; outline:none; }
.mig-input:focus { border-color:var(--accent); box-shadow:0 0 0 3px rgba(16,185,129,.18); }
.mig-btn { cursor:pointer; text-decoration:none; font-size:12.5px; font-weight:600; color:var(--text);
  background:var(--elev); border:1px solid var(--line); padding:8px 12px; border-radius:10px; }
.mig-btn:hover { border-color:var(--accent2); }
.mig-pill { font-size:12px; font-weight:600; padding:6px 11px; border-radius:999px;
  border:1px solid var(--line); background:var(--elev); color:var(--muted); }
.mig-pill.ok { color:#059669; border-color:rgba(16,185,129,.5); background:rgba(16,185,129,.1); }
.mig-pill.bad { color:#e11d48; border-color:rgba(225,29,72,.5); background:rgba(225,29,72,.1); }

/* ---------- Stat cards + filters ---------- */
.mig-wrap { max-width:1280px; margin:0 auto; padding:22px 24px 0; }
.mig-stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:14px; }
.mig-stat { background:var(--card); border:1px solid var(--line); border-radius:14px;
  padding:16px 18px; box-shadow:var(--shadow); border-top:3px solid var(--accent); }
.mig-stat:nth-child(2n) { border-top-color:var(--accent2); }
.mig-stat span { display:block; font-size:12px; color:var(--muted); }
.mig-stat b { display:block; margin-top:4px; font-size:28px; line-height:1.1; color:var(--text); }
.mig-filters { display:flex; flex-wrap:wrap; gap:8px; margin:16px 0 0; align-items:center; }
.mig-filters small { color:var(--muted); margin-right:4px; }
.mig-chip { cursor:pointer; user-select:none; font-size:12px; font-weight:700; padding:6px 12px;
  border-radius:999px; border:1px solid var(--line); background:var(--card); color:var(--text); }
.mig-chip.off { opacity:.4; text-decoration:line-through; }

/* ---------- Swagger layout ---------- */
.swagger-ui .wrapper { max-width:1280px !important; padding:10px 24px 60px !important; }
.swagger-ui .info { margin:18px 0 18px !important; background:var(--card); border:1px solid var(--line);
  border-radius:16px; padding:20px 24px; box-shadow:var(--shadow); }
.swagger-ui .scheme-container { background:var(--card) !important; border:1px solid var(--line);
  border-radius:14px; box-shadow:none !important; padding:14px 20px !important; }
.swagger-ui .opblock-tag { background:var(--card); border:1px solid var(--line) !important;
  border-radius:12px; margin:14px 0 8px !important; padding:10px 16px !important; }
.swagger-ui .opblock { border-radius:12px !important; box-shadow:none !important; margin:0 0 10px !important; }
.swagger-ui .btn.authorize { color:#fff !important; border:none !important; border-radius:10px;
  background:linear-gradient(135deg,var(--accent),var(--accent2)) !important; }
.swagger-ui .btn.authorize svg { fill:#fff !important; }
.swagger-ui section.models { background:var(--card); border:1px solid var(--line); border-radius:16px; }

/* ---------- Dark overrides ---------- */
html[data-theme="dark"] .swagger-ui, html[data-theme="dark"] .swagger-ui .info .title,
html[data-theme="dark"] .swagger-ui .info p, html[data-theme="dark"] .swagger-ui .info li,
html[data-theme="dark"] .swagger-ui .info a, html[data-theme="dark"] .swagger-ui .opblock-tag,
html[data-theme="dark"] .swagger-ui .opblock .opblock-summary-path,
html[data-theme="dark"] .swagger-ui .opblock .opblock-summary-description,
html[data-theme="dark"] .swagger-ui .opblock-description-wrapper p,
html[data-theme="dark"] .swagger-ui .parameter__name, html[data-theme="dark"] .swagger-ui .parameter__type,
html[data-theme="dark"] .swagger-ui table thead tr th, html[data-theme="dark"] .swagger-ui table thead tr td,
html[data-theme="dark"] .swagger-ui .response-col_status, html[data-theme="dark"] .swagger-ui .response-col_description,
html[data-theme="dark"] .swagger-ui label, html[data-theme="dark"] .swagger-ui .tab li,
html[data-theme="dark"] .swagger-ui .model, html[data-theme="dark"] .swagger-ui .model-title,
html[data-theme="dark"] .swagger-ui section.models h4, html[data-theme="dark"] .swagger-ui .responses-inner h4,
html[data-theme="dark"] .swagger-ui .responses-inner h5, html[data-theme="dark"] .swagger-ui .opblock-section-header h4,
html[data-theme="dark"] .swagger-ui .opblock-section-header label,
html[data-theme="dark"] .swagger-ui .servers > label, html[data-theme="dark"] .swagger-ui .markdown p,
html[data-theme="dark"] .swagger-ui .renderedMarkdown p { color:var(--text) !important; }
html[data-theme="dark"] .swagger-ui .info .base-url, html[data-theme="dark"] .swagger-ui .parameter__in,
html[data-theme="dark"] .swagger-ui .prop-type { color:var(--muted) !important; }
html[data-theme="dark"] .swagger-ui .opblock .opblock-section-header { background:var(--elev); box-shadow:none; }
html[data-theme="dark"] .swagger-ui .opblock.opblock-get { background:rgba(14,165,233,.08); border-color:rgba(14,165,233,.4); }
html[data-theme="dark"] .swagger-ui .opblock.opblock-post { background:rgba(16,185,129,.08); border-color:rgba(16,185,129,.4); }
html[data-theme="dark"] .swagger-ui .opblock.opblock-put { background:rgba(245,158,11,.08); border-color:rgba(245,158,11,.4); }
html[data-theme="dark"] .swagger-ui .opblock.opblock-delete { background:rgba(244,63,94,.08); border-color:rgba(244,63,94,.4); }
html[data-theme="dark"] .swagger-ui input, html[data-theme="dark"] .swagger-ui textarea,
html[data-theme="dark"] .swagger-ui select { background:var(--bg) !important; color:var(--text) !important;
  border:1px solid var(--line) !important; }
html[data-theme="dark"] .swagger-ui .microlight, html[data-theme="dark"] .swagger-ui .highlight-code pre,
html[data-theme="dark"] .swagger-ui .opblock-body pre.microlight { background:#0b1220 !important; color:#e5e7eb !important; }
html[data-theme="dark"] .swagger-ui .btn { color:var(--text); border-color:var(--line); background:transparent; }
html[data-theme="dark"] .swagger-ui .btn.execute { background:var(--accent); border-color:var(--accent); color:#fff; }
html[data-theme="dark"] .swagger-ui svg:not(.locked):not(.unlocked) { fill:var(--muted); }
html[data-theme="dark"] .swagger-ui .model-box, html[data-theme="dark"] .swagger-ui section.models .model-container { background:var(--elev); }
html[data-theme="dark"] .swagger-ui .dialog-ux .modal-ux { background:var(--card); border:1px solid var(--line); color:var(--text); }
html[data-theme="dark"] .swagger-ui .dialog-ux .modal-ux-header h3,
html[data-theme="dark"] .swagger-ui .dialog-ux .modal-ux-content h4,
html[data-theme="dark"] .swagger-ui .dialog-ux .modal-ux-content p { color:var(--text) !important; }
"""

MIGRASL_DOCS_JS = r"""
(function () {
  var THEME_KEY = 'migrasl_docs_theme';

  function getTheme() {
    try { return localStorage.getItem(THEME_KEY) || 'dark'; } catch (e) { return 'dark'; }
  }
  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
    var b = document.getElementById('migThemeBtn');
    if (b) b.textContent = t === 'dark' ? 'Iftiin' : 'Mugdi';
  }
  setTheme(getTheme());

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }

  function buildHeader() {
    var bar = el('div', 'mig-flagbar');
    var head = el('header', 'mig-head');
    head.id = 'migHeader';
    head.innerHTML =
      '<div class="mig-brand"><div class="mig-logo">MS</div><div>' +
      '<h1>MigraSL &middot; Somaliland Migration Systems</h1>' +
      '<p>API Explorer &middot; Weji-aqoonsi, Diiwaan, Xafiisyo &amp; Askar</p></div></div>' +
      '<div class="mig-tools">' +
      '<span id="migHealth" class="mig-pill">API: hubinaya...</span>' +
      '<input id="migSearch" class="mig-input" type="search" placeholder="Raadi endpoint (/staff, /scan-face)...">' +
      '<a class="mig-btn" href="http://127.0.0.1:5500/index.html" target="_blank" rel="noopener">Dashboard</a>' +
      '<a class="mig-btn" href="/openapi.json" target="_blank" rel="noopener">OpenAPI JSON</a>' +
      '<button id="migThemeBtn" class="mig-btn" type="button"></button></div>';
    document.body.prepend(head);
    document.body.prepend(bar);
    document.getElementById('migThemeBtn').addEventListener('click', function () {
      setTheme(getTheme() === 'dark' ? 'light' : 'dark');
    });
    setTheme(getTheme());
    document.getElementById('migSearch').addEventListener('input', applyFilters);
  }

  var hidden = {};  // method -> true marka la qariyay

  function applyFilters() {
    var q = (document.getElementById('migSearch').value || '').trim().toLowerCase();
    document.querySelectorAll('.opblock-tag-section').forEach(function (sec) {
      var any = false;
      sec.querySelectorAll('.opblock').forEach(function (blk) {
        var m = (blk.querySelector('.opblock-summary-method') || {}).textContent || '';
        var okMethod = !hidden[m.trim().toUpperCase()];
        var okText = !q || blk.textContent.toLowerCase().indexOf(q) !== -1;
        var show = okMethod && okText;
        blk.style.display = show ? '' : 'none';
        if (show) any = true;
      });
      sec.style.display = any ? '' : 'none';
    });
  }

  function buildStats(spec) {
    var paths = spec.paths || {}, endpoints = 0, methods = {}, tags = {};
    Object.keys(paths).forEach(function (p) {
      Object.keys(paths[p]).forEach(function (m) {
        if (['get', 'post', 'put', 'delete', 'patch'].indexOf(m) === -1) return;
        endpoints++;
        methods[m.toUpperCase()] = (methods[m.toUpperCase()] || 0) + 1;
        (paths[p][m].tags || ['default']).forEach(function (t) { tags[t] = true; });
      });
    });
    var schemas = Object.keys((spec.components || {}).schemas || {}).length;
    var wrap = el('div', 'mig-wrap');
    wrap.id = 'migStatsWrap';
    var stats = el('div', 'mig-stats');
    [['Endpoints', endpoints], ['Qaybaha (tags)', Object.keys(tags).length],
     ['Schemas', schemas], ['Nooca API', (spec.info || {}).version || '-'],
     ['OpenAPI', spec.openapi || '-']].forEach(function (s) {
      stats.appendChild(el('div', 'mig-stat', '<span>' + s[0] + '</span><b>' + s[1] + '</b>'));
    });
    wrap.appendChild(stats);
    var f = el('div', 'mig-filters', '<small>Shaandhee:</small>');
    Object.keys(methods).sort().forEach(function (m) {
      var c = el('span', 'mig-chip', m + ' &middot; ' + methods[m]);
      c.addEventListener('click', function () {
        hidden[m] = !hidden[m];
        c.classList.toggle('off', !!hidden[m]);
        applyFilters();
      });
      f.appendChild(c);
    });
    wrap.appendChild(f);
    var host = document.querySelector('#swagger-ui');
    host.parentNode.insertBefore(wrap, host);
  }

  function checkHealth() {
    var p = document.getElementById('migHealth');
    fetch('/health').then(function (r) {
      p.textContent = r.ok ? 'API: shaqeynaya' : 'API: khalad ' + r.status;
      p.className = 'mig-pill ' + (r.ok ? 'ok' : 'bad');
    }).catch(function () { p.textContent = 'API: ma shaqeynayo'; p.className = 'mig-pill bad'; });
  }

  function init() {
    if (document.getElementById('migHeader')) return;
    buildHeader();
    checkHealth();
    setInterval(checkHealth, 30000);
    fetch('/openapi.json').then(function (r) { return r.json(); }).then(buildStats).catch(function () {});
    // Swagger wuu dib u rendheeyaa marka tag la furo -> dib u shaandhee
    new MutationObserver(function () {
      if (Object.keys(hidden).some(function (k) { return hidden[k]; }) ||
          (document.getElementById('migSearch').value || '')) applyFilters();
    }).observe(document.getElementById('swagger-ui'), { childList: true, subtree: true });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
"""


def install_docs(app):
    # Ka saar /docs caadiga ah haddii uu jiro (docs_url=None ayaa sidoo kale loo baahan yahay)
    app.router.routes = [r for r in app.router.routes if getattr(r, "path", None) != "/docs"]

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_docs():
        page = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="MigraSL API Docs",
            swagger_ui_parameters={
                "persistAuthorization": True,
                "displayRequestDuration": True,
                "docExpansion": "none",
                "tagsSorter": "alpha",
            },
        )
        html = page.body.decode("utf-8")
        inject = "<style>" + MIGRASL_DOCS_CSS + "</style>"
        html = html.replace("</head>", inject + "</head>", 1)
        html = html.replace("</body>", "<script>" + MIGRASL_DOCS_JS + "</script></body>", 1)
        return HTMLResponse(content=html, status_code=200)
