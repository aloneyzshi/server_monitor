import psutil
import  datetime
def parser_sys_disk(mountpoint):
    partitions_list = {}
    d = psutil.disk_usage(mountpoint)
    partitions_list['mountpoint'] = mountpoint
    partitions_list['total'] = round(d.total / 1024 / 1024 / 1024.0, 2)
    partitions_list['free'] = round(d.free / 1024 / 1024 / 1024.0, 2)
    partitions_list['used'] = round(d.used / 1024 / 1024 / 1024.0, 2)
    partitions_list['percent'] = d.percent
    return partitions_list

def get_linux_disk():
    sys_disk = {'/dev/sda':'200G','/dev/sdb':'100G'}
    print sys_disk
    return sys_disk

    partition_info = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        partition_info.append(parser_sys_disk(p.mountpoint))
    sys_disk = partition_info
    return sys_disk



if __name__ == '__main__':
    print get_linux_disk()