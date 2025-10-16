# config.py

BASE_URL = "http://192.168.7.99:8090/"  # 修改为实际公网服务地址
# 411104
ACCESS_TOKEN = ""       # 若无需认证，设为空 ""

HEADERS = {
    "Content-Type": "application/json"
}
if ACCESS_TOKEN:
    HEADERS["Authorization"] = f"Bearer {ACCESS_TOKEN}"


DEVICE_ID = "192.168.7.99"  # 设备标识（设备的唯一ID，可以是自定义的标识符）
DEVICE_TYPE = 3            # 设备类型Ⅰ类
SUBNET_ID = "有线网1"      # 子网编号

LOCATION_TYPE = 1           #定位类型（0-室外 1-室内）
# 定位串口配置
SERIAL_PORT = "/dev/ttyUSB0"   # 修改为你的串口名
BAUD_RATE = 115200
OUTPUT_FILE = "uwb_data_log.jsonl"  # 持久化保存路径
# 定义位置变化阈值（可以根据需要调整）
POSITION_CHANGE_THRESHOLD = 0.1  # 位置变化超过 0.1 米时才推送数据
