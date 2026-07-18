from __future__ import annotations
import hashlib,json,re,urllib.request,xml.etree.ElementTree as ET
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CFG=json.loads((ROOT/"config/sources.json").read_text(encoding="utf-8"))
OUT=ROOT/"data/automated.json"
old=json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"items":[]}
known={x["id"]:x for x in old.get("items",[])}
keywords=[x.lower() for x in CFG["keywords"]]
def clean(x): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",x or "")).strip()
def first(node,names):
    for name in names:
        hit=node.find(name)
        if hit is not None and hit.text: return clean(hit.text)
    return ""
for feed in CFG["feeds"]:
    if not feed.get("enabled"): continue
    try:
        req=urllib.request.Request(feed["url"],headers={"User-Agent":"Razer-Radar/1.0 (+https://github.com/Scoplatinum/Razer-Radar)"})
        root=ET.fromstring(urllib.request.urlopen(req,timeout=30).read())
        nodes=root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        for n in nodes[:80]:
            title=first(n,["title","{http://www.w3.org/2005/Atom}title"]);summary=first(n,["description","summary","{http://www.w3.org/2005/Atom}summary"])
            text=(title+" "+summary).lower()
            if not any(k in text for k in keywords): continue
            link=first(n,["link","guid"])
            if not link:
                el=n.find("{http://www.w3.org/2005/Atom}link");link=el.attrib.get("href","") if el is not None else ""
            uid=hashlib.sha256((link or title).encode()).hexdigest()[:16]
            known[uid]={"id":uid,"category":feed["category"],"title":title,"title_en":title,"organization":feed["name"],"location":"国际","published_at":first(n,["pubDate","date","{http://www.w3.org/2005/Atom}updated"]),"updated_at":datetime.now(timezone.utc).date().isoformat(),"deadline":"","priority":20,"verification_status":"automated_unreviewed","summary":summary[:420],"summary_en":summary[:420],"relevance":"关键词自动匹配；需打开原文后再判断研究质量与具体关联。","tags":["自动收集","待人工核验"],"source_url":link}
    except Exception as exc: print(f"WARN {feed['name']}: {exc}")
items=sorted(known.values(),key=lambda x:x.get("updated_at","") ,reverse=True)[:300]
OUT.write_text(json.dumps({"generated_at":datetime.now(timezone.utc).isoformat(),"items":items},ensure_ascii=False,indent=2),encoding="utf-8")
