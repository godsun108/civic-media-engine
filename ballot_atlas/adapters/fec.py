"""OpenFEC federal filing intake. FEC registration does NOT establish ballot access.
Set FEC_API_KEY in environment. No credentials in repository.
"""
import json,os,urllib.parse,urllib.request
from datetime import datetime,timezone
BASE="https://api.open.fec.gov/v1/candidates/"
def fetch(state="FL",year=2026,max_pages=10,opener=None):
    key=os.environ.get("FEC_API_KEY")
    if not key: raise RuntimeError("FEC_API_KEY is required")
    if not (1<=max_pages<=100): raise ValueError("max_pages must be 1..100")
    opener=opener or urllib.request.urlopen
    rows=[]; seen=set()
    for page in range(1,max_pages+1):
        query=urllib.parse.urlencode({"api_key":key,"state":state,"election_year":year,"per_page":100,"page":page})
        url=BASE+"?"+query
        with opener(urllib.request.Request(url,headers={"User-Agent":"BallotAtlas/0.1"}),timeout=20) as response:
            payload=json.load(response)
        for item in payload.get("results",[]):
            cid=item.get("candidate_id")
            if not cid or cid in seen: continue
            seen.add(cid)
            rows.append({"source_id":"fec:"+cid,"name":item.get("name",""),"office":{"H":"U.S. House","S":"U.S. Senate","P":"President"}.get(item.get("office"),"Federal office"),"jurisdiction":state,"source_url":"https://www.fec.gov/data/candidate/"+urllib.parse.quote(cid,safe="")+"/","source_updated_at":datetime.now(timezone.utc).isoformat(),"party":item.get("party_full") or item.get("party") or "Not established","ballot_status":"NOT_VERIFIED","source_kind":"federal_filing"})
        pagination=payload.get("pagination") or {}
        if page>=pagination.get("pages",page): break
    return rows
if __name__=="__main__":
    from pathlib import Path
    output=Path(__file__).resolve().parents[1]/"incoming.json"
    records=fetch()
    output.write_text(json.dumps(records,indent=2)+"\n")
    print(json.dumps({"federal_filing_records":len(records),"ballot_access_verified":False}))
