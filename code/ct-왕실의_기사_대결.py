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

knights_hp = [knight[-1] for knight in knights]

def count_wall_and_bombs(knight_id, y2move, x2move):
    # 테두리에 벽을 두른 board라, 따로 좌표 처리 할 필요 없이 좌측상단이 (1,1)
    r, c, h, w, _ = knights[knight_id-1]
    has_wall = False
    bomb_num = 0
    if x2move == 0: # 위아래 움직임
        vertical_point = r-1 if y2move == -1 else r+h+1
        for i in range(c, c+w+1):
            # 벽이 있으면
            if new_board[vertical_point][i] == '2':
                return True, None
            # 지뢰가 있으면
            if new_board[vertical_point][i] == '1':
                bomb_num += 1
    else: # 좌우 움직임
        horizontal_point = c-1 if x2move == -1 else c+w+1
        for i in range(r, r+h+1):
            # 벽이 있으면
            if new_board[i][horizontal_point] == '2':
                return True, None
            # 지뢰가 있으면
            if new_board[i][horizontal_point] == '1':
                bomb_num += 1

    return has_wall, bomb_num

def find_knights(knight_id, y2move, x2move):
    r, c, h, w, _ = knights[knight_id-1]
    knights_found = defaultdict(int)
    if x2move == 0: # 상하 이면
        vertical_point = r-1 if y2move == -1 else r+h+1
        for i in range(c, c+w+1):
            knights_found[knight_board[vertical_point][i]] += 1

    elif y2move == 0: # 좌우 이면
        horizontal_point = c-1 if x2move == -1 else c+w+1
        for i in range(r, r+h+1):
            knights_found[knight_board[i][horizontal_point]] += 1

    return list(knights_found.keys())

answer = 0
#상우하좌
ydir, xdir = [-1, 0, 1, 0], [0, 1, 0, -1]
for _ in range(Q):
    ordered_k_id, dir_id = list(map(int, input().split()))
    dy, dx = ydir[dir_id], xdir[dir_id]

    # 기사 이동
    Q = deque([ordered_k_id])
    while Q:
        k_id = Q.popleft()
        # 벽과 지뢰 찾기
        has_wall, bomb_nums = count_wall_and_bombs(k_id, dy, dx)
        ## 벽이 있으면, 다음 지시 수행
        if has_wall:
            break
        # 밀린 기사 처리
        ## 밀린 기사 들을 Q에 append
        knights_found = find_knights(k_id, dy, dx)
        for knight_found in knights_found:
            if knight_found == 0:
                continue
            Q.append(knight_found)
        ## hp 및 위치 처리
        ### 첫 기사면
        if k_id == ordered_k_id:
            continue
        r, c, h, w, k = knights[k_id - 1]
        k -= bomb_nums
        if k < 0:
            # eliminate
            eliminated_knight = knights.pop(k_id - 1)
            print('eliminate')
        print('hi')


