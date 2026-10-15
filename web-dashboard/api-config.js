window.MIGRASL_API_URL = window.MIGRASL_API_URL || (
    window.location.protocol === 'file:' ||
    ['localhost', '127.0.0.1'].includes(window.location.hostname)
        ? 'http://127.0.0.1:8000'
        : window.location.origin
);
