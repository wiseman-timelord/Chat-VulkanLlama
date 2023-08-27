import psutil
import os

# Declare large_list as a global variable
large_list = None

def allocate_memory(size_gb):
    global large_list
    print("Debug: Allocating memory...")
    # Allocate 1GB of RAM
    # 1 GB = 1024 * 1024 * 1024 bytes
    # We'll create a list of zeros to fill up the memory
    large_list = [0] * (size_gb * 1024 * 1024 * 1024 // 8)  # Each int takes up 8 bytes
    print("Debug: Memory allocated.")

def display_memory_stats():
    global large_list
    print("Debug: Fetching memory stats...")
    
    # Access large_list to ensure it's not garbage collected
    print(f"Debug: First element in large_list: {large_list[0]}")
    
    # Virtual Memory
    virtual_memory = psutil.virtual_memory()
    print(f"Total Virtual Memory (RAM): {virtual_memory.total / (1024 ** 3):.2f} GB")
    print(f"Available Virtual Memory: {virtual_memory.available / (1024 ** 3):.2f} GB")
    print(f"Used Virtual Memory: {virtual_memory.used / (1024 ** 3):.2f} GB")
    print(f"Percent Virtual Memory Used: {virtual_memory.percent}%")
    print(f"Active Virtual Memory: {virtual_memory.active / (1024 ** 3):.2f} GB")
    print(f"Inactive Virtual Memory: {virtual_memory.inactive / (1024 ** 3):.2f} GB")
    print(f"Buffers: {virtual_memory.buffers / (1024 ** 3):.2f} GB")
    print(f"Cached: {virtual_memory.cached / (1024 ** 3):.2f} GB")
    print(f"Shared: {virtual_memory.shared / (1024 ** 3):.2f} GB")
    print(f"Slab: {virtual_memory.slab / (1024 ** 3):.2f} GB")
    
    # Swap Memory
    swap_memory = psutil.swap_memory()
    print(f"Total Swap Memory: {swap_memory.total / (1024 ** 3):.2f} GB")
    print(f"Used Swap Memory: {swap_memory.used / (1024 ** 3):.2f} GB")
    print(f"Free Swap Memory: {swap_memory.free / (1024 ** 3):.2f} GB")
    print(f"Percent Swap Memory Used: {swap_memory.percent}%")
    print(f"Bytes Swapped in: {swap_memory.sin / (1024 ** 3):.2f} GB")
    print(f"Bytes Swapped out: {swap_memory.sout / (1024 ** 3):.2f} GB")
    
    # Process Memory
    process = psutil.Process(os.getpid())
    process_memory_info = process.memory_info()
    print(f"Resident Set Size (RSS) - Memory used by this process: {process_memory_info.rss / (1024 ** 3):.2f} GB")
    print(f"USS: {process.memory_full_info().uss / (1024 ** 3):.2f} GB")
    print(f"PSS: {process.memory_full_info().pss / (1024 ** 3):.2f} GB")
    print(f"Swap: {process.memory_full_info().swap / (1024 ** 3):.2f} GB")
    
    print("Debug: Memory stats fetched.")

if __name__ == "__main__":
    allocate_memory(1)  # Allocate 1 GB of RAM
    display_memory_stats()  # Display memory stats
