import json
from datetime import datetime
from api.net_api import push_attack_Info,push_detection_Info,push_topology_ns3,push_topology2_ns3,push_timeLineInfo



def push_topologyInfo():
    print("上传设备数据")
    path = 'data/6_7.json'
    for n in range(100):
        path = 'json/{}.json'.format(n+1)
        with open(path, 'r', encoding='utf-8') as file:
            print (path)
            device_file = json.load(file)
            nodes = device_file['nodes']
            edges = device_file['edges']
            response= push_topology_ns3('unique_graph_'+str(n+1),nodes,edges)
            print(response)
        print()
        #exit() #用于测试


# 上传告警数据
def push_topologyInfo2():
    print("上传NS3网络拓扑...")
    path = 'data/8.json'
    with open(path, 'r', encoding='utf-8') as file:
        device_file = json.load(file)
        graph_id = device_file['graph_id']
        all = device_file['all']
        sub = device_file['sub']
        # exit() 用于测试
        response = push_topology2_ns3(graph_id,all,sub)
        print("告警数据上传响应:", response)


# 上传风险分析数据1
def push_timeLine():
    print("上传风险分析数据...")
    path = 'data/9.json'
    with open(path, 'r', encoding='utf-8') as file:
        timeLine = json.load(file)
        # print(timeLine)
        # exit() 用于测试
    response = push_timeLineInfo(timeLine)
    print("风险分析数据上传响应:", response)



def push_detection_data():
    # print("上传NS3网络拓扑...")
    path = 'data/10.json'
    with open(path, 'r', encoding='utf-8') as file:
        device_file = json.load(file)
        detection_info = device_file['detection_info']
        trace_info = device_file['trace_info']
        detection_accuracy_info = device_file['detection_accuracy_info']
        # exit() 用于测试
    response = push_detection_Info(detection_info,trace_info,detection_accuracy_info)
    print("告警数据上传响应:", response)


# 上传攻击数据
def push_attack_info():
    print("上传攻击数据...")
    path = 'data/11.json'
    for i in range(100):
        with open(path, 'r', encoding='utf-8') as file:
            att_info = json.load(file)
            att_info["id"] = "unique_graph_"+str(i+1)
            att_info["time"] = att_info.pop("时间")
            att_info["attack_sign"] = att_info.pop("恶意攻击标识")
            att_info["detection_time"] = att_info.pop("检测时长")
            att_info["investigation_time"] = att_info.pop("溯源时长")
            #print(att_info)
            #exit() #用于测试
        response = push_attack_Info(att_info)
    print("风险分析数据上传响应:", response)


# 执行上传操作
if __name__ == "__main__":
    push_topologyInfo()  # 上传攻击检测可视化图
    #push_topologyInfo2()  # 上传NS3拓扑
    #push_timeLine()  # 上传攻击检测评估1
    #push_detection_data()  # 上传攻击检测数据
    #push_attack_info()  # 上传攻击检测评估2

