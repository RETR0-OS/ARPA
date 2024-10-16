import GPUtil

# Get the list of all GPUs
gpus = GPUtil.getGPUs()

for gpu in gpus:
    print(f"GPU ID: {gpu.id}")
    print(f"Name: {gpu.name}")
    print(f"Memory Total: {gpu.memoryTotal}MB")
    print(f"Memory Free: {gpu.memoryFree}MB")
    print(f"Memory Used: {gpu.memoryUsed}MB")
    print(f"GPU Load: {gpu.load*100}%")
    print(f"GPU Temperature: {gpu.temperature} C")
