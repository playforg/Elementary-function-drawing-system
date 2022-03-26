import pygame, random

class raindrop():                           #定义一个雨点类，雨点有位置、重量、颜色、是否落到水面、是否存在、绘制线宽等属性
    raindrop_max_radius = 15                # 雨滴落到水面后产生涟漪的初始最大圆的默认半径
    color_R = 0                             #雨滴颜色的默认红色分量
    color_G = 255                           #雨滴颜色的默认绿色分量
    color_B = 255                           #雨滴颜色的默认蓝色分量

    def __init__(self,screen_width,screen_heght,raindrop_weight):               #雨点初始化构造函数
        self.raindrop_x = random.choice(range(screen_width))                    #雨点落到水面时在窗口中x坐标#随机生成雨点落到水面时在窗口中x坐标，0到窗口最大值
        self.raindrop_y = random.choice(range(int(screen_heght*7/8),screen_heght))#雨点落到水面时在窗口中y坐标#随机生成雨点落到水面时在窗口中y坐标，窗口最大值的一半到窗口最大值，即雨点只落在屏幕的下半屏
        self.raindrop_weight=random.choice(range(1,raindrop_weight))            #随机生成雨滴的重量，默认1-8，可在初始化时由调用函数传入
        self.raindrop_radius=random.choice(range(1,self.raindrop_max_radius))   #随机生成涟漪的初始最小圆的半径，默认1-5
        self.line_width = 1                                                     #绘制雨滴只有线段和椭圆，定义绘制的默认线宽，雨滴比涟漪宽一个像素
        # self.color_R = random.choice(range(255))                              #随机生成雨滴颜色的红色分量
        # self.color_G = random.choice(range(255))                              #随机生成雨滴颜色的绿色分量
        # self.color_B = random.choice(range(255))                              #随机生成雨滴颜色的蓝色分量
        self.raindrop_move_x = self.raindrop_x                                  #雨滴下落过程中的x坐标就是前面随机生成的滴落点x坐标
        self.raindrop_move_y = 2                                                #雨滴下落过程中的y坐标初始为2，滴落运行过程中会增大，但不会大于滴落点的y坐标self.raindrop_y
        self.raindrop_move_x_dev = 0                                            # 雨滴下落过程中的x坐标的移动增量
        self.raindrop_move_y_dev = 0                                            # 雨滴下落过程中的y坐标的移动增量
        self.raindrop_move_y_dev = random.choice(range(10, 60))                 #随机生成雨滴下落的移动速度，这样雨滴就不会整齐划一的落下了
        self.rain_transparency = random.choice((255,230,205,180,155))           #定义雨点滴落过程中的透明度
        self.raindrop_transparency = 255                                        #定义雨点滴落后产生涟漪的透明度
        self.raindrop_dripped = False                                           #雨滴构造时都是没有滴落到水面的
        self.raindrop_over = True                                               # 雨滴是否存在bool变量


    def get_x(self):
        return self.raindrop_x

    def get_y(self):
        return self.raindrop_y

    def get_weight(self):
        return self.raindrop_weight

    def get_radius(self):
        return self.raindrop_radius

    def get_over(self):
        return self.raindrop_over

    def transparency_Diminishing(self):                                     #涟漪透明度逐渐低减函数
        if self.raindrop_transparency>5:
            self.raindrop_transparency=self.raindrop_transparency-4
        return self.raindrop_transparency

    def weight_Diminishing(self):                                           #雨滴重量递减函数
        if self.raindrop_weight>0 :
            self.raindrop_weight=self.raindrop_weight-1
        return self.raindrop_weight

    def radius_Increasing(self):                                            #涟漪绘制半径递增函数
        if self.raindrop_radius<=30*self.raindrop_weight:                   #涟漪的最大半径为雨滴重量的20倍
            self.raindrop_radius=self.raindrop_radius+2
        else:
            self.raindrop_over = False                                      #涟漪一旦超过最大半径，则标识雨滴为不存在
        return self.raindrop_radius

    def move_Increasing(self):                                              #雨滴滴落移动位置递增函数，只定义了y坐标的移动
        if (self.raindrop_move_y + self.raindrop_move_y_dev) < self.raindrop_y :
            self.raindrop_move_y = self.raindrop_move_y + self.raindrop_move_y_dev
        else:
            self.raindrop_dripped = True                                    #一旦雨滴滴落到水面就将雨滴标识为“已滴落”

    def draw_raindrop(self,raindrop_screen,color=(0, 255, 0,255),line_width=1):
        #################################开始####绘制雨滴下落代码####开始#######################################
        if self.raindrop_dripped==False:
            pygame.draw.line(raindrop_screen,(self.color_R, self.color_G, self.color_B, self.rain_transparency),(self.raindrop_move_x,self.raindrop_move_y),
                             (self.raindrop_move_x,self.raindrop_move_y+self.raindrop_weight),self.line_width+1)
            self.move_Increasing()
        #################################结束####绘制雨滴下落代码####结束#######################################
        #################################开始####绘制椭圆形雨滴涟漪代码####开始#######################################

        if self.raindrop_dripped == True:
            pygame.draw.ellipse(raindrop_screen, (self.color_R, self.color_G, self.color_B, self.raindrop_transparency),
                                (self.raindrop_x - self.raindrop_radius,
                                 self.raindrop_y - self.raindrop_radius / 2, self.raindrop_radius * 2,
                                 self.raindrop_radius), self.line_width)
            if self.raindrop_radius-60>0:
                pygame.draw.ellipse(raindrop_screen, (self.color_R, self.color_G, self.color_B, min(self.raindrop_transparency+60,255)),
                                    (self.raindrop_x - (self.raindrop_radius-60),
                                     self.raindrop_y - (self.raindrop_radius-60) / 2, (self.raindrop_radius-60) * 2,
                                     (self.raindrop_radius-60)), self.line_width)
            if self.raindrop_radius-100>0:
                pygame.draw.ellipse(raindrop_screen, (self.color_R, self.color_G, self.color_B, min(self.raindrop_transparency+100,255)),
                                    (self.raindrop_x - (self.raindrop_radius-100),
                                     self.raindrop_y - (self.raindrop_radius-100) / 2, (self.raindrop_radius-100) * 2,
                                     (self.raindrop_radius-100)), self.line_width)
            self.radius_Increasing()
            self.transparency_Diminishing()
        #################################结束####绘制椭圆形雨滴涟漪代码####结束#######################################
        return

class Rain_Curtain():          #定义一个雨幕类,雨幕类包含很多雨点raindrops对象
    raindrops = []
    default_weight = 8

    def __init__(self,screen,width,height):             #需要绘制屏幕和屏幕的宽和高进行初始化
        self.screen =screen
        self.width = width
        self.height = height
        self.alpha_screen = screen.convert_alpha()      #用屏幕构造一个相同大小的画板，raindrops先画在这个画板上

    def run(self):                                      #让雨幕运行起来的函数
        self.raindrops.append(raindrop(self.width, self.height, self.default_weight))  # 构造一个雨滴，追加到雨滴链表
        raindrops_len = 1  # 定义雨滴链表长度整型变量
        i = 0
        #print(len(self.raindrops))
        while i < raindrops_len:
            raindrops_len = len(self.raindrops)
            if not self.raindrops[i].get_over():
                del self.raindrops[i]
            raindrops_len = len(self.raindrops)
            i = i + 1
        self.alpha_screen.fill(pygame.Color(0, 0, 0,0))             #绘制雨点链表前，先将画板清空
        for i in range(len(self.raindrops)):
            if self.raindrops[i].get_over():
                self.raindrops[i].draw_raindrop(self.alpha_screen)
        self.screen.blit(self.alpha_screen, (0, 0))

    def get_default_weight(self):
        return self.default_weight

    def set_default_weight(self,default_weight):
        self.default_weight=default_weight