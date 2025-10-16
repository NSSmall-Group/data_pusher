# api.py

from typing import List, Dict, Optional
from client import post


# 中心上传
def push_alerts(alerts: List[Dict]) -> dict:
    """
    推送告警数据
    """
    return post("/netApi/alerts", {"alerts": alerts})


# 中心上传
def push_risk_analysis(risk_analysis: List[Dict]) -> dict:
    """
    推送网络层风险分析数据
    """
    return post("/netApi/riskAnalysis", {"risk_analysis": risk_analysis})


# 中心上传
def push_blacklist(blacklist: List[Dict]) -> dict:
    """
    推送黑名单数据
    """
    return post("/netApi/blacklist", {"blacklist": blacklist})


# 边缘上传
def push_topology(nodes: Optional[List[Dict]] = None,
                  edges: Optional[List[Dict]] = None,
                  community: Optional[List[Dict]] = None) -> dict:
    """
    推送拓扑结构与通信记录
    """
    payload = {}
    # if nodes is not None:
    #     payload["nodes"] = nodes
    if edges is not None:
        payload["edges"] = edges
    if community is not None:
        payload["community"] = community
    return post("/netApi/topology", payload)


# 中心上传
def push_attack_Info(att_info: Dict) -> dict:
    """
    推送攻击数据
    """
    print(att_info)
    return post("/ns3Layer/attackInfo",att_info)



def push_detection_Info(detection_info: List[Dict], trace_info: List[Dict],
                        detection_accuracy_info: List[Dict]) -> dict:
    """
    推送检测数据
    """
    payload = {}
    payload['detection_info'] = detection_info
    payload['trace_info'] = trace_info
    payload['detection_accuracy_info'] = detection_accuracy_info
    
    return post("/ns3Layer/detectionInfo", payload)


def push_topology_ns3(graph_id: str,nodes:List[Dict],edges:List[Dict]) -> dict:
    """
    推送拓扑1数据
    """
    payload = {}
    payload['graph_id'] = graph_id
    payload['nodes'] = nodes
  
    payload['edges'] = edges
    return post("/ns3Layer/topologyInfo", payload)

def push_topology2_ns3(graph_id: str,alla:Dict,sub:Dict) -> dict:
    """
    推送拓扑2数据
    """
    payload = {}
    payload['graph_id'] = graph_id
    payload['all'] = alla
    
    payload['sub'] = sub
    return post("/ns3Layer/topology2Info", payload)

def push_timeLineInfo(timeLine:Dict) -> dict:
    """
    推送时间轴数据
    """
    
    return post("/ns3Layer/timeLineInfo", timeLine)
