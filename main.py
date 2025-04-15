import pygame
import math

# Инициализация Pygame
pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Тор с Pygame")

# видимость
f = width / 2
center_x, center_y = width / 2, height / 2
scale = 100

pos_x, pos_y, pos_z = 0, 0, 200
rot_x, rot_y = 0, 0

# функция тора
def x_func(u, v, a, b):
    return (a + b * math.cos(v)) * math.cos(u)

def y_func(u, v, a, b):
    return (a + b * math.cos(v)) * math.sin(u)

def z_func(v, b):
    return b * math.sin(v)

# вращения
def rotate_point(x, y, z, rot_x, rot_y):
    # вокруг оси X
    y_rot_x = y * math.cos(rot_x) - z * math.sin(rot_x)
    z_rot_x = y * math.sin(rot_x) + z * math.cos(rot_x)
    y, z = y_rot_x, z_rot_x
    # вокруг оси Y
    x_rot_y = x * math.cos(rot_y) - z * math.sin(rot_y)
    z_rot_y = x * math.sin(rot_y) + z * math.cos(rot_y)
    return x_rot_y, y, z_rot_y

def proj_point(x, y, z):
    if z > 0:
        x2d = (f * x) / z + center_x
        y2d = (f * y) / z + center_y
        return x2d, y2d
    return None

# параметры тора
a, b = 3, 1 
# a, b = 3, 3
# a, b = 3, 4
# a, b = 3, 5
u_min, u_max = 0, 2 * math.pi
v_min, v_max = 0, 2 * math.pi
u_step, v_step = 0.2, 0.2

running = True
clock = pygame.time.Clock()


# Сам цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    move_speed = 5
    rot_speed = 0.05
    if keys[pygame.K_w]: pos_z -= move_speed  
    if keys[pygame.K_s]: pos_z += move_speed  
    if keys[pygame.K_a]: pos_x += move_speed  
    if keys[pygame.K_d]: pos_x -= move_speed  
    if keys[pygame.K_q]: rot_y += rot_speed   
    if keys[pygame.K_e]: rot_y -= rot_speed   
    if keys[pygame.K_UP]: pos_y -= move_speed 
    if keys[pygame.K_DOWN]: pos_y += move_speed 
    if keys[pygame.K_LEFT]: rot_x += rot_speed
    if keys[pygame.K_RIGHT]: rot_x -= rot_speed

    screen.fill((255, 255, 255))  # Белый фон

    # Каркас из точек
    nu = int((u_max - u_min) / u_step) + 1
    nv = int((v_max - v_min) / v_step) + 1
    grid_3d = [[(x_func(u_min + i * u_step, v_min + j * v_step, a, b) * scale,
                 y_func(u_min + i * u_step, v_min + j * v_step, a, b) * scale,
                 z_func(v_min + j * v_step, b) * scale)
                for j in range(nv)] for i in range(nu)]

    # вращения и смещения тора
    grid_3d_transformed = []
    for i in range(nu):
        row = []
        for j in range(nv):
            x, y, z = grid_3d[i][j]
            x, y, z = rotate_point(x, y, z, rot_x, rot_y)  # Вращение
            x += pos_x
            y += pos_y
            z += pos_z  # Смещение
            row.append((x, y, z))
        grid_3d_transformed.append(row)

    # Отрисовка тора 
    for i in range(nu):
        for j in range(nv):
            # Линии u
            p1 = grid_3d_transformed[i][j]
            p2 = grid_3d_transformed[(i + 1) % nu][j]
            if p1[2] > 0 and p2[2] > 0:
                x1 = (f * p1[0]) / p1[2] + center_x
                y1 = (f * p1[1]) / p1[2] + center_y
                x2 = (f * p2[0]) / p2[2] + center_x
                y2 = (f * p2[1]) / p2[2] + center_y
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 1)

            # Линии v
            p1 = grid_3d_transformed[i][j]
            p2 = grid_3d_transformed[i][(j + 1) % nv]
            if p1[2] > 0 and p2[2] > 0:
                x1 = (f * p1[0]) / p1[2] + center_x
                y1 = (f * p1[1]) / p1[2] + center_y
                x2 = (f * p2[0]) / p2[2] + center_x
                y2 = (f * p2[1]) / p2[2] + center_y
                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 1)

    # Отрисовка осей координат
    length = 1000  # 
    origin = (0, 0, 0) 
    axes = [
        ((length, 0, 0), (255, 0, 0)),
        ((0, length, 0), (0, 255, 0)),
        ((0, 0, length), (0, 0, 255))
    ]

    # Трансформация и проецирование осей
    for axis_end, color in axes:
        # Начало и конец оси
        x0, y0, z0 = origin
        x1, y1, z1 = axis_end

        x0, y0, z0 = rotate_point(x0, y0, z0, rot_x, rot_y)
        x0 += pos_x
        y0 += pos_y
        z0 += pos_z
        x1, y1, z1 = rotate_point(x1, y1, z1, rot_x, rot_y)
        x1 += pos_x
        y1 += pos_y
        z1 += pos_z

        proj0 = proj_point(x0, y0, z0)
        proj1 = proj_point(x1, y1, z1)

        if proj0 and proj1:
            pygame.draw.line(screen, color, proj0, proj1, 2)  # Толщина линий 2 пикселя
            pygame.draw.circle(screen, (0, 0, 0), (int(proj0[0]), int(proj0[1])), 3)  # Точка в начале координат

    pygame.display.flip()
    clock.tick(60)

pygame.quit()