#!/usr/bin/env python3

from app import app
context = ('ssl.cert', 'ssl.key')
app.run(host='0.0.0.0', port=5001, threaded=True, debug=False, ssl_context=context)
