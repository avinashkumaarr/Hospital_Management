import urllib.request

endpoints = [
    '/',
    '/static/css/styles.css',
    '/static/js/api.js',
    '/static/js/app.js',
    '/api/health',
    '/api/auth/roles',
    '/api/analytics/dashboard?hospital_id=1'
]

for ep in endpoints:
    url = f'http://127.0.0.1:8000{ep}'
    try:
        req = urllib.request.urlopen(url)
        print(f'{ep} -> HTTP {req.status} (Length: {len(req.read())})')
    except Exception as e:
        print(f'{ep} -> FAILED: {e}')
