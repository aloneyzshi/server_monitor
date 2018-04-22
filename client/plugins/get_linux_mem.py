import psutil
import  datetime
def get_linux_mem():
    sys_mem = {}
    mem = psutil.virtual_memory()
    sys_mem["total"] = mem.total / 1024 / 1024
    sys_mem["percent"] = mem.percent
    sys_mem["available"] = mem.available / 1024 / 1024
    sys_mem["used"] = mem.used / 1024 / 1024
    sys_mem["free"] = mem.free / 1024 / 1024
    #sys_mem["buffers"] = mem.buffers / 1024 / 1024
    #sys_mem["cached"] = mem.cached / 1024 / 1024
    print sys_mem
    return sys_mem


if __name__ == '__main__':
    print get_linux_mem()