import sys
sys.stdin = open('data/ct-왕실의_기사_대결.txt')

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
# 2. 기사들만의 보드 따로 하나 추가
# 기사 이동(bfs)
# 1. 명령 받은 기사 이동
# 2. 이동한 줄에 다른 기사 정보, 벽, 폭탄 확인
# 3. 벽이 있으면 break,
# 4. 벽이 없으면 폭탄으로 데미지 주기.
# 5. 데미지 처리

# board with wall
new_board = []
new_board.append([2]*(L+2))
for i in range(L):
    tmp = [2] + board[i] + [2]
    new_board.append(tmp)
new_board.append([2] * (L + 2))

# board with knight positions
knight_board = [[0] * L for _ in range(L)]
for knight_id, knight_info in enumerate(knights):
    r, c, h, w, _ = knight_info
    r, c = r-1, c-1
    for i in range(r, r+h):
        for j in range(c, c+w):
            knight_board[i][j] = knight_id + 1

knights_hp = [knight[-1] for knight in knights]

def count_bomb():
    pass

def has_knights(knight_id, y2move, x2move):
    r, c, h, w, _ = knights[knight_id-1]
    knights = set()
    if x2move == 0: # 상하 이면
        v_point = r-1 if y2move == -1 else r+h
        for i in range(v_point, v_point+w):
            if knight_board[v_point][i] != 0
    elif y2move == 0: # 좌우 이면



#상우하좌
ydir, xdir = [-1, 0, 1, 0], [0, 1, 0, -1]
for _ in range(Q):
    k_id, dir_id = list(map(int, input().split()))
    dy, dx = ydir[dir_id], xdir[dir_id]
    # 왕의 명령대로 움직임.
    # if has_wall(k_id, dy, dx):
    #     continue
    if has_knights(k_id, dy, dx):
        # print(do everything!)


