import psutil
import os
import time

def display_cpu_stats():
    print("Debug: Fetching CPU stats...")
    
    # CPU Info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_times_percent = psutil.cpu_times_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    
    print(f"Total CPU Cores: {cpu_count}")
    print(f"CPU Usage: {cpu_percent}%")
    print(f"CPU Times Percent: User={cpu_times_percent.user}%, System={cpu_times_percent.system}%, Idle={cpu_times_percent.idle}%")
    print(f"CPU Frequency: Current={cpu_freq.current} MHz, Min={cpu_freq.min} MHz, Max={cpu_freq.max} MHz")
    
    print("Debug: CPU stats fetched.")

if __name__ == "__main__":
    # Display CPU stats
    display_cpu_stats()
