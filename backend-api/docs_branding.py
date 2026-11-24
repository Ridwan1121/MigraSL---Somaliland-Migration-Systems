"""Bogga /docs ee MigraSL: hordhac website-ka + API Explorer (Swagger UI)."""
from fastapi.responses import HTMLResponse

DESCRIPTION = """
**API-ga weji-aqoonsiga ee hay'adda socdaalka Somaliland.**

### Sida loo bilaabo
1. Guji **Authorize**, kadibna geli username iyo password-kaaga.
2. Markaas endpoint kasta wuxuu isticmaalayaa token-kaaga.

### Qaybaha
- **Immigrants**: diiwaangelinta, wax beddelka iyo tirtirka ajaanibta.
- **Weji-aqoonsi**: scan-face, detect-faces, register-face.
- **extras**: dashboard summary iyo sawirrada ajaanibta.
- **offices**: xafiisyada.
- **staff**: askarta iyo maamulayaasha.
- **ranks**: darajooyinka ciidanka Somaliland.

### Doorarka
- **superadmin**: wax walba wuu sameeyaa.
- **admin**: wuxuu maamulaa xafiisyada iyo askarta hoose.
- **officer**: diiwaangelinta iyo weji-aqoonsiga oo keliya.
"""

PAGE = r"""<!DOCTYPE html>
<html lang="so">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>MigraSL API · Dokumentiga</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
<style>
  :root { --bg:#0a0e1a; --panel:#111827; --line:rgba(255,255,255,.08); --text:#e5e7eb; --muted:#9ca3af; --blue:#3b82f6; --violet:#8b5cf6; --gold:#fcd34d; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font-family:'Segoe UI', system-ui, sans-serif; }
  a { color:inherit; text-decoration:none; }
  nav { position:sticky; top:0; z-index:10; display:flex; align-items:center; justify-content:space-between; padding:14px 6%; background:rgba(10,14,26,.9); backdrop-filter:blur(10px); border-bottom:1px solid var(--line); }
  .brand { display:flex; align-items:center; gap:10px; font-weight:800; }
  .brand-mark { width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,var(--blue),var(--violet)); display:grid; place-items:center; }
  nav .links a { margin-left:22px; color:var(--muted); font-size:14px; }
  nav .links a:hover { color:#fff; }
  .hero { padding:72px 6% 56px; display:grid; grid-template-columns:1.2fr 1fr; gap:40px; align-items:center; background:radial-gradient(900px 400px at 85% -10%, rgba(59,130,246,.25), transparent 60%), radial-gradient(700px 400px at -10% 110%, rgba(139,92,246,.2), transparent 60%), var(--bg); }
  .kicker { display:inline-block; padding:6px 12px; border:1px solid var(--line); border-radius:999px; font-size:12px; color:var(--gold); margin-bottom:18px; }
  h1 { font-size:48px; line-height:1.1; margin:0 0 14px; font-weight:800; }
  .lead { color:var(--muted); font-size:17px; line-height:1.6; max-width:560px; margin:0; }
  .shahada { direction:rtl; font-size:24px; color:var(--gold); margin:26px 0 0; padding:14px 18px; border-right:3px solid var(--gold); background:rgba(252,211,77,.06); border-radius:10px; display:inline-block; }
  .status { display:inline-flex; align-items:center; gap:8px; font-size:13px; color:#86efac; margin-top:22px; }
  .status::before { content:''; width:8px; height:8px; border-radius:50%; background:#22c55e; box-shadow:0 0 10px #22c55e; }
  .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:30px; }
  .stat { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:14px 16px; }
  .stat b { display:block; font-size:24px; }
  .stat span { font-size:12px; color:var(--muted); }
  .flag-card { border:1px solid var(--line); border-radius:24px; padding:22px; background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.01)); box-shadow:0 30px 60px rgba(0,0,0,.4); text-align:center; }
  .flag-card svg { width:100%; height:auto; border-radius:10px; box-shadow:0 10px 30px rgba(0,0,0,.4); display:block; }
  .flag-card .cap { margin-top:12px; font-size:13px; color:var(--muted); }
  section { padding:56px 6%; }
  h2 { font-size:28px; margin:0 0 8px; }
  .sub { color:var(--muted); margin:0 0 26px; }
  .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px; }
  .card { background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:18px; }
  .art { height:110px; border-radius:12px; margin-bottom:14px; display:grid; place-items:center; font-size:40px; color:#fff; }
  .art.a1 { background:linear-gradient(135deg,#d62828,#fcd34d); }
  .art.a2 { background:linear-gradient(135deg,#1e3a8a,#0f766e); }
  .art.a3 { background:linear-gradient(135deg,#007a3d,#0ea5e9); }
  .art.a4 { background:linear-gradient(135deg,#7c2d12,#d97706); }
  .art.a5 { background:linear-gradient(135deg,#312e81,#be185d); }
  .card h3 { margin:0 0 6px; font-size:17px; }
  .card p { margin:0; color:var(--muted); font-size:14px; line-height:1.55; }
  .band { background:rgba(255,255,255,.02); border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
  .grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
  .mini { background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:20px; }
  .mini h3 { margin:0 0 10px; font-size:16px; color:var(--gold); }
  .mini ol, .mini ul { margin:0; padding-left:18px; }
  .mini li { margin-bottom:8px; color:var(--muted); font-size:14px; line-height:1.5; }
  .explorer { background:#fff; border-radius:18px; padding:8px; color:#111; }
  .explorer .information-container, .explorer .topbar { display:none; }
  footer { padding:28px 6%; color:var(--muted); font-size:13px; border-top:1px solid var(--line); display:flex; justify-content:space-between; }
  @media (max-width:900px) {
    .hero { grid-template-columns:1fr; }
    h1 { font-size:36px; }
    .grid3 { grid-template-columns:1fr; }
    .stats { grid-template-columns:repeat(2,1fr); }
    nav .links a { display:none; }
  }
</style>
</head>
<body>

<nav>
  <div class="brand"><div class="brand-mark"><i class="fas fa-id-card"></i></div><div>MigraSL</div></div>
  <div class="links">
    <a href="#hordhac">Hordhac</a>
    <a href="#goobaha">Goobaha</a>
    <a href="#qaybaha">Qaybaha</a>
    <a href="#explorer">API Explorer</a>
    <a href="http://127.0.0.1:5500/index.html">Dashboard</a>
  </div>
</nav>

<header class="hero" id="hordhac">
  <div>
    <span class="kicker">Somaliland Migration Systems</span>
    <h1>MigraSL API</h1>
    <p class="lead">API-ga weji-aqoonsiga ee hay'adda socdaalka Somaliland: diiwaangelinta ajaanibta, weji-aqoonsiga, xafiisyada iyo maamulka askarta.</p>
    <div class="shahada">لَا إِلٰهَ إِلَّا الله مُحَمَّدٌ رَسُولُ الله</div>
    <div class="status" id="apiStatus">API: shaqeynaya</div>
    <div class="stats">
      <div class="stat"><b id="sEndpoints">–</b><span>Endpoints</span></div>
      <div class="stat"><b id="sTags">–</b><span>Qaybaha</span></div>
      <div class="stat"><b id="sSchemas">–</b><span>Schemas</span></div>
      <div class="stat"><b id="sVersion">–</b><span>Nooca API</span></div>
    </div>
  </div>
  <div class="flag-card">
    <svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Calanka Somaliland">
      <rect width="900" height="200" fill="#d62828"/>
      <rect y="200" width="900" height="200" fill="#ffffff"/>
      <rect y="400" width="900" height="200" fill="#007a3d"/>
      <polygon points="0,0 300,300 0,600" fill="#000000"/>
      <path d="M120,240 L134.11,280.58 L177.07,281.46 L142.83,307.42 L155.27,348.54 L120,324 L84.73,348.54 L97.17,307.42 L62.93,281.46 L105.89,280.58 Z" fill="#ffffff"/>
    </svg>
    <div class="cap">Calanka Jamhuuriyadda Somaliland</div>
  </div>
</header>

<section id="goobaha" class="band">
  <h2>Goobaha & Magaalooyinka</h2>
  <p class="sub">Xarunta dhexe ee Caasimadda Hargeysa, iyo magaalooyinka muhiimka ah.</p>
  <div class="cards">
    <div class="card">
      <div class="art a1"><i class="fas fa-city"></i></div>
      <h3>Hargeysa: Caasimadda</h3>
      <p>Xarunta dhexe ee Jamhuuriyadda Somaliland, oo ku taal Gobolka Maroodi Jeeh.</p>
    </div>
    <div class="card">
      <div class="art a2"><i class="fas fa-mountain"></i></div>
      <h3>Laas Geel</h3>
      <p>Goob taariikhi ah oo leh farshaxanka dhagaxa ee hore u dhaqanka, ku dhow Hargeysa.</p>
    </div>
    <div class="card">
      <div class="art a3"><i class="fas fa-anchor"></i></div>
      <h3>Berbera</h3>
      <p>Dekedda badda ee ugu weyn, oo muhiim u ah ganacsiga iyo socdaalka.</p>
    </div>
    <div class="card">
      <div class="art a4"><i class="fas fa-landmark"></i></div>
      <h3>Burco</h3>
      <p>Magaalo ku taal Gobolka Togdheer.</p>
    </div>
    <div class="card">
      <div class="art a5"><i class="fas fa-map-location-dot"></i></div>
      <h3>Boorama</h3>
      <p>Magaalo ku taal Gobolka Awdal.</p>
    </div>
  </div>
</section>

<section id="qaybaha">
  <h2>Bilowga & Doorarka</h2>
  <p class="sub">Sida loo bilaabo, qaybaha API-ga, iyo doorarka isticmaalayaasha.</p>
  <div class="grid3">
    <div class="mini">
      <h3>Sida loo bilaabo</h3>
      <ol>
        <li>Guji <b>Authorize</b>, kadibna geli username iyo password-kaaga.</li>
        <li>Markaas endpoint kasta wuxuu isticmaalayaa token-kaaga.</li>
      </ol>
    </div>
    <div class="mini">
      <h3>Qaybaha</h3>
      <ul>
        <li><b>Immigrants</b>: diiwaangelinta, wax beddelka, tirtirka.</li>
        <li><b>Weji-aqoonsi</b>: scan-face, detect-faces, register-face.</li>
        <li><b>extras</b>: dashboard summary iyo sawirrada.</li>
        <li><b>offices</b>: xafiisyada. <b>staff</b>: askarta.</li>
        <li><b>ranks</b>: darajooyinka ciidanka.</li>
      </ul>
    </div>
    <div class="mini">
      <h3>Doorarka</h3>
      <ul>
        <li><b>superadmin</b>: wax walba wuu sameeyaa.</li>
        <li><b>admin</b>: xafiisyada iyo askarta hoose.</li>
        <li><b>officer</b>: diiwaangelinta iyo weji-aqoonsiga oo keliya.</li>
      </ul>
    </div>
  </div>
</section>

<section id="explorer" class="band">
  <h2>API Explorer</h2>
  <p class="sub">Endpoint kasta ku tijaabi. Marka hore Authorize ku samee.</p>
  <div class="explorer"><div id="swagger-ui"></div></div>
</section>

<footer>
  <span>© MigraSL · Somaliland Migration Systems</span>
  <span>OpenAPI 3.1</span>
</footer>

<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
(function () {
  fetch('/openapi.json').then(r => r.json()).then(spec => {
    const paths = Object.values(spec.paths || {});
    const methods = ['get', 'post', 'put', 'delete', 'patch'];
    let ops = 0;
    const tags = new Set();
    paths.forEach(p => {
      Object.keys(p).filter(k => methods.includes(k)).forEach(k => {
        ops += 1;
        (p[k].tags || []).forEach(t => tags.add(t));
      });
    });
    document.getElementById('sEndpoints').textContent = ops;
    document.getElementById('sTags').textContent = tags.size;
    document.getElementById('sSchemas').textContent = Object.keys((spec.components && spec.components.schemas) || {}).length;
    document.getElementById('sVersion').textContent = spec.info.version;
  }).catch(() => {
    document.getElementById('apiStatus').textContent = 'API: ma xiriiri karo';
  });

  window.ui = SwaggerUIBundle({
    url: '/openapi.json',
    dom_id: '#swagger-ui',
    deepLinking: true,
    persistAuthorization: true,
    docExpansion: 'list',
    defaultModelsExpandDepth: -1
  });
})();
</script>
</body>
</html>
"""


def swagger_docs_response(openapi_url: str = "/openapi.json") -> HTMLResponse:
    return HTMLResponse(PAGE)
