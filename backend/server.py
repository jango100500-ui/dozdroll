"""
REAL-EXPERIMENT BRIDGE
----------------------
This is deliberately NOT a fake neural API. It is a small HTTP bridge for a
local instance of the published FlyWire/Shiu/fly-api stack.

The browser never decides that the fly pressed REROLL. The server's simulator
must return a motor/arrival event. The web UI only visualizes that event.

Install the real stack described in docs/REAL_SETUP.md, then replace the
`SimulatorAdapter` methods with the exact experiment runner from your checked-
out fly-api revision. Keeping this seam explicit prevents us from pretending
that a hand-coded JS animation is the connectome.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json, time, math, os

class SimulatorAdapter:
    def __init__(self):
        self.running=False; self.trial=0; self.presses=0; self.reward=0
        self.x=-4.0; self.z=0.0; self.last=time.time()
        self.brain="NOT CONNECTED"
        self.mode=os.getenv("FLY_SIM_MODE","real")
    def start(self):
        self.running=True; self.brain="REAL SIM BRIDGE"; return self.state("started")
    def stop(self):
        self.running=False; return self.state("stopped")
    def step(self,dt_ms):
        # SAFETY: In real mode we do not invent neural activity. Until a real
        # simulator adapter is installed, the server reports "NOT CONNECTED".
        if self.mode!="demo":
            return self.state("waiting for real simulator adapter")
        # Optional visual smoke-test only; never call this "brain activity".
        if self.running:
            self.x += 0.018
            if self.x >= 2.65:
                self.x=-4; self.trial+=1; self.presses+=1; self.reward+=1
                return self.state("DEMO ONLY: fly reached REROLL; reward injected")
        return self.state(None)
    def state(self,event=None):
        return {"ok":True,"brain":self.brain,"trial":self.trial,"presses":self.presses,
                "reward":self.reward,"fly":{"x":self.x,"z":self.z},"event":event}

sim=SimulatorAdapter()
class H(BaseHTTPRequestHandler):
    def send(self,obj):
        b=json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        n=int(self.headers.get("Content-Length","0")); body=self.rfile.read(n)
        try: data=json.loads(body or b"{}")
        except: data={}
        if self.path=="/start": self.send(sim.start())
        elif self.path=="/stop": self.send(sim.stop())
        elif self.path=="/step": self.send(sim.step(data.get("dt_ms",250)))
        else: self.send({"ok":False,"error":"unknown endpoint"})
    def log_message(self,*a): pass

print("Fly REROLL bridge: http://localhost:8765")
print("REAL mode is intentionally inert until the fly-api adapter is connected.")
print("For a visual smoke test: FLY_SIM_MODE=demo python server.py")
ThreadingHTTPServer(("0.0.0.0",8765),H).serve_forever()
