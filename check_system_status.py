import subprocess
import platform
import time
import os

def is_system_rebooting():
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['systeminfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            uptime_info = result.stdout.split('\n')
            for line in uptime_info:
                if "System Boot Time" in line:
                    boot_time_str = line.split(":")[1].strip()
                    boot_time_str = boot_time_str.split(",")[0]
                    boot_time = time.strptime(boot_time_str, "%m/%d/%Y")
                    current_time = time.time()
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
        if platform.system() == "Windows":
            command = ['ping', '-n', '1', '-w', '1000', ip_address]
        else:
            command = ['ping', '-c', '1', '-W', '1', ip_address]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

ip_address = os.getenv('ip_address', '192.168.1.14')
if is_system_online(ip_address) and not is_system_rebooting():
    print(f"The system {ip_address} is online.")
    os.environ['SystemStatus'] = 'online'
else:
    print(f"The system {ip_address} is either offline or rebooting.")
    os.environ['SystemStatus'] = 'offline'
