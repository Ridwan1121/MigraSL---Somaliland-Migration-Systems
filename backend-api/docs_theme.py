from fastapi import FastAPI
from fastapi.responses import HTMLResponse

MIGRASL_DOCS_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>__APP_TITLE__ · MigraSL API Docs</title>
  <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
  <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />

  <style>
    :root,
    html[data-theme="dark"] {
      --bg-main: #070d19;
      --bg-card: #0f172a;
      --bg-elevated: #162033;
      --bg-input: #0b1324;
      --border-subtle: rgba(148, 163, 184, 0.18);
      --text-primary: #f8fafc;
      --text-secondary: #e2e8f0;
      --text-muted: #94a3b8;
      --header-bg: rgba(11, 18, 34, 0.92);
      --accent-emerald: #10b981;
      --accent-cyan: #06b6d4;
      --glow-emerald: rgba(16, 185, 129, 0.10);
      --glow-cyan: rgba(6, 182, 212, 0.10);
    }

    html[data-theme="light"] {
      --bg-main: #f4f7fb;
      --bg-card: #ffffff;
      --bg-elevated: #eef2f7;
      --bg-input: #f8fafc;
      --border-subtle: rgba(15, 23, 42, 0.14);
      --text-primary: #0f172a;
      --text-secondary: #1e293b;
      --text-muted: #475569;
      --header-bg: rgba(255, 255, 255, 0.92);
      --accent-emerald: #059669;
      --accent-cyan: #0284c7;
      --glow-emerald: rgba(16, 185, 129, 0.08);
      --glow-cyan: rgba(2, 132, 199, 0.08);
    }

    html, body {
      margin: 0;
      min-height: 100%;
      background:
        radial-gradient(circle at top right, var(--glow-emerald), transparent 36%),
        radial-gradient(circle at top left, var(--glow-cyan), transparent 36%),
        var(--bg-main);
      color: var(--text-primary);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      transition: background-color 0.2s ease, color 0.2s ease;
    }

    code, pre, .microlight, .opblock-summary-path, .model-title, input[type="text"], textarea, select {
      font-family: 'JetBrains Mono', monospace !important;
    }

    .swagger-ui .topbar { display: none !important; }

    .migrasl-header {
      position: sticky;
      top: 0;
      z-index: 999;
      backdrop-filter: blur(14px);
      background: var(--header-bg);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .migrasl-brand { display: flex; align-items: center; gap: 12px; }

    .migrasl-logo {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #ffffff;
      font-size: 15px;
      box-shadow: 0 8px 20px rgba(16, 185, 129, 0.22);
    }

    .migrasl-title { margin: 0; font-size: 16px; font-weight: 700; color: var(--text-primary); }
    .migrasl-subtitle { margin: 2px 0 0; font-size: 12px; color: var(--text-muted); }

    .migrasl-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; }

    .migrasl-btn,
    .migrasl-theme-btn {
      cursor: pointer;
      text-decoration: none;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      padding: 8px 13px;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: border-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
    }

    .migrasl-btn:hover,
    .migrasl-theme-btn:hover { border-color: var(--accent-cyan); color: var(--text-primary); }
    .migrasl-theme-btn:active { transform: scale(0.98); }

    .swagger-ui .wrapper { max-width: 1280px !important; padding: 20px 24px 64px !important; }

    .swagger-ui .info,
    .swagger-ui .scheme-container,
    .swagger-ui .opblock-tag,
    .swagger-ui section.models,
    .swagger-ui .model-box {
      background: var(--bg-card) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 14px !important;
      box-shadow: none !important;
    }

    .swagger-ui .info { padding: 22px 24px !important; margin: 16px 0 22px !important; }
    .swagger-ui .info .title { color: var(--text-primary) !important; font-size: 26px !important; font-weight: 800 !important; }

    .swagger-ui .info p,
    .swagger-ui .info li,
    .swagger-ui .info .base-url,
    .swagger-ui .parameter__type,
    .swagger-ui .opblock-tag small { color: var(--text-muted) !important; }

    .swagger-ui .opblock-tag,
    .swagger-ui .opblock-summary-path,
    .swagger-ui .opblock-summary-description,
    .swagger-ui .opblock-section-header h4,
    .swagger-ui table thead tr th,
    .swagger-ui .parameter__name,
    .swagger-ui .response-col_status,
    .swagger-ui .response-col_description,
    .swagger-ui .model-title,
    .swagger-ui .prop-name { color: var(--text-secondary) !important; }

    .swagger-ui .opblock { border-radius: 12px !important; margin: 0 0 10px !important; box-shadow: none !important; }
    .swagger-ui .opblock.opblock-get { background: rgba(14, 165, 233, 0.08) !important; border-color: rgba(14, 165, 233, 0.35) !important; }
    .swagger-ui .opblock.opblock-post { background: rgba(16, 185, 129, 0.08) !important; border-color: rgba(16, 185, 129, 0.35) !important; }
    .swagger-ui .opblock.opblock-put { background: rgba(245, 158, 11, 0.08) !important; border-color: rgba(245, 158, 11, 0.35) !important; }
    .swagger-ui .opblock.opblock-delete { background: rgba(244, 63, 94, 0.08) !important; border-color: rgba(244, 63, 94, 0.35) !important; }

    .swagger-ui input[type="text"],
    .swagger-ui input[type="password"],
    .swagger-ui input[type="search"],
    .swagger-ui textarea,
    .swagger-ui select {
      background: var(--bg-input) !important;
      color: var(--text-primary) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 8px !important;
    }

    .swagger-ui .highlight-code pre,
    .swagger-ui .microlight {
      background: var(--bg-input) !important;
      color: var(--text-primary) !important;
      border: 1px solid var(--border-subtle) !important;
      border-radius: 10px !important;
    }

    .swagger-ui .btn.authorize {
      background: linear-gradient(135deg, var(--accent-emerald), #059669) !important;
      color: #ffffff !important;
      border: none !important;
      border-radius: 10px !important;
      font-weight: 600 !important;
    }

    .swagger-ui .btn.execute {
      background: linear-gradient(135deg, var(--accent-cyan), #0284c7) !important;
      color: #ffffff !important;
      border: none !important;
      border-radius: 8px !important;
      font-weight: 600 !important;
    }

    html[data-theme="light"] .swagger-ui .opblock-body,
    html[data-theme="light"] .swagger-ui .responses-wrapper,
    html[data-theme="light"] .swagger-ui .model-box { background: #ffffff !important; }
  </style>
</head>
<body>
  <header class="migrasl-header">
    <div class="migrasl-brand">
      <div class="migrasl-logo">MS</div>
      <div>
        <h1 class="migrasl-title">MigraSL · Somaliland Migration Systems</h1>
        <p class="migrasl-subtitle">API Explorer · Biometrics, Registry, Photos, Staff &amp; Offices</p>
      </div>
    </div>
    <div class="migrasl-actions">
      <button id="migraslThemeToggle" class="migrasl-theme-btn" type="button" aria-label="Toggle Light or Dark Theme">
        <span id="migraslThemeIcon">☀️</span>
        <span id="migraslThemeLabel">Light Mode</span>
      </button>
      <a class="migrasl-btn" href="/openapi.json" target="_blank" rel="noopener">OpenAPI JSON</a>
      <a class="migrasl-btn" href="/redoc" target="_blank" rel="noopener">ReDoc</a>
    </div>
  </header>

  <div id="swagger-ui"></div>

  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    (function () {
      const STORAGE_KEY = "migrasl_docs_theme";
      const root = document.documentElement;
      const btn = document.getElementById("migraslThemeToggle");
      const icon = document.getElementById("migraslThemeIcon");
      const label = document.getElementById("migraslThemeLabel");

      function applyTheme(theme) {
        const nextTheme = theme === "light" ? "light" : "dark";
        root.setAttribute("data-theme", nextTheme);
        try {
          localStorage.setItem(STORAGE_KEY, nextTheme);
        } catch (_) {}

        if (nextTheme === "light") {
          icon.textContent = "🌙";
          label.textContent = "Dark Mode";
        } else {
          icon.textContent = "☀️";
          label.textContent = "Light Mode";
        }
      }

      let savedTheme = "dark";
      try {
        savedTheme = localStorage.getItem(STORAGE_KEY) || "dark";
      } catch (_) {}
      applyTheme(savedTheme);

      btn.addEventListener("click", function () {
        const current = root.getAttribute("data-theme");
        applyTheme(current === "dark" ? "light" : "dark");
      });
    })();

    const ui = SwaggerUIBundle({
      url: "/openapi.json",
      dom_id: "#swagger-ui",
      layout: "BaseLayout",
      deepLinking: true,
      filter: true,
      docExpansion: "list",
      persistAuthorization: true,
      tryItOutEnabled: true,
      showExtensions: true,
      showCommonExtensions: true,
      oauth2RedirectUrl: window.location.origin + "/docs/oauth2-redirect",
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ]
    });
  </script>
</body>
</html>
"""


def install_docs(app: FastAPI) -> None:
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_docs() -> HTMLResponse:
        rendered_html = MIGRASL_DOCS_HTML.replace("__APP_TITLE__", app.title or "MigraSL API")
        return HTMLResponse(content=rendered_html, status_code=200)
