from pathlib import Path
import subprocess,json,datetime,shutil
R=Path(__file__).resolve().parents[1]
compiler=['java','-m','jdk.compiler/com.sun.tools.javac.Main','-Xlint:all']
sources=sorted(R.glob('Task*/src/**/*.java'))+[R/'tools/Check.java']
target=R/'build/main';target.mkdir(parents=True,exist_ok=True)
p=subprocess.run(compiler+['-d',str(target)]+list(map(str,sources)),capture_output=True,text=True)
if p.returncode:raise RuntimeError(p.stderr)
for i in range(1,13):
 if not (R/f'Task{i:02}'/'src').exists():continue
 task=R/f'Task{i:02}';(task/'results').mkdir(parents=True,exist_ok=True);(task/'screenshots').mkdir(exist_ok=True)
 (task/'results/compiler.txt').write_text('$ '+' '.join(compiler)+' -d build/main [all task src files and tools/Check.java]\n'+p.stdout+p.stderr+'Exit=0\n')
for task,name in [('Task03','ParkingFacility'),('Task08','FeeDemo')]:
 if not (R/task/'complete'/f'{name}.java').exists():continue
 target=R/'build'/task;target.mkdir(parents=True,exist_ok=True)
 p=subprocess.run(compiler+['-d',str(target),str(R/task/'complete'/f'{name}.java')],capture_output=True,text=True)
 with (R/task/'results/compiler.txt').open('a') as log:log.write('$ '+' '.join(compiler)+' -d build/'+task+' '+task+'/complete/'+name+'.java\n'+p.stdout+p.stderr+f'Exit={p.returncode}\n')
 if p.returncode:raise RuntimeError(p.stderr)
# Deliberately illegal private access must fail compilation.
if (R/'Task10/input/IllegalAccess.java.txt').exists():
 tmp=R/'build/negative';tmp.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/'Task10/input/IllegalAccess.java.txt',tmp/'IllegalAccess.java')
 p=subprocess.run(compiler+['-cp',str(R/'build/main'),'-d',str(tmp),str(tmp/'IllegalAccess.java')],capture_output=True,text=True)
 (R/'Task10/results/private-access-rejected.txt').write_text(p.stderr+f'Exit={p.returncode}\nExpected: nonzero exit for private access\n')
 if p.returncode==0 or 'private access' not in p.stderr:raise AssertionError('Private access was not rejected')
(R/'build/environment.json').write_text(json.dumps({'java':subprocess.run(['java','-version'],capture_output=True,text=True).stderr,'origin':'workspace execution','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
print('PASS all available task groups and supplied programs compile; available private access negative test rejected')
