from typing import List, Dict
from client import post

def push_device_info(device_info: List[Dict]) -> dict:
    """
    推送设备信息数据
    :param device_info: 设备信息列表
    :return: 返回推送结果
    """
    return post("/deviceApi/device", {"device_info": device_info})