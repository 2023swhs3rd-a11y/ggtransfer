# 사용: cd src && python3 build.py  → ../index.html(GitHub Pages)와 ../artifact.html(Claude 페이지 본문) 생성
import base64, io, json, string, subprocess, sys
subprocess.run([sys.executable, 'parse.py'], check=True)
t = open('template.html').read()
data, mp = open('data.json').read(), open('map.json').read()
from fontTools import subset
from fontTools.ttLib import TTFont
chars = set(t) | set(data) | set(string.printable) | set('년개월명곳%~·…–—○●÷×')
opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']
font = TTFont('fonts/PretendardVariable.woff2')
s = subset.Subsetter(opts); s.populate(text=''.join(c for c in chars if ord(c) >= 32)); s.subset(font)
buf = io.BytesIO(); font.flavor = 'woff2'; font.save(buf)
body = t.replace('__FONT__', base64.b64encode(buf.getvalue()).decode()).replace('__DATA__', data).replace('__MAP__', mp)
open('../artifact.html', 'w').write(body)
import urllib.parse
fav = urllib.parse.quote(open('favicon.svg').read().strip(), safe=' =:/')
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{fav}">\n'
        '<style>:root{color-scheme:light}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
open('../index.html', 'w').write(head + body + '\n</body>\n</html>\n')
print('font subset', len(buf.getvalue()), 'bytes; index.html', len(head + body))
