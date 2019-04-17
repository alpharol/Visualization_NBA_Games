import argparse
import pandas as pd
from Event import *
from Elements import Team


class Competition:
    
    """读取文件"""
    
    def __init__(self, path_to_json, event_index):
        
        """设置参数：路径、事件"""
        
        self.home_team = None
        self.guest_team = None
        self.event = None
        self.path_to_json = path_to_json
        self.event_index = event_index

    def data(self):
        #读取json文件
        data_frame = pd.read_json(self.path_to_json)
        last_default_index = len(data_frame) - 1
        self.event_index = min(self.event_index, last_default_index)
        index = self.event_index
        
        event = data_frame['events'][index]
        self.event = Event(event)
        self.home_team = Team(event['home']['teamid'])
        self.guest_team = Team(event['visitor']['teamid'])

    def anishow(self):
        #展示动画
        self.event.show()

"""
设置运行参数：
--path=  #文件路径
--event= #所选攻防回合
"""
parser = argparse.ArgumentParser(description='设置输入时的参数')
parser.add_argument('--path', type=str,
                    help='原始数据的路径（将文件放在根目录下后使用相对路径）',
                    required = True)
parser.add_argument('--event', type=int, default=0,
                    help='选择比赛中的一个时间段绘制视频')

args = parser.parse_args()

#执行文件
Sport_ani = Competition(path_to_json=args.path, event_index=args.event)
Sport_ani.data()
Sport_ani.anishow()

