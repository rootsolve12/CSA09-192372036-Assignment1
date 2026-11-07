from pathlib import Path
import subprocess,sys,json,datetime
R=Path(__file__).resolve().parents[1]
for i in ([int(x) for x in sys.argv[1:]] or [i for i in range(1,13) if (R/f'Task{i:02}/src').exists()]):
 task=f'Task{i:02}';main=f'task{i:02}.{task}Demo';folder=R/task/'results'
 command=['java','-Xms64m','-Xmx512m','-cp',str(R/'build/main'),main]
 p=subprocess.run(command,capture_output=True,text=True,timeout=180)
 (folder/'output.txt').write_text(p.stdout+p.stderr)
 if p.returncode:raise RuntimeError(task+' failed:\n'+p.stdout+p.stderr)
 execution='$ java -cp build/main '+main+'\n'+p.stdout
 if i in [3,8]:
  name='ParkingFacility' if i==3 else 'FeeDemo';p=subprocess.run(['java','-cp',str(R/'build'/task),name],capture_output=True,text=True)
  (folder/'supplied-output.txt').write_text(p.stdout+p.stderr)
  assert p.returncode==0 and p.stdout==(R/task/'input/expected.txt').read_text(),task+' supplied output mismatch'
  execution+='\n$ java -cp build/'+task+' '+name+'\n'+p.stdout+'PASS Exact expected output match\n'
 if i==11:
  p=subprocess.run(['java','-cp',str(R/'build/main'),'task11.ParkingCLI'],input=(R/task/'input/scenario.txt').read_text(),capture_output=True,text=True)
  (folder/'cli-output.txt').write_text(p.stdout+p.stderr)
  assert p.returncode==0 and p.stdout==(R/task/'input/expected-cli.txt').read_text(),'CLI output mismatch'
  execution+='\n$ java -cp build/main task11.ParkingCLI < Task11/input/scenario.txt\n'+p.stdout+'PASS Exact CLI expected output match\n'
  p=subprocess.run(['java','-Xms128m','-Xmx512m','-cp',str(R/'build/main'),'task11.LookupBenchmark'],capture_output=True,text=True,timeout=180)
  (folder/'lookup.csv').write_text(p.stdout)
  assert p.returncode==0,p.stderr
 (folder/'execution.txt').write_text(execution)
 (folder/'environment.json').write_text((R/'build/environment.json').read_text())
 print(task,p.returncode,'PASS',flush=True)
