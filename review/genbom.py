# -*- coding: utf-8 -*-
# Genererer BOM.txt fra BUDGET.md's tabeller. Kør igen efter enhver budgetændring.
import re, os
ROOT=r'C:\Users\PK\Desktop\Agervej\Lux teresse'
m=open(os.path.join(ROOT,'BUDGET.md'),encoding='utf-8').read()

def strip_md(t):
    t=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',t)  # links -> text
    return t.replace('**','').strip()

sections=[]
for sm in re.finditer(r'^## ([A-I])\. (.+?)$(.*?)(?=^## |\Z)',m,re.M|re.S):
    k,title,body=sm.group(1),strip_md(sm.group(2)),sm.group(3)
    rows=[]; total=None
    for l in body.split('\n'):
        if not l.startswith('| ') or l.startswith('| Vare') or l.startswith('|---'): continue
        f=[strip_md(x) for x in l.split('|')[1:-1]]
        if f[0].startswith('Sum '):
            total=next(x for x in f[1:] if x); continue
        # Vare Spec Antal Enhed Stkpris Total Butik Sikkerhed Note
        rows.append(dict(vare=f[0],spec=f[1],antal=f[2],enhed=f[3],pris=f[4],total=f[5],butik=f[6],sik=f[7],note=f[8]))
    sections.append((k,title,rows,total))

def wrap(t,w,indent):
    out=[];line=''
    for word in t.split():
        if len(line)+len(word)+1>w: out.append(line); line=word
        else: line=(line+' '+word).strip()
    if line: out.append(line)
    return ('\n'+' '*indent).join(out)

W=100
L=[]
L.append('='*W)
L.append('LUX DECK - KOMPLET STYKLISTE (BOM)')
L.append('Naturpool 2x3 m, biofilter, termofyr-terrasse +35, zen-sandcirkel, teknikboks')
L.append('Priser DKK inkl. moms, verificeret 19.-20. august 2026. Alt arbejde selvbyg.')
L.append('Fuld dokumentation: https://github.com/cph4cker/lux-terrasse (BUDGET.md, review/)')
L.append('='*W)
L.append('')
grand=0
for k,title,rows,total in sections:
    L.append(f'{k}. {title.upper()}   [{total} kr]')
    L.append('-'*W)
    for r in rows:
        antal=f"{r['antal']} {r['enhed']}".strip()
        L.append(f"[ ] {r['vare']}")
        if r['spec']: L.append(f"      {wrap(r['spec'],W-8,6)}")
        L.append(f"      {antal}  a {r['pris']} kr  =  {r['total']} kr    ({r['butik']}, {r['sik']})")
        if r['note']: L.append(f"      OBS: {wrap(r['note'],W-12,11)}")
        L.append('')
    grand+=int(total.replace('.',''))
L.append('='*W)
def kr(v): return f'{v:,}'.replace(',','.')
L.append(f"MATERIALER I ALT, EKSKL. UFORUDSET:  {kr(grand)} kr")
L.append(f"+ 20 % UFORUDSET:                    {kr(round(grand*0.2))} kr")
L.append(f"BUDGET INKL. UFORUDSET:              {kr(round(grand*1.2))} kr")
L.append('')
L.append('Udenfor tallet: ingeniørberegning af armering 1.500-3.000 kr (SKAL laves før jern bestilles),')
L.append('evt. UV-C 1.500 kr (kun hvis vandet bliver grønt), evt. færdigbeton til bundpladen +2.500 kr.')
L.append('')
et1=sum(int(t.replace('.','')) for k,_,_,t in sections if k in 'ABGHI')
et2=grand-et1
L.append(f"ETAPE 1 (A, B, G, H, I: hul, plader, vægge, trappe, terrasse, sandcirkel): {kr(et1)} kr")
L.append(f"ETAPE 2 (C, D, E, F: membran, VVS, pumpe, filtergrus, vand):               {kr(et2)} kr")
L.append('')
L.append('INDKØBSPLAN (kort):')
L.append('  1. Byggemarked, EN palleordre (uge 0-1): 3 pl. 19 cm blok + 1 pl. 15 cm + 1 pl. cement = fri')
L.append('     levering. Bed om projektpris (5-10 %). + armering (EFTER ingeniøren), net, folie, forskalling.')
L.append('  2. Vognmand (ring 2): 6 t stabilgrus 0-32 (uge 0) + 10 t betongrus 0-16 (dagen før støbning)')
L.append('     + 0,5 t bakkesand 0-4 til puds. Etape 2: filtergrus 2,7 t hentes selv på trailer (vaskede sorter).')
L.append('  3. HN/jem&fix på trailer: strøer, reglar, beslag, A4-skruer 4,8x75, fiberdug, presenning,')
L.append('     dykpumpe, kabelrør, PVC-lim, sandkassesand i sække.')
L.append('  4. Termofyr-butik: 28 dæk + 3 fascia + 2 låg = 33 brædder, samme batch, spørg om restparti.')
L.append('  5. Net: jordskruer.dk (18 stk 68/1000 + maskinleje), kakelgiganten (alt Mapei, 1 fragt),')
L.append('     koimad.dk (PVC + haner), fynshavedam.dk (12 V-pumpe + skimmer, 1 fragt). Planter: havecenter, maj.')
L.append('  6. DBA nu: betonblander 130-160 l (~1.200, sælges igen), stavvibrator.')
L.append('')
L.append('MÅ IKKE SPARES VÆK: armering + fyldte celler (vent på ingeniøren), 5 sæt Mapelastic + net,')
L.append('cementdosering >=300 kg/m3 og pladen på ÉN dag, gennemføringer FØR cellefyld, jordskruer 1000 mm,')
L.append('47x200 bjælker + strø c/c 400, A4-skruer + forboring, hulkehl + slidpuds på vægtoppe,')
L.append('geotekstil + 5 cm afretning under filtergrus, 28 døgns hærdning før bagfyld.')
L.append('')
L.append('Genereret 2026-08-20 fra BUDGET.md.')
open(os.path.join(ROOT,'BOM.txt'),'w',encoding='utf-8',newline='\r\n').write('\n'.join(L))
print('rows:',sum(len(r) for _,_,r,_ in sections),'total:',grand)
