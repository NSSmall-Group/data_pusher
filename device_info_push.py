# -*- coding: utf-8 -*-
import requests
import psutil
import uuid
import socket
import platform
import json
from typing import List, Dict
from datetime import datetime
import time
import serial

from api.device_api import push_device_info
from config import SUBNET_ID, DEVICE_TYPE, DEVICE_ID, LOCATION_TYPE, SERIAL_PORT, BAUD_RATE, POSITION_CHANGE_THRESHOLD

# 用于存储上一次的坐标
last_position = None

# 获取设备的唯一标识（可以使用 MAC 地址或者 UUID）
def get_device_id() -> str:
    # # 获取设备的 MAC 地址（如果可能）
    # mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)])
    # # 如果获取不到 MAC 地址，使用系统的 UUID
    # if mac:
    #     return mac
    return DEVICE_ID


# 获取设备类型（根据系统或设备的配置进行映射）
def get_device_type() -> int:
    return DEVICE_TYPE


# 获取设备的网络信息（如 IP 地址、子网）
def get_subnet_info() -> str:
    # ip_address = socket.gethostbyname(socket.gethostname())
    # subnet_id = ip_address.split('.')[0] + "." + ip_address.split('.')[1]  # 仅根据 IP 的前两段生成子网编号
    return SUBNET_ID


# 获取设备状态（通过网络接口或自定义的逻辑判断）
def get_device_status() -> int:
    # 示例：如果设备的网络连接正常，则返回状态 1（正常）
    if psutil.net_if_addrs():
        return 1  # 设备在线
    return 0  # 设备离线


# 获取设备位置信息（如果有 GPS 或其他定位服务，获取具体位置）
def get_location_info(position) -> Dict[str, float]:
    if LOCATION_TYPE == 1:
        location_info = {
            "x": position[0],
            "y": position[1],
            "z": position[2]
        }
    else:
        location_info = {
            "latitude": 34.052235,  # 假设坐标
            "longitude": -118.243683,
            "altitude": 93.0
        }
    return location_info

# 判断位置变化是否超过阈值
def is_position_changed(new_position):
    global last_position
    if last_position is None:
        last_position = new_position
        return True  # 首次位置直接认为有变化
    # 计算 x, y, z 距离的变化
    distance = sum([(new_position[i] - last_position[i]) ** 2 for i in range(3)]) ** 0.5
    if distance > POSITION_CHANGE_THRESHOLD:
        last_position = new_position
        return True
    return False


def parse_kt_line(line: str):
    """
    解析以 '$KT' 开头的定位数据帧
    """
    try:
        parts = line.strip().split(',')
        if not parts[0].startswith("$KT"):
            return None
        role = parts[0][1:]  # 去掉 $
        distances = [None if p == 'NULL' else float(p) for p in parts[1:5]]
        coord_part = parts[5] if len(parts) > 5 else ""
        pos = None
        if coord_part.startswith("LO=[") and coord_part.endswith("]"):
            pos_str = coord_part[4:-1]
            pos = [float(x) for x in pos_str.split(',')]

        return {
            "type": "kt",
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "distances_m": distances,
            "position": pos
        }
    except Exception as e:
        print(f"解析 KT 帧错误: {e}")
        return None

# 生成设备信息并推送
def generate_device_info(position) -> List[Dict]:
    device_id = get_device_id()
    device_type = get_device_type()
    subnet_id = get_subnet_info()
    status = get_device_status()
    location_info = get_location_info(position)

    # 设备信息列表
    device_info = [
        {
            "device_id": device_id,
            "device_type": device_type,
            "subnet_id": subnet_id,
            "status": status,
            "location_type": LOCATION_TYPE,  # 假设设备位置信息是 GPS 坐标
            "location_info": location_info
        }
    ]
    return device_info


# 推送设备信息到服务器
def push_device_info_to_server(position):
    device_info = generate_device_info(position)
    response = push_device_info(device_info)
    print("Device Info Push Response:", response)


if __name__ == "__main__":
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"[+] 正在监听串口 {SERIAL_PORT}（115200 8N1）")

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            if line.startswith("$KT"):
                parts = line.strip().split(',')
                coord_part = parts[5:]  # 去掉 $

                
                position = [0]*3
                if coord_part[0].startswith("LO=[") and coord_part[2].endswith("]"):
                    position[0] = float(coord_part[0][4:])
                    position[1] = float(coord_part[1])
                    position[2] = float(coord_part[2][:-1])
                    print(f"读取到定位数据: {position}")

                    if is_position_changed(position):
                        push_device_info_to_server(position)

        except KeyboardInterrupt:
            print("\n[-] 停止监听")
            break
        except Exception as e:
            print(f"[!] 错误: {e}")
        time.sleep(1)

#sudo /home/net2/anaconda3/envs/data_pusher/bin/python device_info_push.py
