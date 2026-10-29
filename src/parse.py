import json,re,sys,glob,os
out={}
R=None
pat=re.compile(r'^(\d+)/(\d+)(?:\((\d+)\.(\d+)\))?$')
bad=[]
for f in sorted(glob.glob('raw/*.json')):
  y=os.path.basename(f)[:4]; rows=json.load(open(f))
  regs=rows[0][1:]
  if R is None: R=regs
  assert regs==R
  recs=[]
  for r in rows[1:]:
    subj=r[0]
    for i,c in enumerate(r[1:]):
      c=c.strip()
      if not c: continue
      m=pat.match(c)
      if not m: bad.append((y,subj,c)); continue
      a,h,yy,mm=m.groups()
      assert int(mm or 0)<12,(y,subj,c)
      recs.append([subj,i,int(a),int(h),None if yy is None else int(yy)*12+int(mm)])
  out[y]=recs
print('bad',bad)
json.dump({'regions':R,'years':out},open('data.json','w'),ensure_ascii=False,separators=(',',':'))
print({k:len(v) for k,v in out.items()}, os.path.getsize('data.json'))
