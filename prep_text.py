import re, json
from pathlib import Path

html = Path("index.html").read_text(encoding="utf-8")
pairs = re.findall(r'urdu:\s*"(.*?)"\s*,\s*roman:\s*"(.*?)"', html, re.S)
print(len(pairs), "paragraphs mile (20 hone chahiye)")

def split_ur(t): return [s.strip() for s in re.split(r'(?<=۔)\s*', t) if s.strip()]
def split_ro(t): return [s.strip() for s in re.split(r'(?<=\.)\s+', t) if s.strip()]
def words(s):    return re.sub(r'[۔،.,؟?!]', '', s).split()

out, bad = {}, 0
for p, (ur, ro) in enumerate(pairs, start=1):
    us, rs = split_ur(ur), split_ro(ro)
    if len(us) != len(rs):
        print(f"P{p:02d}: sentences ghalat urdu={len(us)} roman={len(rs)}"); bad += 1; continue
    sents = []
    for i, (u, r) in enumerate(zip(us, rs), start=1):
        uw, rw = words(u), words(r)
        if len(uw) != len(rw):
            bad += 1
            print(f"P{p:02d} S{i:02d}: urdu={len(uw)} roman={len(rw)}\n  {u}\n  {r}")
        sents.append({"urdu": u, "roman": r, "urdu_words": uw, "roman_words": rw})
    out[p] = {"urdu": ur, "roman": ro, "sentences": sents}

Path("paragraphs.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("Masail:", bad)
