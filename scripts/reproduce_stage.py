"""Recompute factorial table and sensitivity counts from frozen compressed traces."""
import collections,gzip,hashlib,json,sys,zipfile
EXPECTED={'catalogs.json.gz':'e3defbee3d93c00cc54a1c7c93073349a8957abf4c133dd6431c02e880429171','factorial.json.gz':'3eed43c77a236c42d23fa19b3e2c6793c25b4f5c6cb92cb5dbd765adbb9cc81f','pairs.json.gz':'ff73ea1c0ef20bf466f4d90a21b16d91e3ed0cef5e0cc227bd794e7d62ddf084','support.json.gz':'e9f4f18913f1ec5930545670c24361902b521149a57315b6ccad35940f2d353a'}
ROWS={'000':((19,26),(18,28)),'001':((15,27),(17,24)),'010':((21,29),(18,28)),'011':((16,29),(17,24)),'100':((19,26),(17,28)),'101':((15,28),(17,24)),'110':((21,28),(17,28)),'111':((16,29),(17,24))}
def check(path):
    with zipfile.ZipFile(path) as z:
        data={}
        for name,sha in EXPECTED.items():
            blob=z.read('stage-local/'+name)
            assert hashlib.sha256(blob).hexdigest()==sha, name
            data[name]=json.loads(gzip.decompress(blob))
    catalogs=data['catalogs.json.gz'];fac=data['factorial.json.gz'];pairs=data['pairs.json.gz'];support=data['support.json.gz']
    assert (len(catalogs),len(fac),len(pairs),len(support))==(18,576,864,72)
    by=collections.defaultdict(list)
    for item in fac: by[item['mask'],item['method']].append(item)
    for mask,counts in ROWS.items():
        for method,(strict,edge) in zip(('simple_llm','schema_llm'),counts):
            group=by[mask,method]
            assert len(group)==36
            assert (sum(x['strict_complete'] for x in group),sum(x['edge_complete'] for x in group))==(strict,edge)
    changes=collections.Counter(p['stage'] for p in pairs if p['comparison']['visible_set_changed'])
    assert changes=={'lexical':48,'lookup':218,'packing':171},changes
    assert sum(bool(x['versus_original']['visible_set_changed']) for x in fac if x['mask']=='001')==44
    labels=collections.Counter(x['outcome_category'] for x in support)
    assert labels=={'pass':55,'explicit_refusal_in_sql':12,'table_name_rejection':4,'wrong_answer':1},labels
    print('PASS stage local: hashes, all 16 factorial cells, 44/72 packing changes, 48/218/171 stage effects and support categories')
    print('SCOPE: re-aggregation from frozen traces, not rerunning graph retrieval or LLM')
if __name__=='__main__':
    if len(sys.argv)!=2: sys.exit('Usage: python scripts/reproduce_stage.py evidence/stage-local-evidence.zip')
    check(sys.argv[1])
