#  页面, 功能和关卡设计:

   * 设计游戏界面 `Scene`, 基于进出栈思想实现无需函数嵌套的界面平级切换;
   * 设计自机, 敌机和 `Boss` 类, 实现完美碰撞检测 (以自机类为例);
   * 设计子弹类 `Bullet` 和轨迹类 `Orbit`;
   * 设计并搭建示例关卡.


## 1. 设计游戏界面和界面切换系统


* 界面设计<br>
  本项目的界面类型分为静态 (Title, Menu, Pause, ScoreBoard, MusicRoom) 和动态 (Game) 两类. 由于时间所限, 暂时只完成了几个基本页面.

   静态页面主要由背景和选单组成, 图层复杂度低. 在本项目中, 菜单的选择和切换由事件检测实现, 选单和背景资源均以贴图形式导入至贴图资源管理器中并调用. 

   例: 主界面定义如下: 

   ```
   # -*- coding: UTF-8 -*-
   import pygame
   from pygame.locals import *
   import sys
   import globe
   from Scene import scene_loading


   class TitleMenu(object):
      """初始化菜单按钮, 设定菜单内容和淡出切换效果"""
      def __init__(self):
         """初始化主页面及按键"""
         self.button_rect = []  						# 获取按键的 'rect' 属性
         self.logo = (pygame.image.load("./Resources/pic/New/title/title_logo.png").convert_alpha()).subsurface(0,128,324,80)
         self.rs = globe.mgame.rsmanager.image		# rs = resource

         self.button_rect.append([400, 150])			# 定位 'Game_Start' 按键位置
         self.button_rect.append([410, 185])			# 定位 'Extra_Start' 按键位置
         self.button_rect.append([420, 220])			# 定位 'Practice Start' 按键位置
         self.button_rect.append([430, 255])			# 定位 'Replay' 按键位置
         self.button_rect.append([440, 290])			# 定位 'Player Data' 按键位置
         self.button_rect.append([450, 325])			# 定位 'Music Room' 按键位置
         self.button_rect.append([460, 360])			# 定位 'Option' 按键位置
         self.button_rect.append([470, 395])			# 定位 'Quit' 按键位置

         self.image = []				# 定义按键贴图, 以列表形式存储
         self.image.append(self.rs["Game_Startb"])			# 0
         self.image.append(self.rs["Game_Startd"])			# 1
         self.image.append(self.rs["Extra_Startb"])			# 2
         self.image.append(self.rs["Extra_Startd"])			# 3
         self.image.append(self.rs["Practise_Startb"])		# 4
         self.image.append(self.rs["Practise_Startd"])		# 5
         self.image.append(self.rs["Replayb"])				# 6
         self.image.append(self.rs["Replayd"])				# 7
         self.image.append(self.rs["Player_Datab"])			# 8
         self.image.append(self.rs["Player_Datad"])			# 9
         self.image.append(self.rs["Music_Roomb"])			# 10
         self.image.append(self.rs["Music_Roomd"])			# 11
         self.image.append(self.rs["Optionb"])				# 12
         self.image.append(self.rs["Optiond"])				# 13
         self.image.append(self.rs["Quitb"])					# 14
         self.image.append(self.rs["Quitd"])					# 15

         self.index = 0				# 初始化高亮按键: 默认为 'Start'
         self.choose = False			# 初始化按键选定状态
         self.flash = 0				# 初始化按键闪烁帧

         # 设定页面切换效果: 淡出
         self.fade = pygame.Surface(globe.mgame.screen.get_size())		# 设定遮罩尺寸
         self.fade.fill((0, 0, 0))		# 以纯黑色填充遮罩

      def event_control(self):
         """事件控制函数"""
         if not self.choose:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()
               if event.type == KEYDOWN:
                  if event.key == pygame.K_F4 and event.mod == pygame.KMOD_LALT:
                     pygame.quit()
                     sys.exit()
                  if event.key == K_UP:
                     if self.index != 0:
                        self.index -= 1
                        self.button_rect[self.index][0] -= 5				# 按键微移动画
                        self.button_rect[self.index + 1][0] += 5			# 按键微移动画
                        globe.mgame.msmanager.play_SE("select")
                  if event.key == K_DOWN:
                     if self.index != 7:
                        self.index += 1
                        self.button_rect[self.index][0] -= 5				# 按键微移动画
                        self.button_rect[self.index - 1][0] += 5			# 按键微移动画
                        globe.mgame.msmanager.play_SE("select")
                  if event.key == K_z:
                     self.choose = True
                     globe.mgame.msmanager.play_SE("select")
         else:				# 检测进行按键选择后的状态
            self.flash += 1
            if self.flash >= 20:				# 按键闪烁 20 下后进行页面切换
               if self.index == 0:
                  if self.flash >= 40:		# 按键闪烁 40 下后进行页面切换
                     globe.mgame.goto(scene_loading.Scene_Loading)
               if self.index == 1:
                  print("Extra_Start_Debug")
               if self.index == 2:
                  print("Practise_Start_Debug")
               if self.index == 3:
                  print("Replay_Debug")
               if self.index == 4:
                  print("Player_Data_Debug")
               if self.index == 5:
                  print("Music_Room_Debug")
               if self.index == 6:
                  print("Option_Debug")
               if self.index == 7:
                  pygame.quit()
                  sys.exit()

            if (self.flash % 2) == 0 and (self.flash <= 40):		# 控制按键闪烁效果
               tmp = self.image[self.index*2]
               self.image[self.index*2] = self.image[self.index*2+1]
               self.image[self.index*2+1] = tmp

      def draw(self, screen):
         """定义菜单绘制函数"""
         # 绘制 Logo
         screen.blit(self.logo, (32, 200))

         # 绘制屏幕按键
         for i in range(0, 8):
            screen.blit(self.image[2*i + 1], self.button_rect[i])
         screen.blit(self.image[2*self.index], self.button_rect[self.index])

         # 定义淡出效果遮罩循环
         if self.flash >= 20:
            self.fade.set_alpha((self.flash-20)*12)			# 对黑色遮罩进行透明化
            screen.blit(self.fade, (0, 0))					# 在屏幕上绘制半透明遮罩模拟淡出效果


   class Scene_Title(object):
      """定义主页面类"""
      # 去尼玛的驼峰命名法
      def __init__(self):
         """初始化主页面"""
         self.rs = globe.mgame.rsmanager
         self.menu = TitleMenu()
         self.count = 0
         self.fade = pygame.Surface(globe.mgame.screen.get_size())

      def update(self):
         """主页面屏幕更新函数"""
         self.menu.event_control()

      def draw(self, screen):
         """绘制背景"""
         screen.blit(self.rs.image["background"], (0, 0))
         self.menu.draw(screen)

         # 淡入效果
         if self.count <= 40:
            self.fade.set_alpha((255 - self.count * 12))  # 对黑色遮罩进行透明化
            screen.blit(self.fade, (0, 0))
            self.count += 1

   ```
  
  设计(~~照抄~~)的主界面如下图: 
  
  <center>
  
  ![](./Tut_Resources/Title.png)

   </center>


* 界面切换<br>
  常规的游戏界面切换方式是通过函数的嵌套调用实现的. 玩家每切换一次界面, 都是从当前函数调用一个新函数而 "切换" 到下一个界面的, 并没有跳出当前函数. 
  当切换了多个层级时, 函数之间的层层嵌套就会明显影响游戏运行速度. 在本项目中, 我们将游戏场景界面视为栈中存储的元素, 在启动游戏时自动地将最先调用
  的界面 (如 `Loading` 或 `Title`) 入栈, 而需要新界面时, 将新界面入栈, 并切换到新界面, 切换回原界面时则从栈中弹出新界面. 这样, 场景切换而导致的
  函数嵌套调用问题即可得到解决. 
  
  在 `GameWindow` 类中, 我们需要初始化界面栈: 
  
  ```
  self.stack = []									 # 定义界面栈, 防止scene函数重复调用
  ```
  
  同时需要在类中定义三个方法: 
  ```
  	def goto(self, scene):
		"""切换到 'scene'. 注意: 当且仅当游戏冷启动时可用该函数!"""
		self.scene = scene()
		self.scene.update()

	def call(self,scene):
		"""从当前界面切换到 'scene' """
		self.scene.stop()
		self.stack.append(self.scene)			# 新界面入栈
		self.scene = scene()					# 切换到新界面

	def back(self):
		"""切换回原界面"""
		self.scene = self.stack.pop()			# 原界面出栈
		self.scene.start()						# 切换回原界面  
  ```
  
<br>

## 2. 设计自机, 敌机和 `Boss` 类


  自机, 敌机和 Boss 是游戏中玩家直接操控或互动的对象. 它们的形象 (贴图, 动画), 位置, 血量 (点数, 能量值), 状态 (正常, 中弹, ...) 和行为会动态变化, 相关的变量和控制这些变量变化的方法都应该在对应的类中妥善定义. 

* 自机类<br>
  对于自机, 我们首先明确, 它具有 `正常`, `正常下放B`, `中弹`, `中弹后`, `中弹后放B`, `坠机(残机为0)` 六种不同状态, 并且它的移动轨迹需要玩家通过方向键控制. 我们将自机类分为三个部分: 贴图/动画定义, 状态定义和行为控制.<br>  

  * 动画定义<br>
  首先, 我们对自机动画进行定义. 自机不同状态下的动画已经预先被导入至贴图资源管理器中, 我们只需要将其简单导入列表按照顺序储存即可:
      ```
      class Player(object):
         """定义自机类: 点数, 能量值, 状态, 运动, 动画, 帧刷新"""

         def __init__(self):
            global resource						# 全局变量: 资源管理器
            global canime  						# 全局变量: 自机动画
            global cstatus  					# 全局变量: 自机状态
            resource = globe.mgame.rsmanager
            self.game_active_rect = globe.game_active_rect		# 设定游戏活动区域
            self.point = [224.0, 450.0]			# 初始化到屏幕底部中央
            self.rect = Rect(0, 0, 10, 10)		# 获取自机图像矩形遮罩

         ---snip---

         canime = {}
            canime["stay"] = resource.anime["player"][0]
            canime["toleft"] = resource.anime["player"][1]
            canime["toright"] = resource.anime["player"][2]
            canime["focus"] = resource.anime["player"][3]
            self.anime = canime["stay"]			# 自机动画, 初始化为 'stay' 类型
            self.aindex = 0						# 自机动画的当前播放帧, 初始化为0
      ```

   <br>

   * 状态定义<br>

         其次, 我们对自机的六种不同状态分别进行定义: 

         ```
            def __init__(self):

            ---snip---

            cstatus = {}
            cstatus["normal"] = 0
            cstatus["invincible"] = 1
            cstatus["crash"] = 2
            cstatus["sc"] = 3
            cstatus["scinvincible"] = 4
            cstatus["hit"] = 5
            self.status = cstatus["normal"]
            globe.cstatus = cstatus

            ---snip---


         ```

         在行为控制部分中, 我们将定义自机的各种可能行为, 并依据自机状态的不同进行特定化的行为控制.  

   <br>

   * 行为控制<br>
     行为控制部分细分为动作行为控制和位置行为控制. 开火, 放B等行为均可归类为动作行为, 而位置行为控制顾名思义, 即控制自机移动, 限制移动范围和后期实现顶上收点, 穿墙, 低速 (Focus) 模式等的分区. 

      ```
      def fire(self):
         """定义开火动作, 维护子弹数量与频率, 自机子弹类"""
         if not globe.scgame.timestop:
            tm = globe.scgame.tmmanager
            bl = globe.scgame.blmanager
            if (self.frame % 5 == 0):
               bl.create_plbl(self.rect.inflate(-12, -8).topleft, 0)
               bl.create_plbl(self.rect.inflate(-12, -8).topright, 0)
            tp = self.power/100
            if tp >= 5:
               tp = 4
            for i in range(int(tp)):
               if (self.frame % 6 == 0):
                  bl.create_plbl(tm.rect[i].center, 1)
                  bl.create_plbl(tm.rect[i].center, 2)

      def firebomb(self):
         """定义Bomb行为, 维护Bomb设定"""
         if (self.power >= 100 and self.status != cstatus["sc"]) and (
               self.status != cstatus["scinvincible"]) and (not globe.scgame.timestop):
            self.power -= 100
            self.status = cstatus["sc"]
            globe.mgame.msmanager.play_SE("invincible")

      def miss(self):
         """定义自机中弹行为, 维护中弹行为"""
         if self.status == cstatus["hit"]:
            # 生成三个P点
            globe.scgame.anmanager.create_anime(resource.anime["bubble"], self.rect.topleft, 5)
            globe.scgame.blmanager.clear_enbl()
            rc = self.rect.copy()
            rc.left -= 20
            globe.scgame.itmanager.create(item.LPowerItem, rc.topleft)
            rc.left += 20
            globe.scgame.itmanager.create(item.LPowerItem, rc.midtop)
            rc.left += 20
            globe.scgame.itmanager.create(item.LPowerItem, rc.topright)

            self.status = cstatus["crash"]
            # 设判定点位置为自机撞弹时所处位置
            self.tmpfc = [self.point[0], self.point[1]]				# tmpfc = tmp_focus
            
            # 重定位自机至屏幕底部中央
            self.rect.midtop = self.game_active_rect.midbottom
            self.point[0] = self.rect.centerx		
            self.point[1] = self.rect.centery
            self.tcount = 0				# 重置计时器
            self.life -= 1				# 残机 -1
            self.power -= 200			# Power -200
            if self.power <= 0:
               self.power = 0

      def move(self):
         """定义和控制自机移动行为, 维护移动检测函数, 高速/低速模式切换, 穿墙功能和顶上收点机能"""
         keys = self.keys
         if keys[pygame.K_z]:
            self.fire()
         if keys[pygame.K_x]:
            self.firebomb()
         if keys[pygame.K_LSHIFT]:
            self.speed = 1.5
         else:
            self.speed = 8
         if (keys[pygame.K_DOWN] or keys[pygame.K_UP]) and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            self.speed /= sqrt(2)
         if keys[pygame.K_DOWN]:
            self.point[1] += self.speed
         if keys[pygame.K_UP]:
            self.point[1] -= self.speed
         if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
            if self.anime != canime["stay"]:
               self.anime = canime["stay"]
               self.aindex = 0
         elif keys[pygame.K_RIGHT]:
            if self.anime != canime["toright"]:
               self.anime = canime["toright"]
               self.aindex = 0
            self.point[0] += self.speed
         elif keys[pygame.K_LEFT]:
            if self.anime != canime["toleft"]:
               self.anime = canime["toleft"]
               self.aindex = 0
            self.point[0] -= self.speed
         if (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
            if self.anime != canime["stay"]:
               self.anime = canime["stay"]
               self.aindex = 0

         self.rect.size = self.anime[self.aindex].get_size()
         self.rect.center = (int(self.point[0]), int(self.point[1]))

         # 限位
         if self.rect.top < self.game_active_rect.top:
            self.rect.top = self.game_active_rect.top
            self.point[1] = self.rect.centery
         elif self.rect.bottom > self.game_active_rect.bottom:
            self.rect.bottom = self.game_active_rect.bottom
            self.point[1] = self.rect.centery

         # 穿墙
         if self.rect.centerx <= self.game_active_rect.left:
            self.rect.centerx = self.game_active_rect.right
            self.point[0] = self.rect.centerx
            globe.mgame.msmanager.play_SE("select")
         elif self.rect.centerx >= self.game_active_rect.right:
            self.rect.centerx = self.game_active_rect.left
            self.point[0] = self.rect.centerx
            globe.mgame.msmanager.play_SE("select")

         # 顶上收点系统
         if self.rect.top < 100:
            globe.scgame.itmanager.getitem()

         # 自动循环播放自机动画
         if self.frame % 6 == 0:
            self.aindex += 1
         if self.aindex >= len(self.anime):
            if self.anime == canime["stay"]:
               self.aindex = 0
            else:
               self.aindex -= 4

      def hit(self):
         """定义撞弹后动作"""
         if self.status == cstatus["normal"]:
            globe.mgame.msmanager.play_SE("miss")
            self.tcount = 0		# 重置记时器
            self.status = cstatus["hit"]

      def update(self):
         """自机刷新函数"""
         # 限制自机能量阈值为500
         if self.power > 500:
            self.power = 500
         self.keys = pygame.key.get_pressed()
         if self.status == cstatus["hit"]:
            if self.tcount >= 20:
               self.miss()
            else:
               self.tcount += 1

         if self.status != cstatus["crash"]:
            self.move()
         else:
            self.tcount += 1
            if self.life < 0 and self.tcount == 20:
               globe.hiscore = globe.scgame.high_score
               globe.mgame.call(scene_gameover.Scene_GameOver)
            if self.tcount <= 60:
               self.point[1] -= 1
            else:
               self.status = cstatus["invincible"]
               self.tcount = 0

         if self.status == cstatus["invincible"]:
            self.tcount += 1
            if self.tcount > 300:
               self.status = cstatus["normal"]
               self.tcount = 0
         elif self.status == cstatus["sc"]:
            self.tcount += 1
            if self.tcount > 360:
               self.status = cstatus["scinvincible"]
               globe.scgame.blmanager.clear_enbl()
               self.tcount = 0
         elif self.status == cstatus["scinvincible"]:
            self.tcount += 1
            if self.tcount > 180:
               self.status = cstatus["normal"]
               self.tcount = 0
         self.frame += 1
      ```

      我们可以在 `PyGame` 中调用内置函数进行 `Sprite` 和组之间, 组与组之间, `Sprite` 和 `Sprite` 之间的矩形碰撞检测和像素级碰撞检测. 


      `Sprite` 和 `Sprite` 之间的矩形碰撞检测: 
      ```
      pygame.sprite.collide_rect(first, second) #返回布尔值`
      ```


      `Sprite` 和组 之间的矩形碰撞检测

      ```
      #第一个参数是 Sprite，
      #第二个参数是 Sprite Group，
      #第三个参数为True，则碰撞检测后，组中所有碰撞的 Sprite 被删除
      #返回值为组中被碰撞的 Sprite
      collide_list = pygame.sprite.spritecollide(sprite,group,False)
      ```

      组与组之间的矩形碰撞检测

      ```
      #前两个参数都是组
      #后两个参数，代表发生碰撞时，是否删除 Sprite
      #该函数返回一个字典
      #第一个组中的每一个 Sprite 都会添加到字典中
      #第二组中与之碰撞的 Sprite 会添加到字典相应的条目中
      hit_list = pygame.sprite.groupcollide(group1,group2,True,False)
      ```
      如我们使用的 `Sprite` 贴图具透明背景, 则可以使用下列方法进行像素级碰撞检测 (又称完美碰撞检测): 

      首先, 要为被检测的 `Sprite` 赋予 `mask` 属性. 
      ```
      self.mask = pygame.mask.from_surface(self.image)
      ```

      其次, 调用函数执行像素级碰撞检测:
      ```
      pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
      ```

      <br>

      在本项目中, 自机的碰撞检测即为完美碰撞检测. 

<br>

## 3. 设计子弹类 `Bullet` 和轨迹类 `Orbit`