from flask import Flask, render_template, request, redirect, url_for, flash, Response
from threading import Thread, Event, Lock
from datetime import datetime
import csv, io, socket, os
try:
    from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, DNS
    SCAPY_OK=True
except Exception:
    SCAPY_OK=False
app=Flask(__name__); app.secret_key=os.environ.get('FLASK_SECRET','local-sniffer-change-me')
packets=[]; lock=Lock(); stop_event=Event(); capture_thread=None; state={'running':False,'iface':'','filter':'','error':''}
MAX_PACKETS=1500

def packet_row(pkt):
    src=dst='—'; proto='OTHER'; sport=dport='—'; length=len(pkt); summary=''
    if IP in pkt: src,dst=pkt[IP].src,pkt[IP].dst
    elif IPv6 in pkt: src,dst=pkt[IPv6].src,pkt[IPv6].dst
    if TCP in pkt: proto='TCP'; sport,dport=str(pkt[TCP].sport),str(pkt[TCP].dport)
    elif UDP in pkt: proto='UDP'; sport,dport=str(pkt[UDP].sport),str(pkt[UDP].dport)
    elif ICMP in pkt: proto='ICMP'
    elif DNS in pkt: proto='DNS'
    try: summary=pkt.summary()
    except Exception: summary='Packet captured'
    return {'time':datetime.now().strftime('%H:%M:%S'),'src':src,'dst':dst,'protocol':proto,'sport':sport,'dport':dport,'length':length,'summary':summary[:180]}

def capture_worker(iface, bpf):
    try:
        def got(pkt):
            row=packet_row(pkt)
            with lock:
                packets.insert(0,row); del packets[MAX_PACKETS:]
        # Short capture windows make stop requests responsive even on quiet interfaces.
        while not stop_event.is_set():
            sniff(iface=iface or None, filter=bpf or None, prn=got, store=False, timeout=1)
    except Exception as e:
        state['error']=str(e)
    finally: state['running']=False

@app.route('/')
def index():
    with lock: rows=list(packets[:100])
    counts={}
    for p in rows: counts[p['protocol']]=counts.get(p['protocol'],0)+1
    return render_template('index.html',title='PacketScope',subtitle='Live packet capture • protocol inspection • exportable evidence',logo='⌁',rows=rows,counts=counts,total=len(packets),running=state['running'],scapy=SCAPY_OK,error=state['error'],iface=state['iface'],bpf=state['filter'])
@app.post('/start')
def start():
    if not SCAPY_OK: flash('Scapy is not installed. Install requirements and Npcap (Windows), then restart.','error'); return redirect(url_for('index'))
    if state['running']: flash('Capture is already running.'); return redirect(url_for('index'))
    iface=request.form.get('iface','').strip() or None; bpf=request.form.get('bpf','').strip()
    state.update(running=True,iface=iface or 'default interface',filter=bpf,error=''); stop_event.clear()
    global capture_thread
    capture_thread=Thread(target=capture_worker,args=(iface,bpf),daemon=True); capture_thread.start()
    flash('Capture started. If no packets appear, verify interface selection and OS capture permissions.'); return redirect(url_for('index'))
@app.post('/stop')
def stop():
    stop_event.set(); state['running']=False; flash('Stop requested. Capture loop exits after the next packet.'); return redirect(url_for('index'))
@app.post('/clear')
def clear():
    with lock: packets.clear()
    state['error']=''; flash('Packet table cleared.'); return redirect(url_for('index'))
@app.get('/export.csv')
def export():
    with lock: rows=list(packets)
    out=io.StringIO(); writer=csv.DictWriter(out,fieldnames=['time','src','dst','protocol','sport','dport','length','summary']); writer.writeheader(); writer.writerows(rows)
    return Response(out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=packetscope_capture.csv'})
if __name__=='__main__': app.run(host='127.0.0.1',port=5001,debug=False,threaded=True)
