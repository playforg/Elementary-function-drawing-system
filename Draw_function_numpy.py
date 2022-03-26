# This is a sample Python script.
# 这是一个初等函数的绘制系统，旨在绘制出所有的初等函数，向中小学生、甚至大学生展示初等函数的具体图像，促进数学兴趣。
# 而“绘制出所有的初等函数”其实是一个比较难以实现的目标，因为初等函数的形式实在是太广袤了，而且最困难的是初等函数很
# 可能有无数个某个类型的奇异点，这些奇异点有的就是“无定义”，有的趋向于无穷大，有的又立即趋向于无穷小，有的除以零可
# 其极限实际上是存在的，甚至有的函数“处处可导”，却处处“不连续”，这样的不可预知的“问题”函数，给编程绘制带来了极大的
# 挑战。本系统基本实现了sin(x)、cos(x)、tan(x)、arcsin(x)、arccos(x)、arctan(x)、sinh(x)、cosh(x)、
# tanh(x)、arcsinh(x)、arccosh(x)、arctanh(x)、log(x)、sqrt(x)、power(x,数值)、运算符：“+”、“-”、“*”、
# "“/”、“^(乘方)” “(”、“)”, pi”和“e”任意符合数学规则组合的函数绘制，但确实不保证所有的初等函数都能绘制；而且比
# 系统暂时没有考虑数学表达式为分段函数的绘制。截止目前，外国人做的函数绘制系统确实比我们做的好些，比如“Number
# Empire”、“Demos"等等。实事上函数绘制系统的完善远未完成，比如找出所有的奇异点、区间极值点、渐近线、交点等等。
# python是目前非常流行的工具，但是有用pygame来建立这样的数学图像绘制系统的我也算是比较奇葩，但实际上我觉得pygame
# 在这方面是非常方便和优秀的；本程序还使用了pygame_menu，其使用教程非常少，只能看GitHuble
# 本脚本需要导入一个雨点类，是我以前写的一个雨点动画，很容易导入使用，您可以在程序中关闭。
# 我是mathfrog,如果您对该程序有任何好的建议和想法，可以通过电子邮箱20836791@qq.com与我联系。
import pygame, sys, random, pygame.locals
import win32api, win32con ,math , numpy ,re ,copy
import pygame_menu
import rain_curtain

class Coordinate_axis():
    origin = (0,0)
    scale = 300                  #定义比例尺，1倍，10倍，100倍,scale不能小于10
    scale_multiple = 0           #定义标尺的倍数
    mark = 20                   #定义坐标轴的等分标记数
    origin_pixel = [0,0]
    line_width = 1
    mark_line = 10
    text_dev = 2                #定义文字偏移量
    color_R = 0                 # 坐标轴颜色的默认红色分量
    color_G = 255               # 坐标轴颜色的默认绿色分量
    color_B = 255               # 坐标轴颜色的默认蓝色分量
    color_alpha = 150           # 坐标轴颜色的默认透明度分量
    def __init__(self,screen,screen_width,screen_height,func_input_menu,func_input_text):
        self.screen = screen
        self.axis_screen = None                                 # 用屏幕构造一个相同大小的坐标轴画板，坐标轴都画在axis_screen上
        self.help_info_screen = None
        self.func_input_screen = None
        self.func_input_menu = func_input_menu
        self.func_input_text = func_input_text
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.origin_pixel = [int(screen_width/2),int(screen_height/2)]
        self.scale_and_multiple = self.scale * math.pow(100, self.scale_multiple)
        self.bg_color = pygame.Color(105, 105, 105)             # 背景颜色
        self.mouse_text_color = pygame.Color(0, 255, 255,150)   # 鼠标移动时是否显示坐标的颜色
        self.mouse_cross_color = pygame.Color(0, 55, 255, 255)  # 鼠标十字架的颜色

        self.axis_num_color = pygame.Color(0,0,0)               # 坐标轴上的刻度数字颜色
        self.function_color = pygame.Color(150, 255, 255)       # 绘制函数的颜色
        self.mouse_text_Flag = True                             # 鼠标移动时是否显示坐标的标志变量
        self.mouse_cross_Flag = True                            # 鼠标移动时是否显示十字架的标志变量
        self.help_info_Flag = False                              # 是否显示帮助信息的标志变量
        self.func_input_Flag = True                             # 是否显示函数输入信息框的标志变量
        self.function_input_legal_Flag = True                   # 输入的函数文本是否合法的标志

        self.axis_font = 20                                     # 坐标轴上的刻度数字字体大小
        self.draw_info_font_size =16
        self.mouse_font_size = 15                               # 鼠标移动时显示坐标的字体大小

        self.help_pos_x = 20
        self.help_pos_y = 50
        self.help_pos_width = 300
        self.help_pos_height = 800
        self.help_screen_pos_x = -self.help_pos_width
        self.help_info_line_width = 3                                               # 帮助信息显示区线条宽度
        self.help_info_head_font_size = 20                                          # 帮助信息显示区头部字体大小
        self.help_info_content_font_size = 14                                       # 帮助信息显示区内容字体大小
        self.help_info_font_bgcolor = pygame.Color(25, 25, 112,180)                 # 帮助信息显示区背景颜色
        self.help_info_color = pygame.Color(0, 55, 255, 255)  # 帮助信息显示区域的基本颜色
        self.help_info_font_color = pygame.Color(255, 105, 105,255)                 # 帮助信息显示区头部字体颜色
        self.help_info_content_font_color = pygame.Color(255, 105, 105, 255)        # 帮助信息显示区内容字体颜色

        self.func_input_width = 1000
        self.func_input_height = 70
        self.func_input_pos_x = 20
        self.func_input_pos_y = 10
        self.func_input_screen_pos_y = self.screen_height
        self.func_input_line_width = 2
        self.func_input_font_size = 20
        self.func_input_bgcolor = pygame.Color(25, 25, 112, 180)                    # 函数信息输入去区背景颜色
        self.func_input_line_color = pygame.Color(0, 55, 255, 255)                  # 帮助信息显示区域的基本颜色
        self.func_input_font_color = pygame.Color(255, 105, 105, 255)               # 函数信息输入去区的字体颜色
        self.function_text_show = []                                                # 函数输入文本列表，每输入一个函数文本处理成合法的用来显示的文本，添加到列表
        self.function_text_error = ""
        self.function_text_error_font_alpha = 255
        self.function_text = []                                                     # 函数输入文本列表，每输入一个函数文本处理成合法的用来执行的文本，一般多一个math.添加到列表
        self.function_max = 20
        self.function_number = 0
        self.function_darw_point_list = [[]for i in range(self.function_max)]      # 保存多个函数的绘制点列信息，以便不用每次刷新都重新计算 for i in range(self.function_max)


    def origin_pixel_right(self):
        if self.origin_pixel[0] + 10 < self.screen_width :
            self.origin_pixel[0] = self.origin_pixel[0] + 10
            self.__calculation_function_draw_point()

    def origin_pixel_left(self):
        if self.origin_pixel[0] - 10 > 0 :
            self.origin_pixel[0] = self.origin_pixel[0] - 10
            self.__calculation_function_draw_point()

    def origin_pixel_up(self):
        if self.origin_pixel[1] - 10 > 0 :
            self.origin_pixel[1] = self.origin_pixel[1] - 10
            self.__calculation_function_draw_point()

    def origin_pixel_down(self):
        if self.origin_pixel[1] + 10 < self.screen_height:
            self.origin_pixel[1] = self.origin_pixel[1] + 10
            self.__calculation_function_draw_point()

    def scale_enlarge(self):                             #按下UP键scale放大，坐标轴衡量区间缩小，显示在其中的函数
        self.scale = self.scale + 10
        if self.scale >100 :
            self.axis_font = 20
        if self.scale < 100 and self.scale > 30 :
            self.axis_font = 15
        if self.scale > self.screen_height/2 :
            self.scale_multiple = self.scale_multiple - 1
            self.scale = 10
            self.axis_font = 7
        self.__calculation_function_draw_point()
        self.scale_and_multiple = self.scale * math.pow(100, self.scale_multiple)

    def scale_reduce(self):                             #按下DOWN键scale缩小，坐标轴衡量区间放大
        if self.scale - 10 > 0 :
            self.scale = self.scale - 10
        elif self.scale_multiple < 3:
            self.scale_multiple = self.scale_multiple + 1
            self.scale = 500
            self.axis_font = 20
        if self.scale < 100 and self.scale > 30 :
            self.axis_font = 15
        if self.scale < 30 and self.scale > 8 :
            self.axis_font = 7
        self.__calculation_function_draw_point()
        self.scale_and_multiple = self.scale * math.pow(100, self.scale_multiple)

    def get_bg_color(self):
        return self.bg_color

    def mouse_text_show(self):
        if self.mouse_text_Flag == True:
            self.mouse_text_Flag = False
        else :
            self.mouse_text_Flag = True

    def __mouse_text(self):
        mouse_font = pygame.font.Font('ariali.ttf', self.mouse_font_size)  # 定义鼠标移动时显示的坐标文字字体
        text_mouse = mouse_font.render(str(                     #构造鼠标移动时显示的坐标值
            round((pygame.mouse.get_pos()[0] - self.origin_pixel[0]) / self.scale * math.pow(10, self.scale_multiple),
                  -self.scale_multiple + 1)) + " , " + str(
            -round((pygame.mouse.get_pos()[1] - self.origin_pixel[1]) / self.scale * math.pow(10, self.scale_multiple),
                   -self.scale_multiple + 1)), True, self.mouse_text_color)
        if self.mouse_text_Flag :
            self.axis_screen.blit(text_mouse,(pygame.mouse.get_pos()[0]-50,pygame.mouse.get_pos()[1]-20))

    def mouse_cross_show(self):
        if self.mouse_cross_Flag == True:
            self.mouse_cross_Flag = False
        else :
            self.mouse_cross_Flag = True

    def __mouse_cross(self):
        if self.mouse_cross_Flag :
            # pygame.draw.line(self.axis_screen,self.mouse_cross_color,(0,pygame.mouse.get_pos()[1]),(self.screen_width,pygame.mouse.get_pos()[1]))
            # pygame.draw.line(self.axis_screen, self.mouse_cross_color, (pygame.mouse.get_pos()[0],0),
            #                  (pygame.mouse.get_pos()[0],self.screen_height))
            i = 0
            while i*20+10 < self.screen_width :
                pygame.draw.line(self.axis_screen, self.mouse_cross_color, (i*25, pygame.mouse.get_pos()[1]),
                                 (i*25+10, pygame.mouse.get_pos()[1]))
                pygame.draw.line(self.axis_screen, self.mouse_cross_color, (pygame.mouse.get_pos()[0], i*25),
                                                  (pygame.mouse.get_pos()[0],i*25+10))
                i=i+1

    def help_info_show(self):
        if self.help_info_Flag == True:
            self.help_info_Flag = False
            self.help_screen_pos_x = - self.help_pos_width
        else :
            self.help_info_Flag = True

    def __help_info(self):
        text_line_height = 32
        text_line_height_2 = 20
        text_line_indent = 30
        text_line_down_dev = 80
        help_info_head_font = pygame.font.Font('方正粗黑宋简体.ttf', self.help_info_head_font_size)  # 定义帮助信息区头部的字体
        help_info_content_font = pygame.font.Font('方正粗黑宋简体.ttf', self.help_info_content_font_size)  # 定义帮助信息区内容的字体
        if self.help_info_Flag:
            self.help_info_screen.fill(self.help_info_font_bgcolor)
            pygame.draw.line(self.help_info_screen, self.help_info_color, (self.help_pos_x, self.help_pos_y),
                             (self.help_pos_x + self.help_pos_width, self.help_pos_y), self.help_info_line_width)
            pygame.draw.line(self.help_info_screen, self.help_info_color,
                             (self.help_pos_x + self.help_pos_width, self.help_pos_y),
                             (self.help_pos_x + self.help_pos_width, self.help_pos_y + self.help_pos_height),
                             self.help_info_line_width)
            pygame.draw.line(self.help_info_screen, self.help_info_color,
                             (self.help_pos_x + self.help_pos_width, self.help_pos_y + self.help_pos_height),
                             (self.help_pos_x, self.help_pos_y + self.help_pos_height), self.help_info_line_width)
            pygame.draw.line(self.help_info_screen, self.help_info_color,
                             (self.help_pos_x, self.help_pos_y + self.help_pos_height),
                             (self.help_pos_x, self.help_pos_y), self.help_info_line_width)
            text_head = help_info_head_font.render("帮助信息（F1）", True, self.help_info_font_color)
            self.help_info_screen.blit(text_head, (int((self.help_pos_width - 100) / 2), 15))
            text_content = help_info_content_font.render("（F1） ——  呼出帮助信息",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev))
            text_content = help_info_content_font.render("（F2） ——  显示/隐藏，雨幕背景",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 1))
            text_content = help_info_content_font.render("（F3） ——  显示/隐藏，鼠标十字架",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 2))
            text_content = help_info_content_font.render("（F4） ——  显示/隐藏，鼠标坐标信息",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 3))
            text_content = help_info_content_font.render("（F5） ——  显示/隐藏，函数输入信息框",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 4))
            text_content = help_info_content_font.render("（F6） ——  清除现有绘制的所有函数",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 5))
            text_content = help_info_content_font.render("（←LEFT） ——  坐标轴原点左移",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 6))
            text_content = help_info_content_font.render("（→RIGHT） ——  坐标轴原点右移",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 7))
            text_content = help_info_content_font.render("（↑UP） ——  坐标轴原点上移",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 8))
            text_content = help_info_content_font.render("（↓DOWN） ——  坐标轴原点下移",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 9))
            text_content = help_info_content_font.render("（Page Up） ——  坐标轴尺度放大",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 10))
            text_content = help_info_content_font.render("（Page Down） ——  坐标轴尺度放缩小",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 11))
            text_content = help_info_content_font.render("系统输入函数规则：",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 12))
            text_content = help_info_content_font.render("系统只接受函数：sin(x)、cos(x)、tan(x)、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13))
            text_content = help_info_content_font.render("arcsin(x)、arccos(x)、arctan(x)、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 1))
            text_content = help_info_content_font.render("sinh(x)    、cosh(x)    、tanh(x)、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 2))
            text_content = help_info_content_font.render("arcsinh(x)、arccosh(x)、arctanh(x)、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 3))
            text_content = help_info_content_font.render("log(x)、sqrt(x)、power(x,数值)、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 4))
            text_content = help_info_content_font.render("系统只接受运算符：“+”、“-”、“*”、",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 5))
            text_content = help_info_content_font.render("                               “/”和“^(乘方)”",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 6))
            text_content = help_info_content_font.render("系统只接受常数：“pi”和“e”",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
            text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 7))
            text_content = help_info_content_font.render("系统只接受其他符号：“(”、“)”和“,”",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 8))
            text_content = help_info_content_font.render("系统能够绘制出以上组件任意组合，但是系统",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 9))
            text_content = help_info_content_font.render("还是留下一些小BUG，(、)和 , 的错误输入方",
                                                         True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 10))
            text_content = help_info_content_font.render(
                "式，系统将不能正确绘制，也不能正确提示错",
                True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 11))
            text_content = help_info_content_font.render(
                "误；如果该系统受到网友的欢迎的话，我将继",
                True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 12))
            text_content = help_info_content_font.render(
                "续完善程序，谢谢！",
                True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 13))
            text_content = help_info_content_font.render(
                "如您关于本系统有任何建议和想法可以致信给",
                True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 14))
            text_content = help_info_content_font.render(
                "本人mathfrog,邮箱地址为20836791@qq.com。",
                True, self.help_info_content_font_color)
            self.help_info_screen.blit(text_content, (
                text_line_indent, text_line_down_dev + text_line_height * 13 + text_line_height_2 * 15))
            ###########开始####控制帮助信息区向右滑出的代码####开始#############分3段速度滑出
            if self.help_screen_pos_x >=-self.help_pos_width and self.help_screen_pos_x <= -int(self.help_pos_width*1/2):
                self.help_screen_pos_x= self.help_screen_pos_x + 50
            elif self.help_screen_pos_x <= 30:
                self.help_screen_pos_x = self.help_screen_pos_x + 20
            elif self.help_screen_pos_x < 50:
                self.help_screen_pos_x = self.help_screen_pos_x + 1
            ###########结束####控制帮助信息区向右滑出的代码####结束#############

    def func_input_show(self):
        if self.func_input_Flag == True:
            self.func_input_Flag = False
            self.func_input_screen_pos_y = self.screen_height
        else :
            self.func_input_Flag = True
            self.__clear_func_input()

    def __clear_func_input(self):
        self.func_input_text.set_value("")

    def __func_input(self):         #具体绘制函数信息输入框，用到pygame_menu库
        func_input_font = pygame.font.Font('方正粗黑宋简体.ttf', self.func_input_font_size)  # 定义帮助信息区头部的字体
        if self.func_input_Flag :
            self.func_input_screen.fill(self.func_input_bgcolor)
            pygame.draw.line(self.func_input_screen, self.func_input_line_color, (self.func_input_pos_x, self.func_input_pos_y),
                             (self.func_input_pos_x + self.func_input_width, self.func_input_pos_y),self.func_input_line_width)
            pygame.draw.line(self.func_input_screen, self.func_input_line_color,
                             (self.func_input_pos_x + self.func_input_width, self.func_input_pos_y),
                             (self.func_input_pos_x + self.func_input_width, self.func_input_pos_y + self.func_input_height),
                             self.func_input_line_width)
            pygame.draw.line(self.func_input_screen, self.func_input_line_color,
                             (self.func_input_pos_x + self.func_input_width, self.func_input_pos_y + self.func_input_height),
                             (self.func_input_pos_x, self.func_input_pos_y + self.func_input_height), self.func_input_line_width)
            pygame.draw.line(self.func_input_screen, self.func_input_line_color,
                             (self.func_input_pos_x, self.func_input_pos_y + self.func_input_height),
                             (self.func_input_pos_x, self.func_input_pos_y), self.func_input_line_width)

            text_func_input = func_input_font.render("请输入函数表达式：", True, self.func_input_font_color)
            self.func_input_screen.blit(text_func_input, (self.func_input_pos_x*2,
                                                          self.func_input_pos_y*4))

            ###########开始####控制帮助信息区向右滑出的代码####开始#############分3段速度滑出
            if self.func_input_screen_pos_y >= self.screen_height-self.func_input_height and \
                            self.func_input_screen_pos_y <= self.screen_height:
                self.func_input_screen_pos_y = self.func_input_screen_pos_y - 30
            elif self.func_input_screen_pos_y >= self.screen_height - self.func_input_height*2 and \
                            self.func_input_screen_pos_y < self.screen_height - self.func_input_height:
                self.func_input_screen_pos_y = self.func_input_screen_pos_y - 10
            elif  self.func_input_screen_pos_y > self.screen_height - self.func_input_height*2 -30 :
                self.func_input_screen_pos_y = self.func_input_screen_pos_y - 1
            ###########结束####控制帮助信息区向右滑出的代码####结束#############
            ###########开始####绘制函数信息输入框,这将用到pygame_menu库####开始#############
            self.func_input_text.draw(self.func_input_screen)
            function_str = self.func_input_text.get_value()
            # font_info = self.func_input_text.get_font_info()
            font_info = self.func_input_text.is_selected()
            #print(font_info)
            self.func_input_text.set_border(1,(0, 55, 255, 255))
            self.func_input_text.set_position(220, self.func_input_pos_y*3)
            #self.func_input_text.set_default_value("sin(x)")
            # if function_str != "":
            #     print(function_str)
            ###########结束####绘制函数信息输入框,这将用到pygame_menu库####结束#############

    def __check_function_text(self,str_function_text):      #检查输入函数字符串是否符合函数式规则,在get_function_text中调用
        print("输入的函数字符串为：",str_function_text)
        pattern_text = '|pi|sinh?\(|cosh?\(|tanh?\(|arcsinh?\(|arccosh?\(|arctanh?\(|power\(|log\(|sqrt\(|x|\(|\)|\+|-|\*|/|\^|[0-9]|\d+\.?\d*|e|,|'       #对输入字符串进行函数识别的匹配模式，搞了好久才明白，要添加新的函数式就要改变这里
        # pattern_text = '|x|\(|\)|\+|-|\*|/|\^|[0-9]|.|po|e|'  # 对输入字符串进行函数识别的匹配模式，搞了好久才明白，要添加新的函数式就要改变这里
        # 目前只能识别以下列表中的字符或者函数，x为自变量：["x","sin","cos","tan","asin","acos","atan",
        #                                     "sinh","cosh","atanh","asinh","acosh","atanh",
        #                                     "pow","log","sqrt",
        #                                     "+","-","*","/","^","(",")"]
        pipei_patt = re.findall(pattern_text,str_function_text)
        str_function_text_format = ""
        str_function_text_format_show = ""
        if pipei_patt != None :
            print("匹配到的函数组件列表为：",pipei_patt)
            for i in range(len(pipei_patt)):
                str_function_text_format_show = str_function_text_format_show +pipei_patt[i]
                if pipei_patt[i] in ("sin(","cos(","tan(","sinh(","cosh(","tanh(","arcsin(","arccos(","arctan(",
                                     "arcsinh(","arccosh(","arctanh(","power(","log(","sqrt(","pi","e"):
                    # print("原始：",pipei_patt[i])
                    pipei_patt[i] = "numpy."+pipei_patt[i]
                    # print("补齐：",pipei_patt[i])
                if pipei_patt[i] == "^" :
                    pipei_patt[i] = "**"
                str_function_text_format = str_function_text_format +pipei_patt[i]

            if str_function_text_format_show != "" :
                print("重新组装的函数为：",str_function_text_format,str_function_text_format_show)
                pass
            else:
                self.function_input_legal_Flag = False
                print("重新组装的函数为空！")
                pass
        else:
            print("pipei_patt为空！")
            pass

        return str_function_text_format,str_function_text_format_show

    def get_function_text(self):
        self.function_input_legal_Flag = True
        if self.func_input_Flag :
            text =self.func_input_text.get_value()          # 通过pygame_menu.TextInput获取输入的函数表达式
            if text!="":
                str_function_text_format,str_function_text_format_show = self.__check_function_text(text)
                if str_function_text_format:
                    self.function_text.append(str_function_text_format)
                    self.function_text_show.append(str_function_text_format_show)
                    self.function_number = self.function_number + 1         #必须在计算绘制点列后给拟绘制函数数量加1
                    #print("程序执行函数为：",self.function_text,"屏幕显示函数为：",self.function_text_show,"拟绘制函数为",self.function_number,"个！")
                    if self.function_input_legal_Flag :
                        self.function_input_legal_Flag = self.__calculation_function_draw_point()
                        # print("self.function_input_legal_Flag为",self.function_input_legal_Flag)
                else:
                    if not self.function_input_legal_Flag :
                        #print("self.function_text[self.function_number-1]为",self.function_text_show[self.function_number-1])
                        self.function_text_error = text
                        print("self.function_text_error为",self.function_text_error)
                        self.function_text_error_font_alpha = 255
                        # del self.function_text[self.function_number-1]
                        # del self.function_text_show[self.function_number - 1]
                        # self.function_number = self.function_number - 1
                        self.function_input_legal_Flag = True

            self.__clear_func_input()

    def __calculation_function_draw_point(self):
        ####计算函数在屏幕上绘制的实际像素位置的核心计算函数，要将文本转化为代码进行运行计算需要用到compile函数，还要注意前拷贝问题
        ####这个函数在获取到一个合法函数表达式字符串后调用，计算全部获取到的合法函数表达式的绘制点列。为什么要把前面的都算一遍？
        ####因为这个函数在坐标轴移动、尺度放大缩小后都要调用一遍，所有合法函数表达式的绘制点列都必须重新计算，计算量比较大哈。
        axis_pointlist = []         #定义坐标轴（仅X轴）数值与屏幕像素点对应的列表，其元素是一个元组
        darw_pointlist = []         #定义每一个绘制点的X像素位置与y像素位置的列表，其元素是一个元组

        for i in range(-int(self.screen_width/2),int(self.screen_width/2)):
            axis_pointlist.append((i+int(self.screen_width/2),
                (i-self.origin_pixel[0]+int(self.screen_width/2))/(self.scale*math.pow(10,-self.scale_multiple))))
        ##^^##构造一个每个像素点与坐标值相对应的列表,i-self.origin_pixel[0]+int(self.screen_width/2)这里不又加又减函数图像就不会跟着坐标轴移动
        ##^^##axis_pointlist[0],要固定初始化为0--self.screen_width
        # print("axis_pointlist:",axis_pointlist)
        darw_x_function = 0
        j = 0
        for j in range(self.function_number) :
            darw_pointlist.clear()

            func_text = self.function_text[j]
            self.function_darw_point_list[j].clear()
            for i in range(len(axis_pointlist)):

                x = axis_pointlist[i][1]                       #x代表自变量x，输入的自变量必须是'x'
                try:
                    compile_func = compile(func_text,'','eval')
                    # print("自变量X为：",x)
                    darw_x_function = eval(compile_func)            #执行python可以识别的函数表达式，取得拟绘制函数的y值（函数值）
                    # print("计算得到的函数值为：",darw_x_function)
                except (ValueError) :
                    print("您输入的函数表达式语法错误！！！",ValueError)
                    darw_x_function = numpy.nan
                except (ZeroDivisionError):
                    # print("赋值前darw_x_function：",x)
                    darw_x_function = numpy.nan
                    # print("赋值前darw_x_function：",darw_x_function)
                except SyntaxError as e :
                    print('抛出输入函数语法错误的异常:\t', repr(e))
                    self.function_text_error = self.function_text_show[self.function_number - 1]
                    del self.function_text[self.function_number-1]
                    del self.function_text_show[self.function_number - 1]
                    self.function_number = self.function_number - 1
                    return False
                except Exception as e :

                    print('计算函数值时抛出未处理异常:\t', repr(e))
                    return False

                try:
                    # if numpy.isnan(darw_x_function) :
                    #     # print(j,i,darw_x_function)
                    #     darw_pointlist.append((axis_pointlist[i][0], numpy.nan))
                    if numpy.isneginf(darw_x_function) :
                        darw_pointlist.append((axis_pointlist[i][0], self.screen_height+1000))
                    elif numpy.isposinf(darw_x_function) :
                        darw_pointlist.append((axis_pointlist[i][0], -1000))
                    # elif type(darw_x_function)==numpy.complex:
                    #     darw_pointlist.append((axis_pointlist[i][0], numpy.nan))
                    else:
                        axis_pointlist_y = -int(darw_x_function * (self.scale * math.pow(10, -self.scale_multiple))) + \
                                           self.origin_pixel[1]
                        # print("darw_pointlist.append成功！",i,j)
                        darw_pointlist.append((axis_pointlist[i][0],axis_pointlist_y))
                        # print("添加完成:",darw_x_function)
                except (ValueError):
                    if numpy.isnan(darw_x_function) :
                        # print(j,i,darw_x_function)
                        darw_pointlist.append((axis_pointlist[i][0], numpy.nan))
                except TypeError :
                    darw_pointlist.append((axis_pointlist[i][0], numpy.nan))
                except Exception as e :
                    # if numpy.isnan(darw_x_function) :
                    #     # print(j,i,darw_x_function)
                    #     darw_pointlist.append((axis_pointlist[i][0], numpy.nan))
                    print("darw_x_function为：",darw_x_function,"类型为：",type(darw_x_function),"出现在第",i,"点！")
                    print('添加绘制点到点列时抛出未处理异常:\t', repr(e))
                    pass

            # for k in range(len(darw_pointlist)-1):            #某个点过大或者过小就设为空点nan
            #     if (darw_pointlist[k][1]<-100) or (darw_pointlist[k][1]>self.screen_height+100):
            #         darw_pointlist_k_0 = darw_pointlist[k][0]
            #         darw_pointlist.pop(k)
            #         darw_pointlist.insert(k, (darw_pointlist_k_0, numpy.nan))

            for k in range(len(darw_pointlist)-1):          #相邻两个点的差绝对值过大，就将这两个点设置为空点nan
                if numpy.abs(darw_pointlist[k][1]-darw_pointlist[k+1][1])>self.screen_height+100:
                    darw_pointlist_k_0 = darw_pointlist[k][0]
                    darw_pointlist.pop(k)
                    darw_pointlist.insert(k, (darw_pointlist_k_0, numpy.nan))
                    darw_pointlist_k1_0 = darw_pointlist[k+1][0]
                    darw_pointlist.pop(k+1)
                    darw_pointlist.insert(k+1, (darw_pointlist_k1_0, numpy.nan))
                    k=k+1
            # self.function_darw_point_list[j].clear()          #后面有深拷贝，不需要做清零
            # print("self.function_darw_point_list[j]为：",j,self.function_darw_point_list[j])
            self.function_darw_point_list[j]=darw_pointlist.copy()
            # print("darw_pointlist.copy()成功！！",self.function_darw_point_list[j])
            ####^^^^这个地方真的是绝了，弄了很久才明白，列表直接赋值是一个赋值引用，如果直接赋值当后面一个darw_pointlist被重新计算出来以后，
            ####^^^^一旦装入（赋值）给self.function_darw_point_list[j]，那前面计算出来的点列都会被后面的覆盖，就无法同时绘制出多条
            ####^^^^函数曲线了，要解决这个问题就要做浅拷贝或者深拷贝，导入copy库
            # print("self.function_darw_point_list[j]为：", j, self.function_darw_point_list[j])
        return True


    def __darw_function(self):
        ####依据存储的绘制点列在屏幕上将点列绘制出来
        for i in range(self.function_number):
            drawing_start_end_point = []                    #用来存储绘制起止点的列表
            begin_Falg = False
            end_Falg = False

            for k in range(self.screen_width):              #查找出绘制的起止点，对于self.function_darw_point_list中的nan不绘制
                try:
                    if (not numpy.isnan(self.function_darw_point_list[i][k][1])) and (begin_Falg != True):
                        begin_k = k
                        begin_Falg = True
                    if (numpy.isnan(self.function_darw_point_list[i][k][1]) or k == (
                            self.screen_width - 1)) and end_Falg != True and begin_Falg == True:
                        end_k = k-1
                        end_Falg = True
                    if begin_Falg and end_Falg:
                        begin_Falg = False
                        end_Falg = False
                        if end_k - begin_k > 2:
                            drawing_start_end_point.append((begin_k, end_k))
                except Exception as e :
                    # print('查找绘制起始点时抛出未处理异常:\t', repr(e))
                    pass
            # print("绘制的第i个函数点列为：",i,self.function_darw_point_list[i])
            # print(drawing_start_end_point)

            try:
                # print("函数绘制开始！",self.function_number,self.function_darw_point_list[i])
                for draw_i in range(len(drawing_start_end_point)):          #分段绘制
                    pygame.draw.lines(self.axis_screen, self.function_color, False, self.function_darw_point_list[i][
                                                                                    drawing_start_end_point[draw_i][0]:
                                                                                    drawing_start_end_point[draw_i][1]])
                    # pygame.draw.lines(self.axis_screen, self.function_color, False, self.function_darw_point_list[i])
                    # print("self.function_darw_point_list[i]函数绘制成功！",draw_i,len(drawing_start_end_point))
            except Exception as e :
                print('绘制曲线时抛出异常:\t', repr(e))
                pass
        self.screen.blit(self.axis_screen, (0, 0))

    def function_clear(self):
        self.function_text.clear()
        self.function_text_show.clear()
        for i in range(len(self.function_darw_point_list)) :
            if self.function_darw_point_list[i] != [] :
                self.function_darw_point_list[i].clear()
        self.function_number = 0
        self.function_text_error = ""

    def __draw_information(self):
        draw_info_pos_x = 50
        draw_info_pos_y = 10
        draw_info_pos_dev = 30
        draw_info_font = pygame.font.Font('方正粗黑宋简体.ttf', self.draw_info_font_size)  # 定义图例字体
        text_draw_info = draw_info_font.render("初等函数绘制系统 1.0", True,
                                               (255, 0, 0))
        self.axis_screen.blit(text_draw_info, (draw_info_pos_x, draw_info_pos_y))

        text_draw_info = draw_info_font.render("比例尺为：" + str(self.scale) + "个像素/刻度", True,
                                               (self.color_R, self.color_G, self.color_B), self.bg_color)
        self.axis_screen.blit(text_draw_info, (self.screen_width - draw_info_pos_x - 200, draw_info_pos_y))
        text_draw_info = draw_info_font.render("您已绘制以下 "+str(self.function_number)+" 个函数：" , True,
                                               (self.color_R, self.color_G, self.color_B))
        self.axis_screen.blit(text_draw_info, (draw_info_pos_x, draw_info_pos_y + draw_info_pos_dev))

        draw_info_font = pygame.font.Font('ariali.ttf', self.draw_info_font_size)  # 定义图例字体
        for i in range(len(self.function_text)):
            text_draw_info = draw_info_font.render("F(x) "+str(i+1)+"=  "+self.function_text_show[i], True,
                                                   (self.color_R, self.color_G, self.color_B))
            self.axis_screen.blit(text_draw_info, (draw_info_pos_x, draw_info_pos_y+(i+2)*draw_info_pos_dev))
        ####开始##显示输入的函数表达式不正确的信息##开始####
        draw_info_font = pygame.font.Font('方正粗黑宋简体.ttf', self.draw_info_font_size)  # 定义图例字体
        if self.function_text_error != "" :
            temp_str = "您输入的函数表达式< " + self.function_text_error + " >不正确！"
            text_draw_info = draw_info_font.render(temp_str,
                                                   True,
                                                   self.help_info_content_font_color)
            temp_str_size = text_draw_info.get_width()
            if self.function_text_error_font_alpha > 0 :
                self.function_text_error_font_alpha = self.function_text_error_font_alpha - 1
                text_draw_info.set_alpha(self.function_text_error_font_alpha)
                self.axis_screen.blit(text_draw_info, ((self.screen_width-temp_str_size) / 2, self.screen_height - 50))
        ####结束##显示输入的函数表达式不正确的信息##结束####

    def __draw_x_y(self):

        axis_font = pygame.font.Font('方正粗黑宋简体.ttf', self.axis_font)             #定义坐标轴上刻度字体
        text_0 = axis_font.render("0",True,self.axis_num_color,self.bg_color)

        ######################开始####绘制X坐标####开始###################################

        i = 1
        while self.origin_pixel[0]+i*self.scale<self.screen_width :
            if self.scale >=100 :
                fu_scale_num = int(self.scale/100)+1
                for k in range(fu_scale_num) :
                    pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B,self.color_alpha+105),
                                     (self.origin_pixel[0] + (i-1) * self.scale + (k)*int(self.scale/fu_scale_num),
                                      self.origin_pixel[1] - int(self.mark_line/2)),
                                     (self.origin_pixel[0] + (i-1) * self.scale + (k)*int(self.scale/fu_scale_num), self.origin_pixel[1]),
                                     self.line_width)
            ####绘制正X轴部分的副刻度线,先绘制副刻度，让主刻度覆盖他
            pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B,255),
                             (self.origin_pixel[0] + i * self.scale,
                              self.origin_pixel[1] - self.mark_line),
                             (self.origin_pixel[0] + i * self.scale, self.origin_pixel[1]),
                             self.line_width)
            ####绘制正X轴部分的主刻度线

            if self.scale_multiple >= 0 :
                text_i_fomat = str(int(i* math.pow(10, self.scale_multiple)))
            else :
                text_i_fomat = str(round(i* math.pow(10, self.scale_multiple),-self.scale_multiple))
            text_i = axis_font.render(text_i_fomat, True, self.axis_num_color, self.bg_color)
            self.axis_screen.blit(text_i, (
                        self.origin_pixel[0] + i *self.scale - self.text_dev * 2,
                                                                         self.origin_pixel[1] + self.text_dev))
            ####绘制正X轴部分的主刻度数字
            i=i+1
        i = 1
        while self.origin_pixel[0] - i * self.scale > 0:
            if self.scale >=100 :
                fu_scale_num = int(self.scale/100)+1
                for k in range(fu_scale_num) :
                    pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B,self.color_alpha+105),
                                     (self.origin_pixel[0] - (i-1) * self.scale - (k)*int(self.scale/fu_scale_num),
                                      self.origin_pixel[1] - int(self.mark_line/2)),
                                     (self.origin_pixel[0] - (i-1) * self.scale - (k)*int(self.scale/fu_scale_num), self.origin_pixel[1]),
                                     self.line_width)
            ####绘制负X轴部分的副刻度线,先绘制副刻度，让主刻度覆盖他
            pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                             (self.origin_pixel[0] - i * self.scale, self.origin_pixel[1] - self.mark_line),
                             (self.origin_pixel[0] - i * self.scale, self.origin_pixel[1]),
                             self.line_width)
            ####绘制负X轴部分的主刻度线
            if self.scale_multiple >= 0:
                text_i_fomat = str(int(-i * math.pow(10, self.scale_multiple)))
            else:
                text_i_fomat = str(round(-i * math.pow(10, self.scale_multiple), -self.scale_multiple))
            text_i = axis_font.render(text_i_fomat, True, self.axis_num_color, self.bg_color)
            self.axis_screen.blit(text_i, (self.origin_pixel[0] - i * self.scale-self.text_dev*10, self.origin_pixel[1] + self.text_dev))
            ####绘制负X轴部分的主刻度数字
            i = i + 1
        ######################结束####绘制X坐标####结束###################################
        ######################开始####绘制Y坐标####开始###################################

        i = 1
        while self.origin_pixel[1]+i*self.scale<self.screen_height :
            if self.scale >=100 :
                fu_scale_num = int(self.scale/100)+1
                for k in range(fu_scale_num) :
                    pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                                     (self.origin_pixel[0] - int(self.mark_line/2), self.origin_pixel[1] + (i-1) * self.scale + (k)*int(self.scale/fu_scale_num)),
                                     (self.origin_pixel[0], self.origin_pixel[1] + (i-1) * self.scale + (k)*int(self.scale/fu_scale_num)),
                                     self.line_width)
            ####绘制正X轴部分的副刻度线,先绘制副刻度，让主刻度覆盖他
            pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                             (self.origin_pixel[0]-self.mark_line, self.origin_pixel[1]+i*self.scale),
                             (self.origin_pixel[0], self.origin_pixel[1]+i*self.scale),
                             self.line_width)
            ####绘制负Y轴部分的主刻度线
            if self.scale_multiple >= 0 :
                text_i_fomat = str(int(-i* math.pow(10, self.scale_multiple)))
            else :
                text_i_fomat = str(round(-i* math.pow(10, self.scale_multiple),-self.scale_multiple))
            text_i = axis_font.render(text_i_fomat, True, self.axis_num_color, self.bg_color)
            self.axis_screen.blit(text_i, (self.origin_pixel[0] - self.text_dev * 20,
                                           self.origin_pixel[1]+i*self.scale - self.text_dev * 15))
            ####绘制负X轴部分的主刻度数字
            i = i + 1
        i = 1
        while self.origin_pixel[1]-i*self.scale>0 :
            if self.scale >=100 :
                fu_scale_num = int(self.scale/100)+1
                for k in range(fu_scale_num) :
                    pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                                     (self.origin_pixel[0] - int(self.mark_line/2), self.origin_pixel[1] - (i-1) * self.scale - (k)*int(self.scale/fu_scale_num)),
                                     (self.origin_pixel[0], self.origin_pixel[1] - (i-1) * self.scale - (k)*int(self.scale/fu_scale_num)),
                                     self.line_width)
            ####绘制正X轴部分的副刻度线,先绘制副刻度，让主刻度覆盖他
            pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                             (self.origin_pixel[0]-self.mark_line, self.origin_pixel[1]-i*self.scale),
                             (self.origin_pixel[0], self.origin_pixel[1]-i*self.scale),
                             self.line_width)
            ####绘制正Y轴部分的主刻度线
            if self.scale_multiple >= 0 :
                text_i_fomat = str(int(i* math.pow(10, self.scale_multiple)))
            else :
                text_i_fomat = str(round(i* math.pow(10, self.scale_multiple),-self.scale_multiple))
            text_i = axis_font.render(text_i_fomat, True, self.axis_num_color, self.bg_color)
            self.axis_screen.blit(text_i, (
                self.origin_pixel[0] - self.text_dev * 20, self.origin_pixel[1] - i * self.scale - self.text_dev * 15))
            ####绘制负Y轴部分的主刻度数字
            i = i + 1
        ####把绘制X轴放到最后，以免被刻度数字覆盖
        pygame.draw.line(self.axis_screen,(self.color_R,self.color_G,self.color_B),
                         (0,self.origin_pixel[1]),(self.screen_width,self.origin_pixel[1]),self.line_width)
        ####绘制X轴直线
        pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                         (self.screen_width - self.mark_line, self.origin_pixel[1] - self.mark_line), (self.screen_width, self.origin_pixel[1]),
                         self.line_width+2)
        ####绘制X轴箭头上部
        pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                         (self.screen_width - self.mark_line, self.origin_pixel[1] + self.mark_line), (self.screen_width, self.origin_pixel[1]),
                         self.line_width+2)
        ####绘制X轴箭头下部

        ####把绘制Y轴放到最后，以免被刻度数字覆盖
        pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                         (self.origin_pixel[0], 0), (self.origin_pixel[0], self.screen_height), self.line_width)
        ####绘制Y轴直线
        pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                         (self.origin_pixel[0], 0), (self.origin_pixel[0]-self.mark_line, 0+self.mark_line),
                         self.line_width+2)
        ####绘制Y轴箭头上部
        pygame.draw.line(self.axis_screen, (self.color_R, self.color_G, self.color_B),
                         (self.origin_pixel[0], 0), (self.origin_pixel[0] + self.mark_line, 0 + self.mark_line),
                         self.line_width+2)
        ####绘制Y轴箭头下部
        ######################结束####绘制Y坐标####结束###################################
        self.axis_screen.blit(text_0, (self.origin_pixel[0] + self.text_dev, self.origin_pixel[1] + self.text_dev))

    def darw(self):                                     # 坐标系绘制的核心函数
        pygame.font.init()                              # 为各个绘制模块初始化字体，各模块需要的字体在各模块内
        self.axis_screen = self.screen.convert_alpha()  # 用屏幕构造一个相同大小的坐标轴画板，坐标轴都画在axis_screen上
        self.help_info_screen = pygame.Surface(         # 为帮助信息区单独构造一个表面绘板
            (self.help_pos_width + self.help_pos_x * 2, self.help_pos_height + self.help_pos_y * 2),
            flags=pygame.SRCALPHA)
        self.func_input_screen = pygame.Surface(        # 为函数信息输入区单独构造一个表面绘板func_input_screen
            (self.func_input_width + self.func_input_pos_x * 2, self.func_input_height + self.func_input_pos_y * 2),
            flags=pygame.SRCALPHA)

        self.__draw_x_y()           #绘制可缩放的X\Y轴坐标
        self.__draw_information()   #绘制信息输出
        self.__mouse_text()         #绘制鼠标跟随的坐标信息
        self.__mouse_cross()        #绘制鼠标跟随的十字架
        self.__help_info()          #绘制帮助信息区域，单独绘制在help_info_screen表面
        self.__func_input()         # 绘制函数信息输入区域，单独绘制在func_input_screen表面
        self.__darw_function()      #绘制输入的函数
        self.axis_screen.blit(self.help_info_screen, (self.help_screen_pos_x, 300))
        self.axis_screen.blit(self.func_input_screen, (int((self.screen_width-self.func_input_width-self.func_input_pos_y * 2)/2),self.func_input_screen_pos_y))
        self.screen.blit(self.axis_screen, (0, 0))

def set_difficulty(screen,width, height):
    # Do the job here !
    print("已经设置！")
    pass




def start_the_game(screen,width,height):
    FPS = 35
    pygame.display.set_caption("初等函数绘制系统")

    new_Rain_Curtain = rain_curtain.Rain_Curtain(screen, width, int(height/1))  # 定义一个雨滴链表，保存了很多个雨滴
    new_Rain_Curtain_Flag = True
    func_input_menu = pygame_menu.Menu("", 800, 60, position=(500, 0, False), theme=pygame_menu.themes.THEME_DARK)
    func_input_text = func_input_menu.add.text_input('',cursor_size=(2,28),input_underline='_',
                                                       maxchar=50)
    func_input_text.set_font(font='方正粗黑宋简体.ttf',font_size=26,color=(255, 105, 105, 255)
                                                                ,selected_color=(5, 255, 255, 255)
                                                                ,readonly_color=(255, 105, 105, 255)
                                                                ,readonly_selected_color=(255, 105, 105, 255)
                                                                ,background_color=(0, 0, 0, 0)
                             )
    func_input_text.set_font_shadow(enabled=True,offset=5)

    new_axis = Coordinate_axis(screen, width, height, func_input_menu,func_input_text)
    while True:  # 窗口主循环开始
        events = pygame.event.get()
        for event in events:  # 窗口事件监听开始
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_PAGEUP:
                    new_axis.scale_enlarge()
                elif event.key == pygame.K_PAGEDOWN:
                    new_axis.scale_reduce()
                elif event.key == pygame.K_RIGHT:
                    new_axis.origin_pixel_right()
                elif event.key == pygame.K_LEFT:
                    new_axis.origin_pixel_left()
                elif event.key == pygame.K_UP:
                    new_axis.origin_pixel_up()
                elif event.key == pygame.K_DOWN:
                    new_axis.origin_pixel_down()
                elif event.key == pygame.K_F1:
                    new_axis.help_info_show()
                elif event.key == pygame.K_F2:
                    if new_Rain_Curtain_Flag :
                        new_Rain_Curtain_Flag = False
                    else:
                        new_Rain_Curtain_Flag = True
                elif event.key == pygame.K_F3:
                    new_axis.mouse_cross_show()
                elif event.key == pygame.K_F4:
                    new_axis.mouse_text_show()
                elif event.key == pygame.K_F5:
                    new_axis.func_input_show()
                elif event.key == pygame.K_F6:
                    new_axis.function_clear()
                elif event.key == pygame.K_RETURN :
                    new_axis.get_function_text()

                elif event.key == pygame.K_KP_ENTER:
                    new_axis.get_function_text()

        ###游戏程序循环代码开始
        screen.fill(new_axis.get_bg_color())
        if func_input_menu.is_enabled():
            func_input_menu.update(events)
            #func_input_menu.draw(screen)
        if new_Rain_Curtain_Flag :
            new_Rain_Curtain.run()
        new_axis.darw()
        # new_axis.darw_fanction()

        pygame.time.delay(FPS)
        pygame.display.flip()  # 更新全部显示
    return None

def main():
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    MyWin =pygame.init()

    screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
    pygame.font.init()
    start_the_game(screen,width,height)
    # ##############################################################################################################
    # menu = pygame_menu.Menu('Draw Function', 800, 300, position=(50, 50, True),center_content=True,
    #                         theme=pygame_menu.themes.THEME_DARK)
    #
    # mytext_input=menu.add.text_input('用户名:', default='谢一鑫',font_name='方正粗黑宋简体.ttf')
    # mytext_input.set_value("mathfrog")
    # menu.add.selector('比例尺 :', [('300像素/刻度', 1), ('100像素/刻度', 2),('10像素/刻度', 3)], onchange=set_difficulty(screen,width, height),font_name='方正粗黑宋简体.ttf')
    # menu.add.button('开始绘制', start_the_game,screen,width,height,background_color=(0,124,11,50),border_color=(255,0,0),
    #                 font_name='方正粗黑宋简体.ttf',font_color=(0,0,255),font_size=40)
    # menu.add.button('开始', start_the_game,screen,width,height,font_name='方正粗黑宋简体.ttf')
    # menu.add.button('Quit',pygame_menu.events.EXIT, font_name='方正粗黑宋简体.ttf')
    #
    #
    # #menu.center_content()
    # menu.mainloop(screen)
    # ##############################################################################################################



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()