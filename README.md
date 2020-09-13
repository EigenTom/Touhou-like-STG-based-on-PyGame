# README

大家好, 就不自我介绍了. 该系列笔记以分析和说明成果 "一个基于  `PyGame` 的类 `Touhou STG` 游戏完整框架" 的程序结构的形式, 记录了本人学习 `PyGame` 过程中总结的部分要点, 经验和知识. 

该笔记分为四个部分: 
1. 基本概念和指令: <br> 
   * 引入面向对象编程和模块化程序设计与游戏资源管理的思想, 为后续的框架搭建打下基础;
   * 介绍 `PyGame` 中的数个基本概念: 窗口, 事件, 屏幕刷新, 资源管理, `Sprite` (精灵);
   * 介绍主窗口和 `Sprite` 的基本定义与使用方法, 解释利用 `subsurface` 实现贴图自动分割的方法;
   * 介绍 `Sprite` 的贴图变换与运动轨迹规划方法.

<br>

2. 项目框架和资源管理:
   * 搭建整体框架, 便于游戏的后续完善和开发; 
   * 设计和编写游戏主窗口 `Game_Window` 类, 实现窗口刷新等基础功能;
   * 搭建游戏贴图资源管理器, 导入并自动化分割 `Sprite` 贴图, 构成 `Animation` 或 `image` 格式化储存, 以备后续取用; 
   * 搭建游戏音频资源管理器, 导入并格式化储存音效和背景音乐, 以备后续取用.

<br>

3. 页面, 功能和关卡设计:
   * 设计游戏界面 `Scene`, 基于进出栈思想实现无需函数嵌套的界面平级切换;
   * 设计自机, 敌机和 `Boss` 类, 实现完美碰撞检测;
   * 设计子弹类 `Bullet` 和轨迹类 `Orbit`;
   * 设计并搭建示例关卡.

<br>

4. 特色机能实现和功能改进
   * 实现低速模式, 顶上收点和穿墙模式等 `Touhou STG` 的特色机能.


完整的游戏程序和资源位于 `/Game` 中, 主程序为 `main.py`, 该项目的逻辑结构见笔记第二章. 

游戏贴图和音频资源取自东方第10作 《东方风神录》, 部分关卡设计和弹幕射击参考了
https://github.com/takahirox/toho-like-js <br>
https://github.com/TkhiienLok/Touhou <br>
https://github.com/jikaiwen/pygame-touhou <br>

教程和界面设计, 关卡设计仍未完成, 持续更新中

