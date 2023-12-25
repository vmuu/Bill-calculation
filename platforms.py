import platform
import hashlib
#import message
#机器码获取
def get_cpu_id():
    try:
        if platform.system() == "Windows":
            # 在Windows系统上获取CPU信息
            import wmi
            c = wmi.WMI()
            cpu_info = c.Win32_Processor()[0]
            cpu_id = cpu_info.ProcessorId.strip()
            cpu_id = cpu_id[0:1]+"F"+cpu_id[1:2]+"C"+cpu_id[2:3]+"X"+cpu_id[3:]
        elif platform.system() == "Linux":
            # 在Linux系统上获取CPU信息
            with open('/proc/cpuinfo', 'r') as file:
                cpu_info = file.read()
                cpu_id = hashlib.md5(cpu_info.encode()).hexdigest()
                cpu_id = cpu_id[0:1] + "F" + cpu_id[1:2] + "C" + cpu_id[2:3] + "X" + cpu_id[3:]
        else:
            # 其他操作系统的处理
            cpu_id = "Unknown"
        return cpu_id
    except Exception as e:
        return str(e)

# def hardwareid():
#     hardware_id = get_cpu_id()
#     if hardware_id:
#         print(f'计算机的硬件码（Hardware ID）：{hardware_id}')
#     else:
#         print('无法获取硬件码')

if __name__ == '__main__':
    hardware_id = get_cpu_id()
    if hardware_id:
        print(f'计算机的硬件码（Hardware ID）：{hardware_id}')
    else:
        print('无法获取硬件码')
    #message.massage(hardware_id)