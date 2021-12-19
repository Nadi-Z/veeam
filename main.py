# Coding task for Veeam: Developer in QA Engineering, Problem 1
# Implemented by: Nadejda Zaharieva, December 2021

# Import external libraries
import subprocess
import psutil

print("Hello!")

# Check if time interval is valid
while True:
    try:
        time_interval = float(input("Please enter the data collection time interval (in seconds): "))
        assert time_interval > 0
        break
    except ValueError:
        print("Time interval must be a real number.")
    except AssertionError:
        print("Time interval must be positive.")

# Check if file path is valid
while True:
    try:
        path = input("Please enter the full path of the executable file: ")
        process = subprocess.Popen(path)
        break
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("File permission denied.")

# Setup
print("Launching application")
p = psutil.Process(process.pid)
command = "lsof -p " + str(process.pid) + " | wc -l"
timer = time_interval

# Open the output file and prepare for data
f = open("output.txt", "w")
f.write("Interval (s)\tCPU usage (%)\tResident Set Size (B)\tVirtual Memory Size (B)\tOpen file descriptors\n")
f.close()
f = open("output.txt", "a")

# While the process is running, write the data to output file each time interval
while psutil.pid_exists(process.pid):
    print("Collecting and writing data (" + str(timer) + "s)")
    f.write(str(timer))
    f.write("\t\t")
    f.write(str(p.cpu_percent(time_interval)))
    f.write("\t\t")
    f.write(str(p.memory_info().rss))
    f.write("\t\t")
    f.write(str(p.memory_info().vms))
    f.write("\t\t")
    f.write(str(subprocess.getoutput(command)))
    f.write("\n")
    timer = timer + time_interval
    process.poll()

# Close output file
f.close()
print("Goodbye!")
