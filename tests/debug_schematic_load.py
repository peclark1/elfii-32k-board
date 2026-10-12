#!/usr/bin/env python3
"""Temporary KiCad load delta-debugger. Runs only on feature/debug-current-load."""
from pathlib import Path
import subprocess

SRC=Path("hardware/kicad/elfii-32k-board.kicad_sch")
OUT=Path("out/load-debug")
OUT.mkdir(parents=True, exist_ok=True)
s=SRC.read_text()

def form_at(start):
    d=0; q=False; esc=False
    for i in range(start,len(s)):
        c=s[i]
        if q:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': q=False
        elif c=='"': q=True
        elif c=="(": d+=1
        elif c==")":
            d-=1
            if d==0: return s[start:i+1]
    raise RuntimeError("unbalanced")

# Parse child forms immediately under root.
root_start=s.index("(kicad_sch")
children=[]
d=0; q=False; esc=False; child_start=None
for i,c in enumerate(s[root_start:], start=root_start):
    if q:
        if esc: esc=False
        elif c=="\\": esc=True
        elif c=='"': q=False
        continue
    if c=='"': q=True; continue
    if c=="(":
        d+=1
        if d==2: child_start=i
    elif c==")":
        if d==2 and child_start is not None:
            f=s[child_start:i+1]
            tag=f[1:].lstrip().split(None,1)[0].split("(",1)[0]
            children.append((tag,f))
            child_start=None
        d-=1

by={}
for tag,f in children: by.setdefault(tag,[]).append(f)
base=[by[k][0] for k in ("version","generator","uuid","paper","title_block") if k in by]
sheet=by["sheet_instances"][0]

def write(name, parts):
    p=OUT/f"{name}.kicad_sch"
    p.write_text("(kicad_sch\n" + "\n".join(base+parts+[sheet]) + "\n)\n")
    return p

def try_load(name,p):
    pdf=OUT/f"{name}.pdf"
    r=subprocess.run(["kicad-cli","sch","export","pdf","-o",str(pdf),str(p)],text=True,capture_output=True)
    msg=(r.stdout+r.stderr).strip().replace("\n"," | ")
    print(f"{name}: rc={r.returncode} {msg}")
    return r.returncode==0

write("empty",["(lib_symbols)"])
write("lib_only",[by["lib_symbols"][0]])
write("instances",[by["lib_symbols"][0],*by.get("symbol",[])])
write("instances_wires",[by["lib_symbols"][0],*by.get("symbol",[]),*by.get("wire",[]),*by.get("label",[])])
write("no_bus",[by["lib_symbols"][0],*by.get("symbol",[]),*by.get("wire",[]),*by.get("label",[]),*by.get("junction",[]),*by.get("no_connect",[]),*by.get("text",[])])
write("no_text",[by["lib_symbols"][0],*by.get("symbol",[]),*by.get("wire",[]),*by.get("label",[]),*by.get("junction",[]),*by.get("no_connect",[]),*by.get("bus",[]),*by.get("bus_entry",[])])
for name in ("empty","lib_only","instances","instances_wires","no_bus","no_text"):
    try_load(name,OUT/f"{name}.kicad_sch")

# If the library itself is bad, split its direct child symbol definitions.
lib=by["lib_symbols"][0]
lib_children=[]
d=0; q=False; esc=False; st=None
for i,c in enumerate(lib):
    if q:
        if esc: esc=False
        elif c=="\\": esc=True
        elif c=='"': q=False
        continue
    if c=='"': q=True; continue
    if c=="(":
        d+=1
        if d==2: st=i
    elif c==")":
        if d==2 and st is not None:
            lib_children.append(lib[st:i+1]); st=None
        d-=1
for i,f in enumerate(lib_children):
    nm=f.split('"')[1] if '"' in f else str(i)
    safe="".join(ch if ch.isalnum() else "_" for ch in nm)
    p=write(f"lib_{i}_{safe}",["(lib_symbols\n"+f+"\n)"])
    try_load(f"lib_{i}_{safe}",p)
