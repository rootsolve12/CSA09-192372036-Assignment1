from pathlib import Path
import base64,hashlib,json,sys
R=Path(__file__).resolve().parents[1]
def record(p,include):
 b=p.read_bytes();binary=p.suffix in ['.jpg','.png'];d={'path':str(p.relative_to(R)),'size':len(b),'binary':binary,'sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
 if include:d['content']=base64.b64encode(b).decode() if binary else b.decode()
 return d
if len(sys.argv)>1:
 d=record(R/sys.argv[1],True)
 if len(sys.argv)>3:d['content']=d['content'][int(sys.argv[2]):int(sys.argv[3])]
 print(json.dumps(d))
else:
 print(json.dumps([record(p,False) for p in sorted(R.rglob('*')) if p.is_file() and 'build' not in p.relative_to(R).parts and '__pycache__' not in p.parts]))
