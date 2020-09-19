# 特色机能实现和功能改进
   * 实现低速模式, 顶上收点和穿墙模式等 `Touhou STG` 的特色机能.

1. 低速模式<br>
   实现原理: 事件检测函数侦测到用户按下左 `Shift` 键后, 改写自机移动速度; 侦测到用户松开该键后, 将移动速度改回初始定义值. 

   ```
   	if keys[pygame.K_LSHIFT]:
		self.speed = 1.5
	else:
		self.speed = 8
   ```

   <br>

2. 顶上收点<br>
   实现原理: 检测到自机中心位置到屏幕顶端的距离小于某个常数时, 调用 "收点" 函数. 
   
   ```
    # 顶上收点系统
	if self.rect.top < 100:
		globe.scgame.itmanager.getitem()

    ---snip---

	def getitem(self):
	"""收点函数"""
	for i in self.item:
		i.status = itstatus["fly"]

    ---snip---

	def update(self):
		tmp = []
		for i in self.item:
			if i.status == itstatus["normal"]:
				
            ---snip---

			else:
				dx = player.point[0] - i.rect.centerx
				dy = player.point[1] - i.rect.centery
				dist = sqrt(dx**2+dy**2)
				if dist == 0:
					dist = 0.0001
				i.vx = int(self.fspeed*dx/dist)
				i.vy = int(self.fspeed*dy/dist)
				i.rect.left += i.vx
				i.rect.top += i.vy
				if i.rect.collidepoint(player.point):
					i.buffer()
					tmp.append(i)
		for i in tmp:
			self.item.remove(i)
   ```

<br>

3. 穿墙模式:<br>
   实现原理: 若检测到自机中心位置距离屏幕左/右边缘小于某个恒定值, 则将自机中心位置横坐标修改为屏幕右/左边缘处. 

   ```
    # 穿墙
	if self.rect.centerx <= self.game_active_rect.left:
		self.rect.centerx = self.game_active_rect.right
		self.point[0] = self.rect.centerx
		globe.mgame.msmanager.play_SE("select")
	elif self.rect.centerx >= self.game_active_rect.right:
		self.rect.centerx = self.game_active_rect.left
		self.point[0] = self.rect.centerx
		globe.mgame.msmanager.play_SE("select")
   ```