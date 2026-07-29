import base64
import re
import urllib.parse
from pathlib import Path

html_path = Path('index.html')
text = html_path.read_text(encoding='utf-8')
folder = html_path.parent
used = set()

mime_map = {
    '.png': 'image/png',
    '.PNG': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.JPG': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml'
}

def encode(match):
    quote = match.group(1)
    src = match.group(2)
    raw = urllib.parse.unquote(src)
    file_path = folder / raw
    if not file_path.exists():
        return match.group(0)
    ext = file_path.suffix
    mime = mime_map.get(ext, 'application/octet-stream')
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('ascii')
    used.add(file_path.name)
    return f'src={quote}data:{mime};base64,{b64}{quote}'

new_text = re.sub(r"""\bsrc=(['"])([^'"]+)\1""", encode, text)
Path('index_standalone.html').write_text(new_text, encoding='utf-8')
print('Embedded:', used)
