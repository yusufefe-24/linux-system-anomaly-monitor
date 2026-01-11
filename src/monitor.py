import time
import statistics

LOG_FILE = "logs/monitor.log"
WINDOW = 6
RATE_THRESHOLD = 2.0   # 2 kat artış alarm

ctxt_rates = []
last_ctxt = None

def read_context_switches():
    with open("/proc/stat") as f:
        for line in f:
            if line.startswith("ctxt"):
                return int(line.split()[1])

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")
    print(msg)

def monitor():
    global last_ctxt

    current_ctxt = read_context_switches()

    if last_ctxt is not None:
        rate = current_ctxt - last_ctxt
        ctxt_rates.append(rate)

        if len(ctxt_rates) > WINDOW:
            ctxt_rates.pop(0)

        if len(ctxt_rates) == WINDOW:
            avg = statistics.mean(ctxt_rates[:-1])
            current = ctxt_rates[-1]

            if avg > 0 and current > avg * RATE_THRESHOLD:
                log(f"ALERT ctxt rate spike: {current} avg:{avg}")
            else:
                log(f"OK ctxt_rate:{current}")

    last_ctxt = current_ctxt

if __name__ == "__main__":
    while True:
        monitor()
        time.sleep(5)
