#设备推送
import subprocess
import json
import time
from typing import List, Dict, Optional
from datetime import datetime

from api.net_api import push_topology


# 假设你已经有了推送函数
def post(endpoint: str, data: dict) -> dict:
    # 示例函数：模拟 HTTP 请求
    print(f"POST {endpoint}: {json.dumps(data, indent=2)}")
    # 在实际情况中，可以使用 requests 库发送 POST 请求
    # response = requests.post(url, json=data, headers=HEADERS)
    # return response.json()
    return {"status": "success"}  # 返回一个模拟成功响应


# 获取 conntrack 命令输出的连接信息
def get_active_connections():
    result = subprocess.run(['conntrack', '-L', '--state', 'NEW'], stdout=subprocess.PIPE)
    return result.stdout.decode()


# 解析 conntrack 输出
def parse_connections(data):
    connections = []
    for line in data.splitlines():
        # 每行数据格式例如：
        # ipv4  2 udp  17  12345 src=192.168.1.10 dst=192.168.1.20 sport=12345 dport=80 [UNREPLIED]
        parts = line.split()
        if len(parts) < 6:
            continue
        # 提取五元组信息
        src_ip = parts[4].split('=')[1]
        dst_ip = parts[5].split('=')[1]
        sport = parts[6].split('=')[1]
        dport = parts[7].split('=')[1]
        # 记录连接信息
        connections.append({
            "source_ip": src_ip,
            "target_ip": dst_ip,
            "source_port": sport,
            "target_port": dport,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return connections

# 上报主动连接信息
def report_connections():
    data = get_active_connections()
    connections = parse_connections(data)

    if connections:
        # 生成拓扑的边（通信路径）
        edges = [
            {"operation": 0, "source_device_id": conn["source_ip"], "target_device_id": conn["target_ip"]}
            for conn in connections
        ]

        # 生成拓扑的通信记录（community）
        community = [
            {
                "timestamp": conn["timestamp"],
                "source_device_id": conn["source_ip"],
                "target_device_id": conn["target_ip"]
            }
            for conn in connections
        ]

        # 推送拓扑数据
        response = push_topology(edges=edges, community=community)
        print("Push Topology Response:", response)
    else:
        print("No active connections found.")


# 每 10 秒检查一次
if __name__ == "__main__":
    while True:
        report_connections()
        time.sleep(3)

# 依赖安装
# sudo apt-get update
# sudo apt-get install conntrack
