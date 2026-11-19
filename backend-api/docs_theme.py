from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

ACCENT = "#3b82f6"

CSS = """
:root { --bg:#111827; --card:#1f2937; --line:#374151; --text:#e5e7eb; --muted:#9ca3af; --accent:""" + ACCENT + """; }
html, body { background: var(--bg) !important; margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
.mig-head { display:flex; align-items:center; gap:12px; padding:16px 24px; background:var(--card); border-bottom:1px solid var(--line); color:#fff; }
.mig-head b { font-size:18px; }
.mig-head span { color:var(--muted); font-size:13px; }
.mig-dot { width:12px; height:12px; border-radius:50%; background:var(--accent); display:inline-block; }
.swagger-ui { color: var(--text); }
.swagger-ui .wrapper { max-width: 1200px; }
.swagger-ui .info .title, .swagger-ui .info p, .swagger-ui .info li, .swagger-ui .info a,
.swagger-ui .opblock-tag, .swagger-ui .opblock .opblock-summary-path, .swagger-ui .opblock .opblock-summary-description,
.swagger-ui .opblock-description-wrapper p, .swagger-ui .opblock-external-docs-wrapper p,
.swagger-ui .parameter__name, .swagger-ui .parameter__type, .swagger-ui table thead tr th, .swagger-ui table thead tr td,
.swagger-ui .response-col_status, .swagger-ui .response-col_description, .swagger-ui label, .swagger-ui .tab li,
.swagger-ui .model, .swagger-ui .model-title, .swagger-ui section.models h4, .swagger-ui .responses-inner h4,
.swagger-ui .responses-inner h5, .swagger-ui .opblock-section-header h4, .swagger-ui .servers > label { color: var(--text) !important; }
.swagger-ui .info .base-url, .swagger-ui .parameter__in, .swagger-ui .markdown p { color: var(--muted) !important; }
.swagger-ui .prop-type { color:#93c5fd; }
.swagger-ui .scheme-container { background: var(--card); box-shadow:none; border-bottom:1px solid var(--line); }
.swagger-ui .opblock-tag { border-bottom:1px solid var(--line); }
.swagger-ui .opblock { background: rgba(255,255,255,.03); border-radius:10px; }
.swagger-ui .opblock .opblock-section-header { background: var(--card); box-shadow:none; }
.swagger-ui .opblock-body pre.microlight, .swagger-ui .highlight-code pre, .swagger-ui .microlight { background:#0b1220 !important; color:#e5e7eb !important; }
.swagger-ui input, .swagger-ui textarea, .swagger-ui select { background:var(--bg) !important; color:#f9fafb !important; border:1px solid var(--line) !important; }
.swagger-ui .btn { color:#f9fafb; border-color:#4b5563; background:transparent; }
.swagger-ui .btn.execute { background:var(--accent); border-color:var(--accent); color:#fff; }
.swagger-ui .btn.authorize { color:#34d399; border-color:#34d399; }
.swagger-ui .btn.authorize svg { fill:#34d399; }
.swagger-ui svg { fill: var(--muted); }
.swagger-ui section.models { border:1px solid var(--line); border-radius:10px; }
.swagger-ui section.models.is-open h4 { border-bottom:1px solid var(--line); }
.swagger-ui section.models .model-container { background: var(--card); }
.swagger-ui .dialog-ux .modal-ux { background:var(--card); border:1px solid var(--line); color:var(--text); }
.swagger-ui .dialog-ux .modal-ux-header { border-bottom:1px solid var(--line); }
.swagger-ui .dialog-ux .modal-ux-header h3, .swagger-ui .dialog-ux .modal-ux-content h4,
.swagger-ui .dialog-ux .modal-ux-content p { color: var(--text); }
"""

HEADER = '<header class="mig-head"><i class="mig-dot"></i><b>MigraSL</b><span>Somaliland Migration Systems &middot; API</span></header>'


def install_docs(app):
    app.router.routes = [r for r in app.router.routes if getattr(r, "path", None) != "/docs"]

    @app.get("/docs", include_in_schema=False)
    def custom_docs():
        page = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="MigraSL API",
            swagger_ui_parameters={
                "persistAuthorization": True,
                "displayRequestDuration": True,
                "docExpansion": "none",
                "tagsSorter": "alpha",
            },
        )
        html = page.body.decode("utf-8")
        html = html.replace("</head>", "<style>" + CSS + "</style></head>", 1)
        html = html.replace("<body>", "<body>" + HEADER, 1)
        return HTMLResponse(html)