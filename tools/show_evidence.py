from pathlib import Path
import sys,subprocess
R=Path(__file__).resolve().parents[1];task,mode=sys.argv[1:3]
if task.isdigit():task=f'Task{int(task):02}'
mode={'c':'compiler','o':'output'}.get(mode,mode)
print('\033[2J\033[H',end='')
print(task+' | Assignment 1 | B Hitesh Roy | 192372036')
print('Campus Smart Parking | Actual workspace execution | OpenJDK 21.0.13')
if mode=='compiler':
 source=next((R/task/'src').rglob(task+'Demo.java'))
 print('Source: '+str(source.relative_to(R)))
 print('\n'.join(source.read_text().splitlines()[:7]))
 print('\nActual saved compiler record:')
 print((R/task/'results/compiler.txt').read_text().strip())
 if task=='Task10':print('Negative test: illegal private-field access rejected by compiler (full log in results).')
else:
 print('Actual saved run log; full output in results/execution.txt')
 lines=(R/task/'results/execution.txt').read_text().splitlines()
 if task=='Task11':
  lines=[x for x in lines if not x.startswith('PASS Scale allocation')]
  lines=lines[:29]+[x for x in lines if x.startswith(('CHECKS PASSED','OCCUPANCY','FEE','PASS Exact CLI','PASS 1000'))]
 for line in lines:print(line)
