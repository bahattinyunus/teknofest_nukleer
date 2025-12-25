import sys
import time
import os
import threading
from reactor_core import ReactorCore

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard(reactor):
    status = reactor.get_status()
    clear_screen()
    print("="*60)
    print(f"       ☢️  REACTOR CONTROL CENTER: {reactor.config.get('reactor_name')} ☢️")
    print("="*60)
    print(f" [STATUS]      {status['scram']}")
    print(f" [POWER]       {status['power']}  |  [FLUX]  {status['flux']}")
    print("-" * 60)
    print(f" [TEMPERATURE] {status['temp']}  (Limit: {reactor.config['thresholds']['critical_temp']}K)")
    print(f" [PRESSURE]    {status['press']}  (Limit: {reactor.config['thresholds']['max_pressure']} bar)")
    print("-" * 60)
    print(f" [RODS POS]    {status['rods']}  [1: Up, 0: Down]")
    print(f" [COOLANT]     {status['coolant']}  [W: Inc, S: Dec]")
    print("="*60)
    print(" Commands: [R <pos>] set Rods, [C <flow>] set Coolant, [S] SCRAM, [Q] Quiet")
    print("="*60)

def control_thread(reactor):
    while not reactor.scram_active:
        try:
            cmd = input().strip().upper()
            if cmd.startswith('R'):
                val = int(cmd.split()[1])
                reactor.update_control_rods(val)
            elif cmd.startswith('C'):
                val = int(cmd.split()[1])
                reactor.update_coolant_flow(val)
            elif cmd == 'S':
                reactor.emergency_shutdown("MANUAL USER SCRAM")
            elif cmd == 'Q':
                break
        except Exception:
            pass

def main():
    reactor = ReactorCore()
    
    # Start input thread
    t = threading.Thread(target=control_thread, args=(reactor,), daemon=True)
    t.start()
    
    try:
        while True:
            reactor.step()
            render_dashboard(reactor)
            time.sleep(1)
            if reactor.scram_active:
                render_dashboard(reactor)
                print("\n[SYSTEM] SEVERE MALFUNCTION OR MANUAL SHUTDOWN DETECTED.")
                print("[SYSTEM] PERSISTENT LOGS SAVED TO /logs/reactor.log")
                break
    except KeyboardInterrupt:
        reactor.emergency_shutdown("KEYBOARD INTERRUPT")
        render_dashboard(reactor)

if __name__ == "__main__":
    main()
