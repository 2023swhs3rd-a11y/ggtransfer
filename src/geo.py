import json,sys
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
d=json.load(open(sys.argv[1]))
M={'수원':['수원'],'성남':['성남'],'안양':['안양','과천'],'부천':['부천'],'광명':['광명'],'안산':['안산'],'평택':['평택'],'군포':['군포','의왕'],'여주':['여주'],'화성':['화성','오산'],'광주':['광주','하남'],'양평':['양평'],'이천':['이천'],'용인':['용인'],'안성':['안성'],'김포':['김포'],'시흥':['시흥'],'의정부':['의정부'],'동두천':['동두천','양주'],'고양':['고양'],'구리':['구리','남양주'],'파주':['파주'],'연천':['연천'],'포천':['포천'],'가평':['가평']}
gg=[f for f in d['features'] if f['properties']['code'].startswith('31')]
geoms={}
for k,pre in M.items():
  gs=[shape(f['geometry']).buffer(0) for f in gg if any(f['properties']['name'].startswith(p) for p in pre)]
  assert gs,k
  geoms[k]=unary_union(gs).buffer(0.0005).buffer(-0.0005).simplify(0.004)
allu=unary_union(list(geoms.values()))
minx,miny,maxx,maxy=allu.bounds
import math
lat0=(miny+maxy)/2; kx=math.cos(math.radians(lat0))
W=600; s=W/((maxx-minx)*kx); H=(maxy-miny)*s
def pt(x,y): return f"{(x-minx)*kx*s:.1f},{(maxy-y)*s:.1f}"
def ring(c): return 'M'+'L'.join(pt(x,y) for x,y in c)+'Z'
out={}
for k,g in geoms.items():
  polys=[g] if g.geom_type=='Polygon' else list(g.geoms)
  path=''.join(ring(p.exterior.coords)+''.join(ring(i.coords) for i in p.interiors) for p in polys if p.area>1e-5)
  c=g.representative_point() if k not in('수원','성남') else g.centroid
  out[k]={'d':path,'c':[float(pt(c.x,c.y).split(',')[0]),float(pt(c.x,c.y).split(',')[1])]}
json.dump({'w':W,'h':round(H,1),'r':out},open(sys.argv[2],'w'),ensure_ascii=False)
print(W,H,len(json.dumps(out)))
