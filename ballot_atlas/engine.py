import json, hashlib
from pathlib import Path

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def normalize(record):
    required=('source_id','name','office','jurisdiction','source_url','source_updated_at')
    if any(not isinstance(record.get(k),str) or not record[k].strip() for k in required): raise ValueError('missing required source field')
    if not record['source_url'].startswith('https://'): raise ValueError('source must be HTTPS')
    return {k:record[k].strip() for k in required} | {'party':record.get('party') or 'Not established','positions':[],'verification':'source_record_only'}
def reconcile(old,incoming):
    state={r['source_id']:r for r in old}; changes=[]
    for raw in incoming:
        candidate=normalize(raw); key=candidate['source_id']; prior=state.get(key)
        if prior is None:
            changes.append({'type':'new_candidate','source_id':key});state[key]=candidate
        elif digest({k:v for k,v in prior.items() if k not in ('positions','verification')})!=digest({k:v for k,v in candidate.items() if k not in ('positions','verification')}):
            candidate['positions']=prior.get('positions',[])
            changes.append({'type':'source_record_changed','source_id':key,'review_required':True})
            state[key]=candidate
    return sorted(state.values(),key=lambda x:x['source_id']),changes
if __name__=='__main__':
    root=Path(__file__).parent
    old=json.loads((root/'candidates.json').read_text()); incoming=json.loads((root/'incoming.json').read_text())
    updated,events=reconcile(old,incoming)
    (root/'candidates.json').write_text(json.dumps(updated,indent=2)+'\n')
    (root/'change_queue.json').write_text(json.dumps(events,indent=2)+'\n')
    print(json.dumps({'candidates':len(updated),'changes':len(events),'status':'LOCAL_ONLY'}))
