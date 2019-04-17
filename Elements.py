"""
本项目旨在从NBA比赛中的log文件模拟还原一场比赛

首先我们定义一些篮球比赛中必须会用到的项目，如篮球、球队、队员等
"""

class Team:
    
    """以字典的格式对NBA各只球队的定义：颜色、名称、球队ID"""
    
    """在本项目只定义了4只球队，分别是克利夫兰骑士队、金州勇士队、洛杉矶湖人队、俄克拉荷马城雷霆队"""
    
    Team_details = {
        1610612739: ('#860038', 'CLE'),   #key是球队的ID, value中的第一项是颜色,第二项是球队名称
        1610612744: ('#FDB927', 'GSW'),
        1610612747: ('#552582', 'LAL'),
        1610612760: ('#007DC3', 'OKC'),
    }

    def __init__(self, id):
        self.id = id
        #根据球队ID提取出球队的颜色和名称
        self.color = Team.Team_details[id][0]
        self.name = Team.Team_details[id][1]



class Basketball:
    
    """定义篮球比赛中的篮球"""
    
    def __init__(self, ball):
        #定义篮球的位置
        self.x = ball[2]
        self.y = ball[3]
        #定义篮球半径的初始值
        self.radius = ball[4]
        #定义篮球的颜色
        self.color = '#ff8c00'  
        


class Basketball_player:
    
    """定义球场上的运动员"""
    
    def __init__(self, player):
        self.team = Team(player[0])
        self.id = player[1]
        self.x = player[2]
        self.y = player[3]
        self.color = self.team.color
      



  
class Moment:
    """定义球场上不同的时刻"""
    def __init__(self, moment):
        #显示当前比赛处在哪一节
        self.quarter = moment[0] 
        #显示当前比赛在本节还有多少时间
        self.game_clock = moment[2] 
        #显示本次进攻剩余时间
        self.shot_clock = moment[3] 
        
        ball = moment[5][0]  
        self.ball = Basketball(ball)
        
        #显示当前时刻球场上的运动员
        players = moment[5][1:]  
        self.players = [Basketball_player(player) for player in players]
