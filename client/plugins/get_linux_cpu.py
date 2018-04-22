import psutil
import  datetime
def get_linux_cpu():
    sys_cpu = {}
    cpu_time = psutil.cpu_times_percent(interval=1)
    sys_cpu['percent'] = psutil.cpu_percent(interval=1)
    sys_cpu['user'] = cpu_time.user
    sys_cpu['system'] = cpu_time.system
    sys_cpu['idle'] = cpu_time.idle
    return sys_cpu


if __name__ == '__main__':
    print get_linux_cpu()