from pathlib import Path
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase.pdfmetrics import stringWidth
from pypdf import PdfReader, PdfWriter
import math

ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = Path(os.environ.get("PROJECTSAURON_BUILD_DIR", ROOT / ".build"))
BASE = BUILD_DIR / "ProjectSauron_CASE-004_REBUILT.pdf"
OUT = BUILD_DIR / "ProjectSauron_CASE-004_VISUAL_v2.pdf"
TMP = BUILD_DIR / "_psauron_overlays"
TMP.mkdir(parents=True, exist_ok=True)
W,H=A4

# Series-aligned palette
DARK = HexColor('#071515')
DARK2 = HexColor('#0B2420')
GREEN = HexColor('#27B87D')
GREEN2 = HexColor('#6BE4B6')
TEAL = HexColor('#2EB6C6')
RED = HexColor('#D94D5D')
RED2 = HexColor('#FF7B87')
INK = HexColor('#172126')
MUTED = HexColor('#607277')
LINE = HexColor('#D8E3E1')
PANEL = HexColor('#F4FAF7')
PANEL2 = HexColor('#EFF8FA')
WHITE = HexColor('#FFFFFF')


def rr(c,x,y,w,h,r=7,fill=None,stroke=LINE,lw=0.8):
    c.setLineWidth(lw)
    if fill: c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x,y,w,h,r,fill=1 if fill else 0,stroke=1)

def label(c,txt,x,y,size=7.2,color=MUTED,font='Helvetica-Bold'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,txt)

def text(c,txt,x,y,size=8,color=INK,font='Helvetica'):
    c.setFillColor(color); c.setFont(font,size); c.drawString(x,y,txt)

def centered(c,txt,x,y,w,size=8,color=INK,font='Helvetica-Bold'):
    c.setFillColor(color); c.setFont(font,size); c.drawCentredString(x+w/2,y,txt)

def arrow(c,x1,y1,x2,y2,color=RED,lw=1.7):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(lw); c.line(x1,y1,x2,y2)
    ang=math.atan2(y2-y1,x2-x1); a=7
    pts=[(x2,y2),(x2-a*math.cos(ang-0.45),y2-a*math.sin(ang-0.45)),(x2-a*math.cos(ang+0.45),y2-a*math.sin(ang+0.45))]
    p=c.beginPath(); p.moveTo(*pts[0]); p.lineTo(*pts[1]); p.lineTo(*pts[2]); p.close(); c.drawPath(p,fill=1,stroke=0)

def section_title(c, x, y, title, subtitle=None):
    c.setFillColor(GREEN); c.rect(x,y+22,5,5,fill=1,stroke=0)
    label(c,title.upper(),x+11,y+21,6.8,GREEN)
    if subtitle: text(c,subtitle,x+11,y+7,7.3,MUTED)


def make_cover(path):
    c=canvas.Canvas(str(path),pagesize=A4)
    # background
    c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
    # layered panels for depth
    c.setFillColor(HexColor('#0A201D')); c.rect(0,H*0.46,W,H*0.54,fill=1,stroke=0)
    c.setFillColor(HexColor('#161014')); c.rect(0,0,W,H*0.26,fill=1,stroke=0)
    # grid
    c.setStrokeColor(Color(0.35,0.8,0.65,alpha=0.11)); c.setLineWidth(0.4)
    step=34
    for x in range(0,int(W)+1,step): c.line(x,0,x,H)
    for y in range(0,int(H)+1,step): c.line(0,y,W,y)
    # top line + meta
    c.setStrokeColor(HexColor('#56746A')); c.setLineWidth(0.6); c.line(37,H-31,W-37,H-31)
    label(c,'MICHEL-DV THREAT CASE STUDIES / CASE-004 / V1.0.0',37,H-47,7.7,GREEN2,'Courier-Bold')
    c.setFillColor(RED); c.rect(W-76,H-44,19,2.8,fill=1,stroke=0)
    label(c,'CYBER ESPIONAGE',W-142,H-58,6.6,HexColor('#C9D5D2'),'Courier')
    label(c,'AIR-GAP OPERATIONS',W-142,H-70,6.6,HexColor('#C9D5D2'),'Courier')
    label(c,'INCIDENT RECONSTRUCTION',W-142,H-82,6.6,HexColor('#C9D5D2'),'Courier')

    # Hero: connected enclave + air-gapped enclave
    hero_y=430; hero_h=245
    # left network zone
    rr(c,45,hero_y+22,205,170,14,HexColor('#0B2420'),HexColor('#4FD2A3'),1.2)
    label(c,'CONNECTED NETWORK',62,hero_y+170,7.5,GREEN2,'Courier-Bold')
    # nodes
    nodes=[(82,hero_y+118,'DC'),(150,hero_y+135,'OPS'),(190,hero_y+88,'PROXY'),(112,hero_y+62,'VFS')]
    for x,y,t in nodes:
        c.setFillColor(HexColor('#102F29')); c.setStrokeColor(GREEN); c.setLineWidth(1)
        c.circle(x,y,18,fill=1,stroke=1); centered(c,t,x-18,y-3,36,7.2,WHITE,'Courier-Bold')
    for (x1,y1,_),(x2,y2,_) in [(nodes[0],nodes[1]),(nodes[1],nodes[2]),(nodes[0],nodes[3]),(nodes[3],nodes[2])]:
        c.setStrokeColor(HexColor('#3F8F78')); c.setLineWidth(1); c.line(x1+18,y1,x2-18,y2)
    # right airgap zone
    rr(c,346,hero_y+22,205,170,14,HexColor('#171216'),HexColor('#EF6672'),1.2)
    label(c,'AIR-GAPPED NETWORK',364,hero_y+170,7.5,RED2,'Courier-Bold')
    for i,(x,y,t) in enumerate([(392,hero_y+112,'WS'),(470,hero_y+125,'DATA'),(430,hero_y+66,'KEYS')]):
        c.setFillColor(HexColor('#24161B')); c.setStrokeColor(RED); c.circle(x,y,18,fill=1,stroke=1); centered(c,t,x-18,y-3,36,7.2,WHITE,'Courier-Bold')
    c.setStrokeColor(HexColor('#8E3D49')); c.line(410,hero_y+112,452,hero_y+125); c.line(408,hero_y+100,430,hero_y+84)

    # air gap divide
    c.setStrokeColor(HexColor('#82948F')); c.setDash(4,4); c.setLineWidth(0.9); c.line(W/2,hero_y+18,W/2,hero_y+198); c.setDash()
    label(c,'AIR GAP',W/2-19,hero_y+205,6.6,HexColor('#A8B9B4'),'Courier-Bold')

    # USB bridge large icon
    ux=W/2-47; uy=hero_y+77
    c.setFillColor(HexColor('#0D1C1B')); c.setStrokeColor(HexColor('#E6F3EF')); c.setLineWidth(1.2)
    c.roundRect(ux,uy,94,44,8,fill=1,stroke=1)
    c.setFillColor(HexColor('#C8DAD5')); c.rect(ux+94,uy+11,20,22,fill=1,stroke=0)
    c.setFillColor(DARK); c.rect(ux+100,uy+15,5,5,fill=1,stroke=0); c.rect(ux+108,uy+24,5,5,fill=1,stroke=0)
    c.setFillColor(GREEN); c.roundRect(ux+11,uy+9,43,26,5,fill=1,stroke=0)
    centered(c,'HIDDEN',ux+11,uy+23,43,6.3,WHITE,'Courier-Bold'); centered(c,'VOLUME',ux+11,uy+13,43,6.3,WHITE,'Courier-Bold')
    c.setFillColor(RED); c.circle(ux+71,uy+22,4,fill=1,stroke=0)
    arrow(c,250,uy+22,ux,uy+22,GREEN,1.5); arrow(c,ux+114,uy+22,346,uy+22,RED,1.5)

    # lower signal line
    c.setStrokeColor(TEAL); c.setLineWidth(1.1)
    y=hero_y-8
    pts=[]
    for i in range(70):
        x=48+i*7.2; yy=y+8*math.sin(i/4.1)+3*math.sin(i/1.9); pts.append((x,yy))
    for a,b in zip(pts,pts[1:]): c.line(a[0],a[1],b[0],b[1])
    label(c,'DNS / SMTP / HTTP  ·  INTERNAL PROXY  ·  REMOVABLE MEDIA',52,hero_y-30,6.6,HexColor('#76C5D0'),'Courier')

    # title block
    title_y=180
    c.setFillColor(WHITE); c.setFont('Helvetica-Bold',30); c.drawString(37,title_y+63,'ProjectSauron / Strider')
    c.setFillColor(RED2); c.setFont('Helvetica-Bold',25); c.drawString(37,title_y+31,'Air-Gap Espionage Platform')
    text(c,'Technical Case Study - Customized Implants, Hidden USB Storage and Memory-Only Espionage',37,title_y+3,11,HexColor('#BBD1CA'))
    c.setFillColor(RED); c.rect(37,title_y-26,4,28,fill=1,stroke=0)
    text(c,'No reusable indicators. No visible partition. No obvious path out.',52,title_y-17,10.5,WHITE,'Helvetica-Bold')
    # footer
    c.setStrokeColor(HexColor('#60736D')); c.line(37,55,W-37,55)
    text(c,'Research & Case Study - @Michel-DV',37,35,9.2,WHITE,'Helvetica-Bold')
    label(c,'1 October 2026',W-128,37,7,HexColor('#AABAB5'),'Courier')
    label(c,'CC BY-NC-ND 4.0',W-128,25,7,HexColor('#AABAB5'),'Courier')
    c.save()


def overlay_for_page(page_no,path):
    c=canvas.Canvas(str(path),pagesize=A4)
    # Decorative edge marker consistent across figures
    def figbox(x,y,w,h,title,subtitle=None,fill=PANEL):
        rr(c,x,y,w,h,8,fill,LINE,0.7)
        c.setFillColor(GREEN); c.rect(x,y+h-5,w,5,fill=1,stroke=0)
        section_title(c,x+10,y+h-27,title,subtitle)
    if page_no==2:
        x,y,w,h=55,73,485,150; figbox(x,y,w,h,'Operation architecture','A platform built around adaptable roles rather than one fixed implant')
        xs=[78,180,282,384,486]; names=['FOOTHOLD','DOMAIN','MEMORY','RELAY','EXFIL']
        subs=['unknown','LSA / admin','plugins / VFS','proxy nodes','DNS / USB']
        for i,(xx,n,s) in enumerate(zip(xs,names,subs)):
            rr(c,xx,y+42,78,50,7,WHITE,HexColor('#CADBD6'),0.7); centered(c,n,xx,y+72,78,7.2,GREEN,'Helvetica-Bold'); centered(c,s,xx,y+56,78,6.5,MUTED)
            if i<4: arrow(c,xx+78,y+67,xs[i+1]-4,y+67,RED,1.2)
        label(c,'CASE MODEL',x+10,y+15,6.3,MUTED,'Courier-Bold'); text(c,'Unknown entry -> privileged Windows estate -> modular in-memory capability -> covert collection -> controlled egress',x+88,y+14,7.3,INK)
    elif page_no==3:
        x,y,w,h=55,72,485,142; figbox(x,y,w,h,'Long-dwell timeline','Operational patience was part of the design')
        base=y+57; c.setStrokeColor(HexColor('#9DCDBB')); c.setLineWidth(2); c.line(x+28,base,x+w-28,base)
        events=[('2011','earliest activity'),('2013','target-specific tooling'),('2015','deep modular platform'),('2016','public exposure')]
        ex=[x+55,x+175,x+305,x+425]
        for xx,(yr,desc) in zip(ex,events):
            c.setFillColor(GREEN); c.circle(xx,base,6,fill=1,stroke=0); centered(c,yr,xx-35,base+25,70,7.8,INK,'Helvetica-Bold'); centered(c,desc,xx-45,base-24,90,6.3,MUTED)
    elif page_no==4:
        x,y,w,h=55,68,485,150; figbox(x,y,w,h,'Intelligence objective','Collection focused on durable access to high-value secrets')
        cols=[('CREDENTIALS','domain and operator access',GREEN),('DOCUMENTS','mission data and archives',TEAL),('KEY MATERIAL','protected communications',RED),('SYSTEM MAP','infrastructure knowledge',GREEN)]
        cw=(w-30)/4
        for i,(a,b,col) in enumerate(cols):
            xx=x+10+i*cw; rr(c,xx,y+34,cw-6,72,7,WHITE,HexColor('#D3DFDC'),0.7); c.setFillColor(col); c.circle(xx+20,y+84,7,fill=1,stroke=0); label(c,a,xx+34,y+81,6.5,col); text(c,b,xx+12,y+55,6.4,MUTED)
    elif page_no==5:
        x,y,w,h=55,68,485,165; figbox(x,y,w,h,'Modular platform model','Capabilities could be mixed per target while core tradecraft remained stable')
        center=(x+w/2,y+79); c.setFillColor(DARK2); c.circle(center[0],center[1],35,fill=1,stroke=0); centered(c,'CORE',center[0]-35,center[1]+4,70,9,WHITE); centered(c,'FRAMEWORK',center[0]-35,center[1]-10,70,6.2,GREEN2)
        mods=[('CRED',x+35,y+95,GREEN),('VFS',x+120,y+35,TEAL),('PROXY',x+330,y+35,RED),('DNS',x+410,y+95,TEAL),('USB',x+120,y+116,RED),('TASK',x+330,y+116,GREEN)]
        for t,xx,yy,col in mods:
            rr(c,xx,yy,62,28,6,WHITE,HexColor('#CCD9D6'),0.7); centered(c,t,xx,yy+10,62,7,col)
            arrow(c,xx+31,yy+14,center[0],center[1],HexColor('#A4B8B1'),0.8)
    elif page_no==6:
        x,y,w,h=55,72,485,142; figbox(x,y,w,h,'Credential collection path','Why domain controllers became collection points')
        boxes=[('DOMAIN\nCONTROLLER',72),('PASSWORD\nFILTER DLL',205),('LSASS /\nAUTH FLOW',338),('ENCRYPTED\nCOLLECTION',471)]
        for i,(t,xx) in enumerate(boxes):
            rr(c,xx,y+43,85,52,7,WHITE,HexColor('#CBD9D5'),0.7)
            a,b=t.split('\n'); centered(c,a,xx,y+72,85,6.7,GREEN if i<3 else RED,'Helvetica-Bold'); centered(c,b,xx,y+57,85,6.5,MUTED)
            if i<3: arrow(c,xx+85,y+69,boxes[i+1][1]-4,y+69,RED,1.1)
    elif page_no==7:
        x,y,w,h=55,69,485,158; figbox(x,y,w,h,'Ephemeral execution stack','Persistent data could live in an encrypted VFS while capability stayed memory-resident')
        layers=[('OPERATOR TASK',HexColor('#EAF8F2')),('IN-MEMORY PLUGIN',HexColor('#E6F5F7')),('CUSTOM LUA / VFS',HexColor('#F2F7F5')),('ENCRYPTED STORE',HexColor('#FFF0F1'))]
        yy=y+30
        for i,(t,col) in enumerate(reversed(layers)):
            rr(c,x+110,yy+i*25,w-220,20,5,col,HexColor('#C8D8D3'),0.6); centered(c,t,x+110,yy+7+i*25,w-220,6.8,INK,'Helvetica-Bold')
        label(c,'DISK',x+42,y+41,6.3,MUTED,'Courier-Bold'); label(c,'MEMORY',x+w-83,y+112,6.3,MUTED,'Courier-Bold')
        arrow(c,x+79,y+48,x+110,y+48,RED,1); arrow(c,x+w-110,y+120,x+w-79,y+120,GREEN,1)
    elif page_no==8:
        x,y,w,h=55,68,485,155; figbox(x,y,w,h,'Trusted administration as execution','Legitimate enterprise mechanisms can become transport for a hostile operator')
        stages=[('ADMIN\nSHARE','normal trust'),('SCRIPT /\nTOOLING','execution'),('REMOTE\nHOST','implant'),('COVERT\nROLE','relay / collect')]
        xs=[72,197,322,447]
        for i,((a,b),xx) in enumerate(zip(stages,xs)):
            rr(c,xx,y+45,90,57,7,WHITE,HexColor('#CADAD5'),0.7); centered(c,a,xx,y+77,90,7,GREEN if i<2 else RED,'Helvetica-Bold'); centered(c,b,xx,y+59,90,6.4,MUTED)
            if i<3: arrow(c,xx+90,y+73,xs[i+1]-5,y+73,RED,1.1)
    elif page_no==9:
        x,y,w,h=55,68,485,160; figbox(x,y,w,h,'Channel constellation','Redundant command and exfiltration paths reduced dependence on one protocol')
        center=(x+w/2,y+73); c.setFillColor(DARK2); c.circle(*center,29,fill=1,stroke=0); centered(c,'NODE',center[0]-28,center[1]-3,56,8,WHITE,'Helvetica-Bold')
        chans=[('DNS',x+60,y+105,TEAL),('HTTP',x+390,y+105,GREEN),('SMTP',x+60,y+37,RED),('ICMP',x+390,y+37,TEAL),('PROXY',x+225,y+118,GREEN)]
        for t,xx,yy,col in chans:
            rr(c,xx,yy,70,27,6,WHITE,HexColor('#CCDAD6'),0.6); centered(c,t,xx,yy+9,70,7,col,'Helvetica-Bold'); arrow(c,center[0],center[1],xx+35,yy+13,HexColor('#9AAFAA'),0.8)
    elif page_no==10:
        x,y,w,h=55,58,485,180; figbox(x,y,w,h,'Air-gap bridge','A removable device can be both transport and covert storage')
        rr(c,x+20,y+40,130,74,9,HexColor('#EAF8F2'),HexColor('#A8D7C5'),0.8); centered(c,'CONNECTED',x+20,y+82,130,8,GREEN,'Helvetica-Bold'); centered(c,'NETWORK',x+20,y+66,130,8,GREEN,'Helvetica-Bold')
        rr(c,x+w-150,y+40,130,74,9,HexColor('#FFF0F1'),HexColor('#E2ADB3'),0.8); centered(c,'AIR-GAPPED',x+w-150,y+82,130,8,RED,'Helvetica-Bold'); centered(c,'NETWORK',x+w-150,y+66,130,8,RED,'Helvetica-Bold')
        ux=x+w/2-48; uy=y+59; rr(c,ux,uy,96,40,7,DARK2,HexColor('#8FB6AA'),0.9); c.setFillColor(GREEN); c.roundRect(ux+12,uy+10,43,20,4,fill=1,stroke=0); centered(c,'HIDDEN VFS',ux+12,uy+17,43,6.1,WHITE,'Courier-Bold'); c.setFillColor(HexColor('#D7E3E0')); c.rect(ux+96,uy+10,18,20,fill=1,stroke=0)
        arrow(c,x+150,y+77,ux-5,y+77,GREEN,1.4); arrow(c,ux+114,y+77,x+w-150,y+77,RED,1.4)
        label(c,'OUTBOUND: tasking / implant movement',x+20,y+20,6.5,MUTED,'Courier'); label(c,'RETURN: collected data / keys',x+w-220,y+20,6.5,MUTED,'Courier')
    elif page_no==11:
        x,y,w,h=55,64,485,165; figbox(x,y,w,h,'Hidden storage beyond the visible partition','The physical device and the filesystem view were not equivalent trust boundaries')
        bx=x+30; by=y+55; bw=w-60; bh=50
        rr(c,bx,by,bw,bh,6,WHITE,HexColor('#BFCFCB'),0.8)
        visible=bw*0.66
        c.setFillColor(HexColor('#E9F6F2')); c.roundRect(bx+1,by+1,visible-1,bh-2,5,fill=1,stroke=0)
        c.setFillColor(HexColor('#1D3B34')); c.roundRect(bx+visible,by+1,bw-visible-1,bh-2,5,fill=1,stroke=0)
        centered(c,'VISIBLE FILESYSTEM',bx,by+20,visible,7.1,GREEN,'Helvetica-Bold')
        centered(c,'HIDDEN / ENCRYPTED',bx+visible,by+24,bw-visible,6.7,WHITE,'Helvetica-Bold'); centered(c,'STORAGE AREA',bx+visible,by+12,bw-visible,6.3,GREEN2,'Helvetica-Bold')
        c.setStrokeColor(RED); c.setLineWidth(1.2); c.line(bx+visible,by-9,bx+visible,by+bh+9); label(c,'OS-visible boundary',bx+visible-29,by-20,6.2,RED,'Courier-Bold')
    elif page_no==12:
        x,y,w,h=55,62,485,165; figbox(x,y,w,h,'Collection priorities','The platform targeted information with durable intelligence value')
        items=[('IDENTITY','credentials / admin access',GREEN),('MISSION','documents / archives',TEAL),('CRYPTO','keys / protected comms',RED),('TOPOLOGY','systems / roles / trust',GREEN)]
        for i,(a,b,col) in enumerate(items):
            xx=x+16+i*115; rr(c,xx,y+45,105,62,7,WHITE,HexColor('#CCD9D6'),0.7); c.setFillColor(col); c.rect(xx, y+45, 4, 62, fill=1, stroke=0); label(c,a,xx+12,y+83,6.8,col); text(c,b,xx+12,y+62,6.2,MUTED)
    elif page_no==13:
        x,y,w,h=55,66,485,158; figbox(x,y,w,h,'Anti-pattern strategy','Per-target variation breaks brittle IOC-based hunting')
        vals=[('Host A','loader α','pipe X','timestamp clone'),('Host B','loader β','DNS Y','unique name'),('Host C','loader γ','proxy Z','memory only')]
        yy=y+42
        for r,row in enumerate(vals):
            xx=x+22; c.setFillColor(WHITE); c.setStrokeColor(HexColor('#D0DDDA')); c.roundRect(xx,yy+r*30,w-44,24,5,fill=1,stroke=1)
            for i,v in enumerate(row): text(c,v,xx+10+i*108,yy+8+r*30,6.6,GREEN if i==0 else INK,'Helvetica-Bold' if i==0 else 'Helvetica')
        label(c,'same mission / different surface',x+150,y+17,6.4,RED,'Courier-Bold')
    elif page_no==14:
        x,y,w,h=55,63,485,162; figbox(x,y,w,h,'Behavior-first hunting','Stable relationships survive when names and hashes do not')
        # funnel
        tiers=[('LOW VALUE','hashes · filenames · domains',430,HexColor('#EEF5F3')),('MEDIUM','module load · service role · proxy behavior',330,HexColor('#EAF7F3')),('HIGH VALUE','trust transitions · auth hooks · media anomalies',235,HexColor('#E8F7F8'))]
        cy=y+112
        for i,(a,b,width,col) in enumerate(tiers):
            xx=x+w/2-width/2; yy=cy-i*36
            c.setFillColor(col); c.setStrokeColor(HexColor('#CAD8D5')); p=c.beginPath(); p.moveTo(xx,yy); p.lineTo(xx+width,yy); p.lineTo(xx+width-38,yy-28); p.lineTo(xx+38,yy-28); p.close(); c.drawPath(p,fill=1,stroke=1)
            label(c,a,xx+13,yy-13,6.5,GREEN if i==2 else MUTED,'Courier-Bold'); text(c,b,xx+88,yy-14,6.5,INK)
    elif page_no==15:
        x,y,w,h=55,57,485,185; figbox(x,y,w,h,'Trust-boundary path','A compact visual companion to the ATT&CK mapping above')
        names=['IDENTITY','DOMAIN','MEMORY','RELAY','MEDIA','AIR GAP']
        xs=[66,146,226,306,386,466]
        for i,(n,xx) in enumerate(zip(names,xs)):
            c.setFillColor(DARK2 if i in [1,2] else WHITE); c.setStrokeColor(GREEN if i<4 else RED); c.setLineWidth(0.9); c.circle(xx,y+89,24,fill=1,stroke=1); centered(c,n,xx-30,y+86,60,5.8,WHITE if i in [1,2] else INK,'Helvetica-Bold')
            if i<5: arrow(c,xx+24,y+89,xs[i+1]-24,y+89,RED if i>=3 else GREEN,1)
        text(c,'credentials',x+7,y+33,6.3,MUTED); text(c,'privilege',x+88,y+33,6.3,MUTED); text(c,'ephemeral code',x+165,y+33,6.3,MUTED); text(c,'covert transport',x+265,y+33,6.3,MUTED); text(c,'hidden storage',x+377,y+33,6.3,MUTED)
    elif page_no==16:
        x,y,w,h=55,53,485,190; figbox(x,y,w,h,'Detection correlation model','Individual weak signals become useful when they describe the same trust-path transition')
        # central alert graph
        center=(x+w/2,y+92); c.setFillColor(DARK2); c.circle(*center,34,fill=1,stroke=0); centered(c,'CORRELATE',center[0]-34,center[1]+3,68,7.4,WHITE,'Helvetica-Bold'); centered(c,'NOT ISOLATE',center[0]-34,center[1]-11,68,6.2,GREEN2,'Courier-Bold')
        sigs=[('LSASS\nMODULE',x+55,y+121,GREEN),('DNS\nSIGNAL',x+377,y+121,TEAL),('USB\nGEOMETRY',x+55,y+38,RED),('PROXY\nROLE',x+377,y+38,GREEN)]
        for t,xx,yy,col in sigs:
            rr(c,xx,yy,82,40,6,WHITE,HexColor('#CCD9D6'),0.7); a,b=t.split('\n'); centered(c,a,xx,yy+23,82,6.5,col,'Helvetica-Bold'); centered(c,b,xx,yy+10,82,6.2,MUTED); arrow(c,xx+41,yy+20,center[0],center[1],HexColor('#9AAEA8'),0.8)
    c.save()

# Create cover and overlays
cover_pdf=TMP/'cover.pdf'; make_cover(cover_pdf)
for n in range(2,17):
    overlay_for_page(n,TMP/f'ov-{n:02d}.pdf')

base=PdfReader(str(BASE)); writer=PdfWriter()
cover=PdfReader(str(cover_pdf)).pages[0]
writer.add_page(cover)
for idx in range(1,len(base.pages)):
    page=base.pages[idx]
    n=idx+1
    ov_path=TMP/f'ov-{n:02d}.pdf'
    if ov_path.exists():
        ov=PdfReader(str(ov_path)).pages[0]
        page.merge_page(ov)
    writer.add_page(page)
with OUT.open('wb') as fh: writer.write(fh)
print(OUT)