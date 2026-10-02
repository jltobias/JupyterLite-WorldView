"""Optional local/server-side Astra runner. Never run this with keys in JupyterLite."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'content'))
from worldview_lab import brief_request, validate_brief

def prepare(evidence, image=None):
    if evidence.get('classification')!='SYNTHETIC EXERCISE':
        raise ValueError('This teaching runner accepts SYNTHETIC EXERCISE evidence only.')
    records=evidence.get('evidence')
    if not isinstance(records,list) or not records:raise ValueError('A nonempty evidence list is required.')
    ids=[r.get('id') for r in records]
    if not all(isinstance(i,str) and i for i in ids) or len(ids)!=len(set(ids)):raise ValueError('Evidence IDs must be unique nonempty strings.')
    request=brief_request(evidence)
    if image:
        image=Path(image);mime={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg'}.get(image.suffix.lower())
        if not mime or image.stat().st_size>5*1024*1024:raise ValueError('Use a PNG or JPEG image no larger than 5 MB.')
        data=base64.b64encode(image.read_bytes()).decode()
        request['input']=[{'role':'user','content':[{'type':'input_text','text':json.dumps(evidence)},
            {'type':'input_image','image_url':f'data:{mime};base64,{data}','detail':'high'}]}]
    return request

def parse_response(response,evidence):
    if response.get('status')!='completed':raise ValueError('Response did not complete; no brief accepted.')
    parts=[]
    for item in response.get('output',[]):
        for part in item.get('content',[]):
            if part.get('type')=='refusal':raise ValueError('Model refused the request; no brief accepted.')
            if part.get('type')=='output_text':parts.append(part['text'])
    if not parts:raise ValueError('No output text returned.')
    brief=json.loads(''.join(parts));validate_brief(brief,evidence)
    return brief

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence',required=True,type=Path)
    parser.add_argument('--image',type=Path,help='Reviewed synthetic map or chart; sent to OpenAI when not dry-running')
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--dry-run',action='store_true',help='Write request only; make no API call')
    args=parser.parse_args()
    if args.evidence.stat().st_size>256*1024:raise ValueError('Evidence exceeds 256 KB teaching limit.')
    raw=args.evidence.read_bytes();evidence=json.loads(raw);request=prepare(evidence,args.image)
    if args.dry_run:result=request
    else:
        key=os.environ.get('OPENAI_API_KEY')
        if not key:raise ValueError('Set OPENAI_API_KEY in the local/server process environment. Never put it in the public site.')
        req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(request).encode(),
            headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=180) as response:payload=json.load(response)
        except urllib.error.HTTPError as error:raise RuntimeError(f'OpenAI HTTP {error.code}; check account access, request limits, and service status.') from None
        result={'brief':parse_response(payload,evidence),'audit':{'requested_model':request['model'],
            'returned_model':payload.get('model'),'response_id':payload.get('id'),'usage':payload.get('usage'),
            'evidence_sha256':hashlib.sha256(raw).hexdigest(),
            'image_sha256':hashlib.sha256(args.image.read_bytes()).hexdigest() if args.image else None,
            'created_at':datetime.now(timezone.utc).isoformat(),'review_status':'UNREVIEWED'}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(('Request prepared (no network call): ' if args.dry_run else 'Unreviewed brief saved: ')+str(args.output))

if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError) as error:
        print('Brief not accepted: '+str(error),file=sys.stderr);sys.exit(1)
