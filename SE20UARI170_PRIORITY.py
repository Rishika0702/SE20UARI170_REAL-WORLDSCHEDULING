from datetime import datetime

class Process:
    def __init__(self, pid, arrival_time_str, burst_time_str, priority):
        self.pid = pid
        self.arrival_time_str = arrival_time_str
        self.burst_time_str = burst_time_str
        self.priority = priority
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


    def convert_burst_time(self):
        parts = self.burst_time_str.split()
        minutes = int(parts[0])
        if parts[1].lower().startswith("hour"):
            minutes *= 60
        return minutes

def main():
    processes_data = [
        ("A", "00:00", "30 minutes", 3),
        ("B", "00:10", "20 minutes", 5),
        ("C", "00:15", "40 minutes", 2),
        ("D", "00:20", "15 mins", 4)
    ]

    processes = []

    for i, data in enumerate(processes_data):
        pid, arrival_time_str, burst_time_str, priority = data
        process = Process(pid, arrival_time_str, burst_time_str, priority)
        processes.append(process)

    processes.sort(key=lambda x: (x.priority, time_to_minutes(x.arrival_time_str)))

    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    total_idle_time = 0

    current_time = 0
    completed = 0
    prev = 0

    while completed != len(processes):
        idx = -1
        mx_priority = -1
        for i in range(len(processes)):
            if time_to_minutes(processes[i].arrival_time_str) <= current_time:
                if processes[i].priority > mx_priority:
                    mx_priority = processes[i].priority
                    idx = i
                if processes[i].priority == mx_priority:
                    if time_to_minutes(processes[i].arrival_time_str) < time_to_minutes(processes[idx].arrival_time_str):
                        mx_priority = processes[i].priority
                        idx = i

        if idx != -1:
            processes[idx].start_time = current_time
            burst_time_minutes = processes[idx].convert_burst_time()
            processes[idx].completion_time = processes[idx].start_time + burst_time_minutes
            processes[idx].turnaround_time = processes[idx].completion_time - time_to_minutes(processes[idx].arrival_time_str)
            processes[idx].waiting_time = processes[idx].turnaround_time - burst_time_minutes
            processes[idx].response_time = processes[idx].start_time - time_to_minutes(processes[idx].arrival_time_str)

            total_turnaround_time += processes[idx].turnaround_time
            total_waiting_time += processes[idx].waiting_time
            total_response_time += processes[idx].response_time
            total_idle_time += processes[idx].start_time - prev

            completed += 1
            current_time = processes[idx].completion_time
            prev = current_time
        else:
            current_time += 1

    min_arrival_time = float("inf")
    max_completion_time = -1
    for i in range(len(processes)):
        min_arrival_time = min(min_arrival_time, time_to_minutes(processes[i].arrival_time_str))
        max_completion_time = max(max_completion_time, processes[i].completion_time)

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
   
    print(f"Average Turnaround Time = {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time = {avg_waiting_time:.2f}")
 
def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

if __name__ == "__main__":
    main()
