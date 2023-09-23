from datetime import datetime

class Process:
    def __init__(self, pid, arrival_time, burst_time_str):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time_str = burst_time_str
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

    def convert_burst_time(self):
        # Parse the burst time string and convert it to minutes
        parts = self.burst_time_str.split()
        minutes = int(parts[0])
        if parts[1].lower().startswith("hour"):
            minutes *= 60
        return minutes

def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def main():
    processes_data = [
        ("A", "00:00", "30 minutes"),
        ("B", "00:10", "20 minutes"),
        ("C", "00:15", "40 minutes"),
        ("D", "00:20", "15 mins")
    ]

    processes = []

    for i, data in enumerate(processes_data):
        pid, arrival_time_str, burst_time_str = data
        arrival_time = time_to_minutes(arrival_time_str)
        process = Process(pid, arrival_time, burst_time_str)
        processes.append(process)

    processes.sort(key=lambda x: x.arrival_time)

    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    total_idle_time = 0

    current_time = 0
    completed = 0
    prev = 0

    while completed != len(processes):
        idx = -1
        mn = float("inf")
        for i in range(len(processes)):
            if processes[i].arrival_time <= current_time:
                if processes[i].convert_burst_time() < mn:
                    mn = processes[i].convert_burst_time()
                    idx = i
                if processes[i].convert_burst_time() == mn:
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        mn = processes[i].convert_burst_time()
                        idx = i

        if idx != -1:
            processes[idx].start_time = current_time
            burst_time_minutes = processes[idx].convert_burst_time()
            processes[idx].completion_time = processes[idx].start_time + burst_time_minutes
            processes[idx].turnaround_time = processes[idx].completion_time - processes[idx].arrival_time
            processes[idx].waiting_time = processes[idx].turnaround_time - burst_time_minutes
            processes[idx].response_time = processes[idx].start_time - processes[idx].arrival_time

            total_turnaround_time += processes[idx].turnaround_time
            total_waiting_time += processes[idx].waiting_time
            total_response_time += processes[idx].response_time
            total_idle_time += processes[idx].start_time - prev

            completed += 1
            current_time = processes[idx].completion_time
            prev = current_time
        else:
            current_time += 1

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_response_time = total_response_time / len(processes)
    cpu_utilization = ((current_time - total_idle_time) / current_time) * 100
    throughput = len(processes) / current_time

    print("\n#P\tAT\tBT\tST\tCT\tTAT\tWT\tRT\n")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time_str}\t{process.start_time}\t{process.completion_time}\t{process.turnaround_time}\t{process.waiting_time}\t{process.response_time}\n")

    print(f"Average Turnaround Time = {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time = {avg_waiting_time:.2f}")
    print(f"Average Response Time = {avg_response_time:.2f}")
    print(f"CPU Utilization = {cpu_utilization:.2f}%")
    print(f"Throughput = {throughput:.2f} process/unit time")


if __name__ == "__main__":
    main()
