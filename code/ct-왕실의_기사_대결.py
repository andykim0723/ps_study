import sys
sys.stdin = open('data/ct-왕실의_기사_대결.txt')

from collections import deque, defaultdict

L, N, Q = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(L)]
knights = [list(map(int, input().split())) for _ in range(N)]


# 로직:
## 기사의 형태: (r, c)를 좌측 상단으로 하여 H, W의 직사각형 헝태, 체력 k
## 기사 이동: 상하좌우 중 한 칸 움직일 수 있음. 움직인 칸에 다른 기사가 있으면, 그 기사도 같이 밀려남
### 밀려난 기사 중 벽에 부딪힌 경우가 있는 경우 전부 무효
### 정상적으로 밀려난 기사들은 자신의 칸에 있는 지뢰 수 만큼 데미지를 받음.
### 명령을 받은 기사는 데미지를 받지 않음.
### 현재 체력 이상으로 데미지를 받는 경우 사라짐.

#### 생존한 기사들의 받은 데미지 양을 구하시오.

# 조건:
# 없는 기사에게 명령을 내리면 무효

# TODO:
# 1. 보드 바깥 테두리에 벽 추가 -> DONE
# 2. 기사들만의 보드 따로 하나 추가 -> DONE
# 기사 이동(bfs)
# 1. 명령 받은 기사 이동
# 2. 이동한 줄에 다른 기사 정보, 벽, 폭탄 확인
# 3. 벽이 있으면 break,
# 4. 벽이 없으면 폭탄으로 데미지 주기.
# 5. 데미지 처리

# 보드 바깥 테두리에 벽 추가
new_board = []
new_board.append([2]*(L+2))
for i in range(L):
    tmp = [2] + board[i] + [2]
    new_board.append(tmp)
new_board.append([2] * (L + 2))

# 기사들만의 보드
knight_board = [[0] * L for _ in range(L)]
for knight_id, knight_info in enumerate(knights):
    r, c, h, w, _ = knight_info
    r, c = r-1, c-1
    for i in range(r, r+h):
        for j in range(c, c+w):
            knight_board[i][j] = knight_id + 1

eliminated = set()
knights_hp = [knight[-1] for knight in knights]

def has_wall(knight_id, y2move, x2move):
    # 테두리에 벽을 두른 board라, 따로 좌표 처리 할 필요 없이 좌측상단이 (1,1)
    r, c, h, w, _ = knights[knight_id-1]
    if x2move == 0: # 위아래 움직임
        vertical_point = r-1 if y2move == -1 else r+h
        for i in range(c, c+w):
            # 벽이 있으면
            if new_board[vertical_point][i] == 2:
                return True

    else: # 좌우 움직임
        horizontal_point = c-1 if x2move == -1 else c+w
        for i in range(r, r+h):
            # 벽이 있으면
            if new_board[i][horizontal_point] == 2:
                return True

    return False

# def find_knights(knight_id, y2move, x2move):
#     r, c, h, w, _ = knights[knight_id-1]
#     r, c = r-1, c-1
#     knights_found = defaultdict(int)
#     if x2move == 0: # 상하 이면
#         vertical_point = r-1 if y2move == -1 else r+h
#         for i in range(c, c+w):
#             knights_found[knight_board[vertical_point][i]] += 1
#
#     elif y2move == 0: # 좌우 이면
#         horizontal_point = c-1 if x2move == -1 else c+w
#         for i in range(r, r+h):
#             knights_found[knight_board[i][horizontal_point]] += 1
#
#     return list(knights_found.keys())

def find_knights(knight_id, y2move, x2move):
    r, c, h, w, _ = knights[knight_id-1]
    if x2move == 0: # 상하 이면
        if y2move == 1:
            check_range = (c)
    knights_found = []
    for tmp_k_id, knight in enumerate(knights):
        if knight_id == tmp_k_id:
            continue
        tmp_r, tmp_c, tmp_h, tmp_w, _ = knight



answer = 0
#상우하좌
ydir, xdir = [-1, 0, 1, 0], [0, 1, 0, -1]
print(knights)
for _ in range(Q):
    ordered_k_id, dir_id = list(map(int, input().split()))
    # 사라진 기사에게 명령을 내리면 무효
    if ordered_k_id in eliminated:
        continue

    # 기사 이동
    dy, dx = ydir[dir_id], xdir[dir_id]
    Q = deque([ordered_k_id])
    moved_knight = deque([ordered_k_id])

    wall = False
    while Q:
        k_id = Q.popleft()
        ## 벽이 있으면, 다음 지시 수행
        if has_wall(k_id, dy, dx):
            wall = True
            break
        # 밀린 기사 들을 Q에 append
        knights_found = find_knights(k_id, dy, dx)

        for knight_found in knights_found:
            if knight_found == 0:
                continue
            Q.append(knight_found)
            moved_knight.append(knight_found)

    if wall:
        continue


    # 밀린 기사들을 움직이고, 지뢰계산하고, 피깎고, elimiate 시킴
    while moved_knight:
        k_id = moved_knight.pop()
        r, c, h, w, k = knights[k_id - 1]

        # 좌상단은 1,1로 시작하므로 0,0보드에 맞추기 위해 r,c변경
        r, c = r-1, c-1
        # knght board 처리: 앞으로 움직이고, 뒤에는 0으로
        if dx == 0:  # 상하 이면
            for i in range(c, c + w):
                if dy == -1: # 상이면
                    knight_board[r-1][i] = k_id
                    knight_board[r+h-1][i] = 0
                elif dy == 1: # 하이면
                    knight_board[r][i] = 0
                    knight_board[r+h][i] = k_id
        elif dy == 0:
            for i in range(r, r+h):
                if dx == -1: # 좌이면
                    knight_board[i][c-1] = k_id
                    knight_board[i][c+w-1] = 0
                elif dx == 1: # 우이면
                    knight_board[i][c] = 0
                    knight_board[i][c+w] = k_id

        # 좌상단 처리
        r, c = r + dy, c + dx

        # 지뢰 계산
        bomb_nums = 0
        for i in range(r, r + h):
            for j in range(c, c + w):
                if new_board[i+1][j+1] == 1:
                    bomb_nums += 1
        # hp 처리
        if k_id == ordered_k_id:
            continue
        k -= bomb_nums
        # 기사가 죽었으면
        if k <= 0:
            # eliminate
            eliminated.add(k_id)
            # knight board에서 없애기
            for i in range(r, r + h):
                for j in range(c, c + w):
                    knight_board[i][j] = 0
        else:
            knights[k_id-1] = [r+1, c+1, h, w, k]

answer = 0
for k_id, knight in enumerate(knights):
    if k_id in eliminated:
        continue
    damage = knights_hp[k_id]-knight[-1]
    answer += damage
print(answer)