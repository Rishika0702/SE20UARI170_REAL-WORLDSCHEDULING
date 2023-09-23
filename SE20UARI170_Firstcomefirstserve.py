from datetime import datetime

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def main():
    processes_data = [
        ("A", "00:00", 30),
        ("B", "00:10", 20),
        ("C", "00:15", 40),
        ("D", "00:20", 15)
    ]

    processes = []

    for i, data in enumerate(processes_data):
        pid, arrival_time_str, burst_time = data
        arrival_time_minutes = time_to_minutes(arrival_time_str)
        processes.append(Process(pid, arrival_time_minutes, burst_time))

    processes.sort(key=lambda x: x.arrival_time)

    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0
    total_idle_time = 0

    for i, process in enumerate(processes):
        process.start_time = max(process.arrival_time, processes[i-1].completion_time if i > 0 else process.arrival_time)
        process.completion_time = process.start_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.start_time - process.arrival_time

        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time
        total_response_time += process.response_time
        total_idle_time += process.arrival_time if i == 0 else process.start_time - processes[i-1].completion_time

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
    avg_response_time = total_response_time / len(processes)
    cpu_utilization = ((processes[-1].completion_time - total_idle_time) / processes[-1].completion_time) * 100

    throughput = len(processes) / (processes[-1].completion_time - processes[0].arrival_time)

    print("\n#P\tAT\tBT\tST\tCT\tTAT\tWT\tRT\n")
    for process in processes:
        arrival_time_str = f"{process.arrival_time // 60:02d}:{process.arrival_time % 60:02d}"
        start_time_str = f"{process.start_time // 60:02d}:{process.start_time % 60:02d}"
        completion_time_str = f"{process.completion_time // 60:02d}:{process.completion_time % 60:02d}"
        print(f"{process.pid}\t{arrival_time_str}\t{process.burst_time}\t{start_time_str}\t{completion_time_str}\t{process.turnaround_time}\t{process.waiting_time}\t{process.response_time}\n")

    print(f"Average Turnaround Time = {avg_turnaround_time:.2f}")
    print(f"Average Waiting Time = {avg_waiting_time:.2f}")
    print(f"Average Response Time = {avg_response_time:.2f}")
    print(f"CPU Utilization = {cpu_utilization:.2f}%")
    print(f"Throughput = {throughput:.2f} process/unit time")

if __name__ == "__main__":
    main()
