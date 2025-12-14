import csv
import sys

#  PRIORITY MAP

PRIORITY_MAP = {
    "high": 1,
    "normal": 2,
    "low": 3
}

#  CSV DOSYASINDAN PROCESS OKUMA

def load_processes(path):
    processes = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arrival = int(row["Arrival_Time"])
            burst = int(row["CPU_Burst_Time"])
            priority_str = row["Priority"].strip().lower()

            processes.append({
                "pid": row["Process_ID"],
                "arrival": arrival,
                "burst": burst,
                "remaining": burst,
                "priority": PRIORITY_MAP[priority_str],
                "start": None,
                "finish": None,
                "waiting": 0,
                "turnaround": 0
            })
    return processes

#  CONTEXT SWITCH SAYISI

def count_context_switches(timeline):
    non_idle = [slot for slot in timeline if slot["pid"] != "IDLE"]
    if len(non_idle) <= 1:
        return 0
    return len(non_idle) - 1

#  CPU VERİMLİLİĞİ HESABI

def compute_cpu_times(timeline, context_switches, cost=0.001):
    if not timeline:
        return 0, 0, 0, 0

    total_time = timeline[-1]["end"]
    busy_time = sum(slot["end"] - slot["start"] for slot in timeline if slot["pid"] != "IDLE")
    idle_time = total_time - busy_time
    overhead = context_switches * cost

    efficiency = busy_time / (total_time + overhead) if total_time > 0 else 0
    return total_time, busy_time, idle_time, efficiency

#  FCFS

def run_fcfs(original):
    processes = [p.copy() for p in original]
    processes.sort(key=lambda p: p["arrival"])

    timeline = []
    current_time = 0.0

    for p in processes:
        arrival = p["arrival"]
        burst = p["burst"]

        if current_time < arrival:
            timeline.append({
                "start": current_time,
                "end": float(arrival),
                "pid": "IDLE"
            })
            current_time = float(arrival)

        p["start"] = current_time
        finish = current_time + burst

        timeline.append({
            "start": current_time,
            "end": finish,
            "pid": p["pid"]
        })

        p["finish"] = finish
        p["waiting"] = p["start"] - p["arrival"]
        p["turnaround"] = p["finish"] - p["arrival"]
        p["remaining"] = 0

        current_time = finish

    cs = count_context_switches(timeline)
    return processes, timeline, cs

#  SJF NON-PREEMPTIVE

def run_sjf_nonpreemptive(original):
    processes = [p.copy() for p in original]
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["waiting"] = 0
        p["turnaround"] = 0

    timeline = []
    current_time = 0.0

    while True:
        ready = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]
        if not ready:
            not_arrived = [p for p in processes if p["remaining"] > 0]
            if not not_arrived:
                break
            next_arrival = min(p["arrival"] for p in not_arrived)
            if current_time < next_arrival:
                timeline.append({
                    "start": current_time,
                    "end": float(next_arrival),
                    "pid": "IDLE"
                })
            current_time = float(next_arrival)
            continue

        p = min(ready, key=lambda x: x["burst"])

        if p["start"] is None:
            p["start"] = current_time

        run_time = p["remaining"]
        finish = current_time + run_time

        timeline.append({
            "start": current_time,
            "end": finish,
            "pid": p["pid"]
        })

        p["remaining"] = 0
        p["finish"] = finish
        p["waiting"] = p["start"] - p["arrival"]
        p["turnaround"] = p["finish"] - p["arrival"]

        current_time = finish

    cs = count_context_switches(timeline)
    return processes, timeline, cs

#  SJF PREEMPTIVE (SRTF)

def run_sjf_preemptive(original):
    processes = [p.copy() for p in original]
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["waiting"] = 0
        p["turnaround"] = 0

    timeline = []
    current_time = 0
    current_pid = None
    slot_start = 0

    total_remaining = sum(p["remaining"] for p in processes)

    while total_remaining > 0:
        ready = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]

        if not ready:

            next_arrival = min(p["arrival"] for p in processes if p["remaining"] > 0)
            if current_pid is not None:

                timeline.append({
                    "start": slot_start,
                    "end": current_time,
                    "pid": current_pid
                })
                current_pid = None

            timeline.append({
                "start": current_time,
                "end": float(next_arrival),
                "pid": "IDLE"
            })
            current_time = int(next_arrival)
            slot_start = current_time
            continue


        p = min(ready, key=lambda x: x["remaining"])

        if current_pid != p["pid"]:
            if current_pid is not None:
                timeline.append({
                    "start": slot_start,
                    "end": float(current_time),
                    "pid": current_pid
                })
            current_pid = p["pid"]
            slot_start = current_time

        if p["start"] is None:
            p["start"] = float(current_time)


        p["remaining"] -= 1
        current_time += 1
        total_remaining = sum(pp["remaining"] for pp in processes)

        if p["remaining"] == 0:
            p["finish"] = float(current_time)
            p["waiting"] = p["finish"] - p["arrival"] - p["burst"]
            p["turnaround"] = p["finish"] - p["arrival"]

    if current_pid is not None:
        timeline.append({
            "start": float(slot_start),
            "end": float(current_time),
            "pid": current_pid
        })

    cs = count_context_switches(timeline)
    return processes, timeline, cs


#  ROUND ROBIN

def run_round_robin(original, quantum):
    processes = [p.copy() for p in original]
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["waiting"] = 0
        p["turnaround"] = 0

    processes.sort(key=lambda p: p["arrival"])

    timeline = []
    current_time = 0.0
    queue = []
    i = 0 


    if processes:
        current_time = float(processes[0]["arrival"])

    while True:

        while i < len(processes) and processes[i]["arrival"] <= current_time:
            queue.append(processes[i])
            i += 1

        if not queue:
            if i >= len(processes):
                break
            next_arrival = processes[i]["arrival"]
            if current_time < next_arrival:
                timeline.append({
                    "start": current_time,
                    "end": float(next_arrival),
                    "pid": "IDLE"
                })
            current_time = float(next_arrival)
            continue

        p = queue.pop(0)

        if p["start"] is None:
            p["start"] = current_time

        run_time = min(quantum, p["remaining"])
        start = current_time
        end = current_time + run_time

        timeline.append({
            "start": start,
            "end": end,
            "pid": p["pid"]
        })

        current_time = end
        p["remaining"] -= run_time

        while i < len(processes) and processes[i]["arrival"] <= current_time:
            queue.append(processes[i])
            i += 1

        if p["remaining"] > 0:
            queue.append(p)
        else:
            p["finish"] = current_time
            p["waiting"] = p["finish"] - p["arrival"] - p["burst"]
            p["turnaround"] = p["finish"] - p["arrival"]

    cs = count_context_switches(timeline)
    return processes, timeline, cs


#  PRIORITY NON-PREEMPTIVE

def run_priority_nonpreemptive(original):
    processes = [p.copy() for p in original]
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["waiting"] = 0
        p["turnaround"] = 0

    timeline = []
    current_time = 0.0

    while True:
        ready = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]
        if not ready:
            not_arrived = [p for p in processes if p["remaining"] > 0]
            if not not_arrived:
                break
            next_arrival = min(p["arrival"] for p in not_arrived)
            if current_time < next_arrival:
                timeline.append({
                    "start": current_time,
                    "end": float(next_arrival),
                    "pid": "IDLE"
                })
            current_time = float(next_arrival)
            continue

        p = min(ready, key=lambda x: (x["priority"], x["arrival"]))

        if p["start"] is None:
            p["start"] = current_time

        run_time = p["remaining"]
        finish = current_time + run_time

        timeline.append({
            "start": current_time,
            "end": finish,
            "pid": p["pid"]
        })

        p["remaining"] = 0
        p["finish"] = finish
        p["waiting"] = p["start"] - p["arrival"]
        p["turnaround"] = p["finish"] - p["arrival"]

        current_time = finish

    cs = count_context_switches(timeline)
    return processes, timeline, cs

#  PRIORITY PREEMPTIVE

def run_priority_preemptive(original):
    processes = [p.copy() for p in original]
    for p in processes:
        p["remaining"] = p["burst"]
        p["start"] = None
        p["finish"] = None
        p["waiting"] = 0
        p["turnaround"] = 0

    timeline = []
    current_time = 0
    current_pid = None
    slot_start = 0

    total_remaining = sum(p["remaining"] for p in processes)

    while total_remaining > 0:
        ready = [p for p in processes if p["arrival"] <= current_time and p["remaining"] > 0]

        if not ready:
            next_arrival = min(p["arrival"] for p in processes if p["remaining"] > 0)
            if current_pid is not None:
                timeline.append({
                    "start": slot_start,
                    "end": float(current_time),
                    "pid": current_pid
                })
                current_pid = None

            timeline.append({
                "start": float(current_time),
                "end": float(next_arrival),
                "pid": "IDLE"
            })
            current_time = int(next_arrival)
            slot_start = current_time
            total_remaining = sum(p["remaining"] for p in processes)
            continue


        p = min(ready, key=lambda x: (x["priority"], x["arrival"]))

        if current_pid != p["pid"]:
            if current_pid is not None:
                timeline.append({
                    "start": float(slot_start),
                    "end": float(current_time),
                    "pid": current_pid
                })
            current_pid = p["pid"]
            slot_start = current_time

        if p["start"] is None:
            p["start"] = float(current_time)

        p["remaining"] -= 1
        current_time += 1
        total_remaining = sum(pp["remaining"] for pp in processes)

        if p["remaining"] == 0:
            p["finish"] = float(current_time)
            p["waiting"] = p["finish"] - p["arrival"] - p["burst"]
            p["turnaround"] = p["finish"] - p["arrival"]

    if current_pid is not None:
        timeline.append({
            "start": float(slot_start),
            "end": float(current_time),
            "pid": current_pid
        })

    cs = count_context_switches(timeline)
    return processes, timeline, cs

#  METRİKLERİN HESABI

def compute_metrics(processes, timeline, cs):
    n = len(processes)
    if n == 0:
        return {
            "avg_waiting": 0,
            "max_waiting": 0,
            "avg_turnaround": 0,
            "max_turnaround": 0,
            "throughput": {50: 0, 100: 0, 150: 0, 200: 0},
            "cpu_efficiency": 0,
            "total_time": 0,
            "busy_time": 0,
            "idle_time": 0,
            "context_switches": cs
        }

    avg_wait = sum(p["waiting"] for p in processes) / n
    max_wait = max(p["waiting"] for p in processes)

    avg_ta = sum(p["turnaround"] for p in processes) / n
    max_ta = max(p["turnaround"] for p in processes)

    checkpoints = [50, 100, 150, 200]
    throughput = {}
    for T in checkpoints:
        throughput[T] = sum(1 for p in processes if p["finish"] is not None and p["finish"] <= T)

    total_time, busy_time, idle_time, eff = compute_cpu_times(timeline, cs)

    return {
        "avg_waiting": avg_wait,
        "max_waiting": max_wait,
        "avg_turnaround": avg_ta,
        "max_turnaround": max_ta,
        "throughput": throughput,
        "cpu_efficiency": eff,
        "total_time": total_time,
        "busy_time": busy_time,
        "idle_time": idle_time,
        "context_switches": cs
    }

#  DOSYAYA YAZMA

def write_results(filename, processes, timeline, metrics, algo_name):
    with open(filename, "w", encoding="utf-8") as f:


        f.write(f"Algorithm: {algo_name}\n\n")

        f.write("Zaman Tablosu:\n")
        for slot in timeline:
            f.write(f"[ {slot['start']:.3f} ] - - {slot['pid']} - - [ {slot['end']:.3f} ]\n")

        f.write("\nBekleme Süreleri:\n")
        f.write(f"Ortalama: {metrics['avg_waiting']:.3f}\n")
        f.write(f"Maksimum: {metrics['max_waiting']:.3f}\n\n")

        f.write("Turnaround Süreleri:\n")
        f.write(f"Ortalama: {metrics['avg_turnaround']:.3f}\n")
        f.write(f"Maksimum: {metrics['max_turnaround']:.3f}\n\n")

        f.write("Throughput:\n")
        for T, val in metrics["throughput"].items():
           f.write(f"T = {T} -> {val} islem tamamlandi\n")

        f.write("\n")

        f.write(f"CPU Verimliliği: {metrics['cpu_efficiency']*100:.2f}%\n")
        f.write(f"Toplam Context Switch: {metrics['context_switches']}\n")

        f.write("\nProsesler:\n")
        for p in processes:
            f.write(
                f"{p['pid']}: arrival={p['arrival']}, burst={p['burst']}, "
                f"start={p['start']}, finish={p['finish']}, "
                f"waiting={p['waiting']}, turnaround={p['turnaround']}\n"
            )

#  MAIN

def main():
    if len(sys.argv) < 3:
        print("Kullanım:")
        print("  python main.py <girdi_dosyasi> <algo> [quantum]")
        print("Algo seçenekleri: fcfs, sjf_np, sjf_p, rr, prio_np, prio_p")
        print("RR için: python main.py Odev1_Case1.txt rr 4")
        sys.exit(1)

    input_path = sys.argv[1]
    algo = sys.argv[2].lower()
    quantum = 4
    if algo == "rr" and len(sys.argv) >= 4:
        quantum = int(sys.argv[3])

    processes = load_processes(input_path)

    if algo == "fcfs":
        procs_after, timeline, cs = run_fcfs(processes)
        out_suffix = "fcfs"
        name = "FCFS"
    elif algo == "sjf_np":
        procs_after, timeline, cs = run_sjf_nonpreemptive(processes)
        out_suffix = "sjf_np"
        name = "SJF Non-Preemptive"
    elif algo == "sjf_p":
        procs_after, timeline, cs = run_sjf_preemptive(processes)
        out_suffix = "sjf_p"
        name = "SJF Preemptive"
    elif algo == "rr":
        procs_after, timeline, cs = run_round_robin(processes, quantum)
        out_suffix = f"rr_q{quantum}"
        name = f"Round Robin (q={quantum})"
    elif algo == "prio_np":
        procs_after, timeline, cs = run_priority_nonpreemptive(processes)
        out_suffix = "prio_np"
        name = "Priority Non-Preemptive"
    elif algo == "prio_p":
        procs_after, timeline, cs = run_priority_preemptive(processes)
        out_suffix = "prio_p"
        name = "Priority Preemptive"
    else:
        print("Bilinmeyen algoritma:", algo)
        sys.exit(1)

    metrics = compute_metrics(procs_after, timeline, cs)
    base = input_path.rsplit(".", 1)[0]
    out_file = f"{base}_{out_suffix}.txt"
    write_results(out_file, procs_after, timeline, metrics, name)
    print(f"{name} tamamlandı. Çıktı: {out_file}")

if __name__ == "__main__":
    main()
