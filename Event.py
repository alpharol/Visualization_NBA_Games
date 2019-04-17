import matplotlib.pyplot as plt
from matplotlib import animation
from PIL import Image
from Elements import Moment
        
"""
数据集中，一场篮球比赛被分成了不同的部分，每一个部分代表着这一时间球场上发生的事情

在本项目中，我们的目的就是使用这些数据，还原出球场的状况。

此处，我们定义并对每一部分进行处理
"""


"""定义球场的大小"""
x1 = 0
x2 = 100
y1 = 0
y2 = 50
d = 6

x_c = x2 / 2 - d / 1.5 + 0.10
y_c = y2 - d / 1.5 - 0.35
    
"""定义球场下方球员信息的长宽""" 
pl_info_l = 0.4 
pl_info_w = 1.5  

    
"""在动图中，每个球员用小圆圈代表，圆圈中有球员的号码
fontsize代表号码的大小
player_s代表圆圈的大小，可以自己调整"""
fontsize = 10
standard_con = 10
player_s = 15 / standard_con
    
    


class Event:
    

    def __init__(self, event):
    #将每一个攻防回合拆分成不同的时刻（moment）,显示每一时刻所处在第几节、当前时间和比赛剩余时间
    #由定义的moment函数实现 
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
    #获取场上运动员信息
        home_players = event['home']['players'] #主场球员
        guest_players = event['visitor']['players'] #客场球员
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        self.player_ids_dict = dict(zip(player_ids, values))
        
    #随着篮球轨迹的变化，更新其半径，篮球的高度越高，半径越大
    def update_radius(self, i, player_circles, ball_circle, annotations, clock_info):
        moment = self.moments[i]
        for j, circle in enumerate(player_circles):
    #对于球场上的每一个队员画一个圈做代表，圆心为此时运动员x/y的坐标
            circle.center = moment.players[j].x, moment.players[j].y
            annotations[j].set_position(circle.center)
    #定义显示时间的格式
            clock_test = 'Quarter {:d}\n {:02d}:{:02d}\n {:03.1f}'.format(
                         moment.quarter,
                         int(moment.game_clock) % 3600 // 60,
                         int(moment.game_clock) % 60,
                         moment.shot_clock)
            clock_info.set_text(clock_test)
        ball_circle.center = moment.ball.x, moment.ball.y
        ball_circle.radius = moment.ball.radius / standard_con
    
        return player_circles, ball_circle

    #绘制动图并保存为视频
    def show(self):   
    #设置坐标轴范围，并隐藏
        ax = plt.axes(xlim=(x1,x2),
                      ylim=(y1,y2))
        ax.axis('off')
        fig = plt.gcf()
        ax.grid(False)  
    #以该时刻的时间为起始时间
        start_moment = self.moments[0]
        player_dict = self.player_ids_dict
    #设置动画中时间显示的位置及颜色
        clock_info = ax.annotate('', xy=[x_c, y_c],
                                 color='black', horizontalalignment='center',
                                   verticalalignment='center')

        annotations = [ax.annotate(self.player_ids_dict[player.id][1], xy=[0, 0], color='w',
                                   horizontalalignment='center',
                                   verticalalignment='center', fontweight='bold')
                       for player in start_moment.players]

       
        sorted_players = sorted(start_moment.players, key=lambda player: player.team.id)
      #根据运动员所属id区分球队 
        home_player = sorted_players[0]
        guest_player = sorted_players[5]
        column_labels = tuple([home_player.team.name, guest_player.team.name])
        column_colours = tuple([home_player.team.color, guest_player.team.color])
        cell_colours = [column_colours for _ in range(5)]
        
        home_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[:5]]
        guest_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[5:]]
        players_data = list(zip(home_players, guest_players))
      #在动画的下方添加主客场球员的姓名球衣信息表格
        table = plt.table(cellText=players_data,
                              colLabels=column_labels,
                              colColours=column_colours,
                              colWidths=[pl_info_l, pl_info_l],
                              loc='bottom',
                              cellColours=cell_colours,
                              fontsize=fontsize,
                              cellLoc='center')
        table.scale(1, pl_info_w)
        table_cells = table.properties()['child_artists']
        for cell in table_cells:
            cell._text.set_color('white')
       #在动画中生成篮球和球员信息
        player_circles = [plt.Circle((0, 0), player_s, color=player.color)
                          for player in start_moment.players]
        ball_circle = plt.Circle((0, 0), player_s,
                                 color=start_moment.ball.color)
        #在动画中展示
        for circle in player_circles:
            ax.add_patch(circle)
        ax.add_patch(ball_circle)
        
        """可以根据需要自己调整速度"""
        interval = 25
        #将每一个时刻创作成一个连续的动画
        anim = animation.FuncAnimation(fig, self.update_radius,
                         fargs=(player_circles, ball_circle, annotations, clock_info),
                         frames=len(self.moments), interval=interval)
        
        """读取球场图片（可以根据自己的喜好修改）"""
        court = Image.open("Warriors.jpg")
        plt.imshow(court, zorder=0, extent=[x1, x2-d, y2, y1])
            
        """保存为视频格式"""        
        anim.save("Warriors vs Cavaliers Quarter1.mp4",fps=25) 

        plt.show()
        
