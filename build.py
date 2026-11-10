#!/usr/bin/env python3
"""NOTE: js/config.js is intentionally NOT inlined: edit it, upload it next to index.html, no rebuild needed.
Builds a self-contained index.html (CSS + JS + favicon inlined) from index.template.html.
Run: python3 build.py   (edit css/, js/ or index.template.html, then rebuild)"""
import re,base64,pathlib
r=pathlib.Path(__file__).parent
h=(r/'index.template.html').read_text()
css=(r/'css/styles.css').read_text()
js=(r/'js/data.js').read_text()+'\n'+(r/'js/auth.js').read_text()+'\n'+(r/'js/app.js').read_text()
fav='data:image/svg+xml;base64,'+base64.b64encode((r/'assets/favicon.svg').read_bytes()).decode()
h=h.replace('<link rel="stylesheet" href="css/styles.css">','<style>\n'+css+'\n</style>')
h=h.replace('href="assets/favicon.svg"','href="'+fav+'"')
h=re.sub(r'<script src="js/data.js"></script><script src="js/auth.js"></script><script src="js/app.js"></script>',lambda m:'<script>\n'+js.replace('</script>','<\\/script>')+'\n</script>',h)
(r/'index.html').write_text(h)
print('built index.html',len(h),'bytes')
