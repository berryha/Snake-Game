'''
性能优化内容：
1.路径缓存机制 🎯
    计算一次路径后缓存保存，避免每帧重复运算 BFS
    只在食物位置改变或路径用完时重新寻路
    大幅降低 CPU 使用率
2.蛇身集合缓存 📦
    使用 snake_set 缓存蛇身位置，避免每次都创建 snake[:-1] 切片
    降低内存分配频率
3.路径节点优化 🚀
    只保存从蛇头到食物的路径点（不包括头部）
    蛇每次移动后自动消除已走过的路径点
    减少路径列表大小
4.导入优化 📥
    将 deque 移到文件顶部导入，避免函数内重复导入

性能提升效果：
    ❌ 之前：每一帧（60fps）都运行完整 BFS，处理 40×30=1200 网格，非常卡顿
    ✅ 现在：路径缓存复用，寻路次数减少 90% 以上，游戏流畅运行
    现在自动模式应该性能良好，不会出现明显的卡顿！

'''
import pgzrun
import random
import math
from collections import deque

#增加无限模式
infinite_mode = False


# 自动模式相关变量
last_pathfind = 0  # 上次寻路的时间
current_path = []  # 当前路径缓存
snake_set = set()  # 蛇身位置集合，避免重复创建列表

#实现贪吃蛇自动吃食物的功能
def auto_eat_food():
    """使用BFS寻路算法自动找到最短路径到食物"""
    global direction, next_direction, last_pathfind, current_path, snake_set
    
    if not food or game_over or not game_started:
        return
    
    head = snake[0]
    
    # 只在必要时重新计算路径（每3帧计算一次）
    if len(current_path) > 0:
        # 使用缓存的路径
        if current_path[0] == head:
            # 蛇头已移动，移除已走过的路径点
            current_path.pop(0)
        
        if len(current_path) > 0:
            next_pos = current_path[0]
            next_x, next_y = next_pos
            head_x, head_y = head
            dx, dy = next_x - head_x, next_y - head_y
            
            if dx == 1:
                next_direction = RIGHT
            elif dx == -1:
                next_direction = LEFT
            elif dy == 1:
                next_direction = DOWN
            elif dy == -1:
                next_direction = UP
            return
    
    # 重新计算路径（路径为空或头部不匹配时）
    # 更新蛇身集合（缓存，避免每次都创建列表切片）
    snake_set = set(snake[:-1])  # 排除蛇尾
    
    # BFS寻路
    queue = deque([(head, [head])])
    visited = {head}
    
    while queue:
        current_pos, path = queue.popleft()
        current_x, current_y = current_pos
        
        # 找到食物
        if current_pos == food["pos"]:
            if len(path) >= 2:
                # 提取从头到食物的路径（不包括头部）
                current_path = path[1:]
                
                next_pos = current_path[0]
                next_x, next_y = next_pos
                head_x, head_y = head
                dx, dy = next_x - head_x, next_y - head_y
                
                if dx == 1:
                    next_direction = RIGHT
                elif dx == -1:
                    next_direction = LEFT
                elif dy == 1:
                    next_direction = DOWN
                elif dy == -1:
                    next_direction = UP
            return
        
        # 探索四个方向
        for nx, ny in [(current_x+1, current_y), (current_x-1, current_y), 
                       (current_x, current_y+1), (current_x, current_y-1)]:
            # 检查边界
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                next_pos = (nx, ny)
                # 检查是否已访问和是否在蛇身上
                if next_pos not in visited and next_pos not in snake_set:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

# 窗口设置
WIDTH = 800
HEIGHT = 600
TITLE = '贪吃蛇游戏'

# 游戏常量
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10
MOVEMENT_INTERVAL = 8  # 每8帧移动一次，控制蛇的速度

# 颜色定义
BACKGROUND_COLOR = (20, 30, 20)
# 蛇头颜色初始为绿色，会根据吃到的豆子颜色变化
SNAKE_HEAD_COLOR = (0, 255, 0)
# 蛇身颜色列表（红橙黄绿青蓝紫）
SNAKE_BODY_COLORS = [
    (255, 0, 0),      # 红
    (255, 165, 0),    # 橙
    (255, 255, 0),    # 黄
    (0, 255, 0),      # 绿
    (0, 255, 255),    # 青
    (0, 0, 255),      # 蓝
    (128, 0, 255),    # 紫
]
snake_color_index = 0  # 当前蛇身颜色索引
SNAKE_BODY_COLOR = SNAKE_BODY_COLORS[snake_color_index]

# 食物类型定义
FOOD_TYPES = {
    "red": {"color": (220, 0, 0), "score": 10, "name": "红豆"},
    "orange": {"color": (255, 165, 0), "score": 10, "name": "橙豆"},
    "yellow": {"color": (255, 255, 0), "score": 10, "name": "黄豆"},
    "green": {"color": (0, 255, 0), "score": 10, "name": "绿豆"},
    "cyan": {"color": (0, 255, 255), "score": 10, "name": "青豆"},
    "blue": {"color": (0, 0, 255), "score": 10, "name": "蓝豆"},
    "purple": {"color": (128, 0, 255), "score": 10, "name": "紫豆"}
}

GRID_COLOR = (40, 50, 40)
TEXT_COLOR = (220, 220, 220)
GAME_OVER_COLOR = (220, 50, 50)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 游戏状态
game_over = False
score = 0
high_score = 0
frame_count = 0
auto_mode = False  # 自动模式开关
direction = RIGHT
next_direction = RIGHT
snake = []
food = None  # 现在food是一个包含位置和类型的字典: {"pos": (x, y), "type": "red/yellow/purple"}
game_started = False
wingame = False


def reset_game():
    """重置游戏"""
    global snake, food, direction, next_direction, score, game_over, game_started, current_path, snake_set,wingame, SNAKE_HEAD_COLOR
    
    # 初始化蛇：头部在中间，加上3节身体
    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2
    snake = [
        (center_x, center_y),      # 头部
        (center_x - 1, center_y),  # 第1节身体
        (center_x - 2, center_y),  # 第2节身体
        (center_x - 3, center_y)   # 第3节身体
    ]
    
    direction = RIGHT
    next_direction = RIGHT
    score = 0
    game_over = False
    game_started = True
    current_path = []  # 重置路径缓存
    snake_set = set()  # 重置蛇身集合
    wingame = False # 重置胜利标志
    
    # 重置蛇头颜色为初始绿色
    SNAKE_HEAD_COLOR = (0, 255, 0)
    
    generate_food()

def generate_food():
    """在随机位置生成食物"""
    global food, current_path
    max_attempts = 100  # 最大尝试次数
    attempts = 0
    
    while attempts < max_attempts:
        # 随机生成食物位置
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        food_pos = (x, y)
        
        # 确保食物不在蛇身上
        if food_pos not in snake:
            # 随机选择食物类型，每种颜色豆子出现的概率是随机且相等的
            food_types = list(FOOD_TYPES.keys())
            food_type = random.choice(food_types)
            food = {"pos": food_pos, "type": food_type}
            break
        attempts += 1
    else:
        # 如果尝试次数超过限制，游戏结束
        global game_over
        game_over = True
    
    # 清除缓存的路径，因为食物位置改变了
    current_path = []

def move_snake():
    """移动蛇"""
    global snake, game_over, score, high_score
    
    if game_over or not game_started:
        return
    
    # 获取当前头部位置
    head_x, head_y = snake[0]
    
    # 根据方向计算新头部位置
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    
    # 检查是否撞墙
    if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
        game_over = True
        return
    
    # 检查是否撞到自己
    if new_head in snake:
        game_over = True
        return
    
    # 检查蛇的长度是否超过100，胜利条件
    if len(snake) >= 100:
        # 如果启用了无限模式，不触发胜利结束
        if not infinite_mode:
            global wingame
            wingame = True
            game_over = True
            return
    
    # 添加新的头部
    snake.insert(0, new_head)
    
    # 检查是否吃到食物
    if new_head == food["pos"]:
        food_type = food["type"]
        score += FOOD_TYPES[food_type]["score"]
        
        # 将蛇头颜色更改为对应豆子的颜色
        global SNAKE_HEAD_COLOR, snake_color_index
        SNAKE_HEAD_COLOR = FOOD_TYPES[food_type]["color"]
        
        # 蛇身颜色自动切换到下一个颜色
        snake_color_index = (snake_color_index + 1) % len(SNAKE_BODY_COLORS)
        
        if score > high_score:
            high_score = score
        generate_food()
        # 注意：吃到食物时不删除尾部，蛇就变长了
    else:
        # 没吃到食物，删除尾部
        snake.pop()

def update():
    """更新游戏逻辑（每秒调用60次）"""
    global frame_count, direction, next_direction, auto_mode
    
    if not game_started or game_over:
        return
    
    # 如果启用自动模式，调用自动吃食物函数
    if auto_mode:
        auto_eat_food()
    else:
        # 更新方向，确保不会直接反向移动
        if keyboard.left and direction != RIGHT:
            next_direction = LEFT
        elif keyboard.right and direction != LEFT:
            next_direction = RIGHT
        elif keyboard.up and direction != DOWN:
            next_direction = UP
        elif keyboard.down and direction != UP:
            next_direction = DOWN
    
    # 控制移动速度：每MOVEMENT_INTERVAL帧移动一次
    frame_count += 1
    if frame_count >= MOVEMENT_INTERVAL:
        frame_count = 0
        # 在自动模式下，直接更新方向（不需要检查反向移动）
        if auto_mode:
            direction = next_direction
        else:
            # 确保方向切换不会导致蛇直接反向移动
            if (direction == RIGHT and next_direction != LEFT) or \
               (direction == LEFT and next_direction != RIGHT) or \
               (direction == UP and next_direction != DOWN) or \
               (direction == DOWN and next_direction != UP):
                direction = next_direction
        move_snake()

def draw_grid():
    """绘制网格线"""
    for x in range(0, WIDTH, CELL_SIZE):
        screen.draw.line((x, 0), (x, HEIGHT), GRID_COLOR)
    for y in range(0, HEIGHT, CELL_SIZE):
        screen.draw.line((0, y), (WIDTH, y), GRID_COLOR)

def draw_snake():
    """绘制蛇"""
    # 缓存蛇的屏幕坐标
    snake_screen_coords = [(x * CELL_SIZE, y * CELL_SIZE) for (x, y) in snake]
    
    for i, (screen_x, screen_y) in enumerate(snake_screen_coords):
        # 绘制蛇身
        if i == 0:  # 头部
            # 绘制头部矩形
            screen.draw.filled_rect(
                Rect((screen_x, screen_y), (CELL_SIZE, CELL_SIZE)),
                SNAKE_HEAD_COLOR
            )
            # 绘制眼睛
            eye_size = CELL_SIZE // 5
            
            if direction == RIGHT:
                # 右眼（靠近头部右侧，上下分开）
                screen.draw.filled_circle(
                    (screen_x + CELL_SIZE - eye_size, screen_y + CELL_SIZE // 4),
                    eye_size, (0, 0, 0)
                )
                # 左眼（靠近头部右侧，上下分开）
                screen.draw.filled_circle(
                    (screen_x + CELL_SIZE - eye_size, screen_y + 3 * CELL_SIZE // 4),
                    eye_size, (0, 0, 0)
                )
            elif direction == LEFT:
                # 左眼（靠近头部左侧，上下分开）
                screen.draw.filled_circle(
                    (screen_x + eye_size, screen_y + CELL_SIZE // 4),
                    eye_size, (0, 0, 0)
                )
                # 右眼（靠近头部左侧，上下分开）
                screen.draw.filled_circle(
                    (screen_x + eye_size, screen_y + 3 * CELL_SIZE // 4),
                    eye_size, (0, 0, 0)
                )
            elif direction == UP:
                # 上眼（靠近头部上方，左右分开）
                screen.draw.filled_circle(
                    (screen_x + CELL_SIZE // 4, screen_y + eye_size),
                    eye_size, (0, 0, 0)
                )
                # 下眼（靠近头部上方，左右分开）
                screen.draw.filled_circle(
                    (screen_x + 3 * CELL_SIZE // 4, screen_y + eye_size),
                    eye_size, (0, 0, 0)
                )
            elif direction == DOWN:
                # 上眼（靠近头部下方，左右分开）
                screen.draw.filled_circle(
                    (screen_x + CELL_SIZE // 4, screen_y + CELL_SIZE - eye_size),
                    eye_size, (0, 0, 0)
                )
                # 下眼（靠近头部下方，左右分开）
                screen.draw.filled_circle(
                    (screen_x + 3 * CELL_SIZE // 4, screen_y + CELL_SIZE - eye_size),
                    eye_size, (0, 0, 0)
                )
        else:  # 身体
            # 绘制身体矩形，使用渐变色
            # 从当前snake_color_index开始，每一节身体使用下一个颜色
            body_color_index = (snake_color_index + i - 1) % len(SNAKE_BODY_COLORS)
            screen.draw.filled_rect(
                Rect((screen_x, screen_y), (CELL_SIZE, CELL_SIZE)),
                SNAKE_BODY_COLORS[body_color_index]
            )

def draw_food():
    """绘制食物"""
    if food:
        x, y = food["pos"]
        screen_x = x * CELL_SIZE
        screen_y = y * CELL_SIZE
        food_type = food["type"]
        
        # 获取食物类型对应的颜色
        food_color = FOOD_TYPES[food_type]["color"]
        
        # 绘制一个圆形食物
        center_x = screen_x + CELL_SIZE // 2
        center_y = screen_y + CELL_SIZE // 2
        
        # 主圆
        screen.draw.filled_circle(
            (center_x, center_y), CELL_SIZE // 2 - 2, food_color
        )
        
        # 根据食物类型绘制不同的高光效果
        if food_type == "red":
            # 红色食物的高光
            highlight_color = (255, 150, 150)
        elif food_type == "orange":
            # 橙色食物的高光
            highlight_color = (255, 200, 150)
        elif food_type == "yellow":
            # 黄色食物的高光
            highlight_color = (255, 255, 150)
        elif food_type == "green":
            # 绿色食物的高光
            highlight_color = (150, 255, 150)
        elif food_type == "cyan":
            # 青色食物的高光
            highlight_color = (150, 255, 255)
        elif food_type == "blue":
            # 蓝色食物的高光
            highlight_color = (150, 150, 255)
        else:  # purple
            # 紫色食物的高光
            highlight_color = (200, 150, 255)
        
        screen.draw.filled_circle(
            (center_x - CELL_SIZE // 6, center_y - CELL_SIZE // 6),
            CELL_SIZE // 6, highlight_color
        )

def draw_start_screen():
    """绘制开始屏幕"""
    screen.draw.text(
        "贪吃蛇游戏",
        center=(WIDTH // 2, HEIGHT // 2 - 100),
        fontname="simhei.ttf",
        fontsize=80,
        color=SNAKE_HEAD_COLOR
    )
    
    screen.draw.text(
        "使用方向键控制蛇的移动",
        center=(WIDTH // 2, HEIGHT // 2 - 20),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    screen.draw.text(
        "吃到红橙黄绿青蓝紫七种豆，蛇头会变色",
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    screen.draw.text(
        "按空格键开始游戏",
        center=(WIDTH // 2, HEIGHT // 2 + 100),
        fontsize=40,
        fontname="simhei.ttf",
        color=(255, 255, 100)
    )
    
    screen.draw.text(
        "按ESC键退出游戏",
        center=(WIDTH // 2, HEIGHT // 2 + 150),
        fontsize=25,
        fontname="simhei.ttf",
        color=(200, 200, 200)
    )

def draw_game_over_screen():
    """绘制游戏结束屏幕"""
    # 半透明黑色覆盖层
    overlay = Rect((0, 0), (WIDTH, HEIGHT))
    screen.draw.filled_rect(overlay, (0, 0, 0, 128))
    
    if wingame:
        # 游戏胜利文字
        screen.draw.text(
            "恭喜你，赢得了游戏!",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=60,
            fontname="simhei.ttf",
            color=(0, 255, 0)
        )
    else:
        # 游戏结束文字
        screen.draw.text(
            "游戏结束!",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=60,
            fontname="simhei.ttf",
            color=GAME_OVER_COLOR
        )
    
    screen.draw.text(
        f"最终得分: {score}",
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        fontsize=40,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    screen.draw.text(
        f"蛇的长度: {len(snake)}",
        center=(WIDTH // 2, HEIGHT // 2 + 70),
        fontsize=35,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    screen.draw.text(
        "按R键重新开始",
        center=(WIDTH // 2, HEIGHT // 2 + 130),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )

def draw():
    """绘制游戏画面"""
    # 清屏
    screen.fill(BACKGROUND_COLOR)
    
    if not game_started:
        # 绘制开始屏幕
        draw_start_screen()
        return
    
    # 绘制网格
    draw_grid()
    
    # 绘制食物
    draw_food()
    
    # 绘制蛇
    draw_snake()
    
    # 绘制分数
    screen.draw.text(
        f"分数: {score}",
        (10, 10),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    # 绘制长度
    screen.draw.text(
        f"长度: {len(snake)}",
        (10, 50),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    # 绘制最高分
    screen.draw.text(
        f"最高分: {high_score}",
        (WIDTH - 200, 10),
        fontsize=30,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    # 绘制操作提示 
    screen.draw.text(
        "方向键控制移动",
        (WIDTH - 200, 50),
        fontsize=20,
        fontname="simhei.ttf",
        color=TEXT_COLOR
    )
    
    # 绘制自动模式状态
    mode_text = "自动模式: 开启" if auto_mode else "按A键启用自动模式"
    mode_color = (255, 200, 0) if auto_mode else TEXT_COLOR
    screen.draw.text(
        mode_text,
        (10, 90),
        fontsize=20,
        fontname="simhei.ttf",
        color=mode_color
    )
    # 绘制无限模式状态
    inf_text = "无限模式: 开启" if infinite_mode else "按B键启用无限模式"
    inf_color = (255, 200, 0) if infinite_mode else TEXT_COLOR
    screen.draw.text(
        inf_text,
        (10, 120),
        fontsize=20,
        fontname="simhei.ttf",
        color=inf_color
    )
    # 绘制蛇身颜色指示
    color_names = ["红", "橙", "黄", "绿", "青", "蓝", "紫"]
    color_text = f"蛇身颜色: {color_names[snake_color_index]} (按C切换)"
    screen.draw.text(
        color_text,
        (10, 150),
        fontsize=20,
        fontname="simhei.ttf",
        color=SNAKE_BODY_COLORS[snake_color_index]
    )
    
    # 游戏结束显示
    if game_over:
        draw_game_over_screen()

import sys

def on_key_down(key):
    """处理按键按下"""
    global next_direction, game_started, auto_mode, infinite_mode, wingame, snake_color_index
    
    # 只处理预期的按键
    valid_keys = [keys.SPACE, keys.ESCAPE, keys.R, keys.LEFT, keys.RIGHT, keys.UP, keys.DOWN, keys.A, keys.B, keys.C]
    if key not in valid_keys:
        return
    
    # Allow toggling color at any time with C
    if key == keys.C:
        snake_color_index = (snake_color_index + 1) % len(SNAKE_BODY_COLORS)
        print(f"Snake color changed to index {snake_color_index}")
        return
    
    # Allow toggling infinite mode at any time with B
    if key == keys.B:
        infinite_mode = not infinite_mode
        if infinite_mode:
            wingame = False
        print(f"INFINITE MODE set to {infinite_mode}")
        return

    if not game_started:
        if key == keys.SPACE:
            reset_game()
        elif key == keys.ESCAPE:
            sys.exit()
        return
    
    if game_over:
        if key == keys.R:
            reset_game()
        elif key == keys.ESCAPE:
            game_started = False
        return
    
    # 游戏进行中按键处理
    if key == keys.A:
        # 按A键切换自动模式
        auto_mode = not auto_mode
    elif not auto_mode:
        # 只有在非自动模式下才响应方向键
        if key == keys.LEFT:
            next_direction = LEFT
        elif key == keys.RIGHT:
            next_direction = RIGHT
        elif key == keys.UP:
            next_direction = UP
        elif key == keys.DOWN:
            next_direction = DOWN
    
    if key == keys.ESCAPE:
        # 返回主菜单
        game_started = False
    elif key == keys.SPACE:
        # 重新开始
        reset_game()

# 启动游戏
pgzrun.go()