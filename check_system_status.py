import subprocess
import platform
import time

def is_system_rebooting():
    try:
        # Get system uptime
        if platform.system() == "Windows":
            result = subprocess.run(['systeminfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            uptime_info = result.stdout.split('\n')
            for line in uptime_info:
                if "System Boot Time" in line:
                    boot_time_str = line.split(":")[1].strip()
                    boot_time_str = boot_time_str.split(",")[0]  # Remove time portion
                    boot_time = time.strptime(boot_time_str, "%m/%d/%Y")
                    current_time = time.time()
                    # If the system was booted less than 5 minutes ago, consider it as rebooting
                    if current_time - time.mktime(boot_time) < 300:
                        return True
                    else:
                        return False
        else:
            result = subprocess.run(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            uptime_info = result.stdout.strip()
            if "load average" in uptime_info:
                return False
            else:
                return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def is_system_online(ip_address):
    try:
        # Choose the appropriate command based on the platform
        if platform.system() == "Windows":
            command = ['ping', '-n', '1', '-w', '1000', ip_address]  # Windows
        else:
            command = ['ping', '-c', '1', '-W', '1', ip_address]  # Unix-like systems

        # Execute the ping command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check the return code
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


ip_address = '192.168.1.14'
if is_system_online(ip_address) and not is_system_rebooting():
    print(f"The system {ip_address} is online.")
    print("##vso[task.setvariable variable=SystemOnline]true")
else:
    print(f"The system {ip_address} is either offline or rebooting.")
    print("##vso[task.setvariable variable=SystemOnline]false")
