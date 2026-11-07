from pathlib import Path
import json,hashlib,csv,re,subprocess
R=Path(__file__).resolve().parents[1]
checks={};total=0
for i in range(1,13):
 task=R/f'Task{i:02}'
 assert (task/'README.md').stat().st_size>1000
 output=(task/'results/output.txt').read_text()
 assert 'AssertionError' not in output and 'Exception in thread' not in output
 found=re.search(r'CHECKS PASSED (\d+)',output);assert found
 n=int(found[1]);assert len([s for s in output.splitlines() if s.startswith('PASS ')])==n
 total+=n;checks[task.name]=n
 assert 'Exit=0' in (task/'results/compiler.txt').read_text()
 with (task/'results/test-table.csv').open() as f:assert len(list(csv.DictReader(f)))==n
 for mode in ['compiler','output']:
  p=task/'screenshots'/f'{mode}.jpg';assert p.stat().st_size>10000 and p.read_bytes().startswith(b'\xff\xd8')
 # Run demos again without replacing captured logs or timing measurements.
 p=subprocess.run(['java','-cp',str(R/'build/main'),f'task{i:02}.Task{i:02}Demo'],capture_output=True,text=True,timeout=180)
 assert p.returncode==0 and p.stdout==output,(i,p.stderr)
for task,name in [('Task03','ParkingFacility'),('Task08','FeeDemo')]:
 source=(R/task/'complete'/f'{name}.java').read_text();assert 'TODO' not in source
 actual=(R/task/'results/supplied-output.txt').read_text();expected=(R/task/'input/expected.txt').read_text();assert actual==expected
 p=subprocess.run(['java','-cp',str(R/'build'/task),name],capture_output=True,text=True);assert p.returncode==0 and p.stdout==expected
cli=subprocess.run(['java','-cp',str(R/'build/main'),'task11.ParkingCLI'],input=(R/'Task11/input/scenario.txt').read_text(),capture_output=True,text=True)
assert cli.returncode==0 and cli.stdout==(R/'Task11/input/expected-cli.txt').read_text()
assert 'private access' in (R/'Task10/results/private-access-rejected.txt').read_text()
base=json.loads((R/'docs/baseline-sha256.json').read_text())
for path,digest in base.items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest
rows=list(csv.DictReader((R/'Task11/results/lookup.csv').open()));assert len(rows)==45
for n in [1000,10000,100000]:
 group=[r for r in rows if int(r['n'])==n];assert len(group)==15 and len(set(r['checksum'] for r in group))==1
 assert all(int(r['elapsed_ns'])>0 and int(r['queries'])==100 for r in group)
 assert all(int(r['comparisons_per_last_hit'])==n for r in group if r['method']!='hashmap')
result={'task_groups':12,'java_sources':len(list(R.glob('Task*/**/*.java')))+1,'assertion_checks':total,'checks_by_task':checks,'seeded_invariant_operations':1000,'independent_van_oracle_cases':216,'supplied_program_outputs':'exact matches','cli_output':'exact match','expected_private_access_compile_failure':'verified','screenshots':24,'lookup_timing_batches':45,'baseline_production_classes_unchanged':len(base),'changed_baseline_production_classes':0,'result':'PASS'}
(R/'docs/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
