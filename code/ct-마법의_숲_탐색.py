import sys
sys.stdin = open('data/ct-마법의_숲_탐색.txt')

import heapq
from collections import deque

def rotate_exit(chulgu, direction):
    if direction == 'left':
        if chulgu == 0:
            return 3
        return chulgu-1
    elif direction == 'right':
        if chulgu == 3:
            return 0
        return chulgu+1

fixed_stones = {}
R, C, K = list(map(int, input().split()))
board = [[0]*C for _ in range(R)]

answer = 0
# 상우하좌
ydir, xdir = [-1, 0, 1, 0], [0, 1, 0, -1]
for _ in range(K):
    # 스폰된 행 번호, 출구 위치
    c, d = list(map(int, input().split()))

    cur_y, cur_x = 0, c-1
    while True:
        # print(cur_y, cur_x)
        if cur_y+2 >= R:
            break
        if board[cur_y+2][cur_x] == 0 and board[cur_y+1][cur_x-1] == 0 and board[cur_y+1][cur_x+1] == 0:
            cur_y+=1
            continue

        if cur_x-2 > 0:
            if board[cur_y][cur_x-2] == 0 and board[cur_y+1][cur_x-1] == 0 and board[cur_y-1][cur_x-1] == 0 and board[cur_y+1][cur_x-2] == 0 and board[cur_y+2][cur_x-1] == 0:
                cur_y+=1
                cur_x-=1
                d = rotate_exit(d, 'left')
                continue
        if cur_x+2 < C:
            if board[cur_y][cur_x+2] == 0 and board[cur_y+1][cur_x+1] == 0 and board[cur_y-1][cur_x+1] == 0 and board[cur_y+2][cur_x+1] == 0 and board[cur_y+1][cur_x+2] == 0:
                cur_y+=1
                cur_x+=1
                d = rotate_exit(d, 'right')
                continue
        break
    # 밖에 나와있으면, empty
    if cur_y-1 < 0 or cur_x-1 < 0 or cur_x+1 > C-1:
        del board
        del fixed_stones
        board = [[0] * C for _ in range(R)]
        fixed_stones = {}
    # 안에있으면
    else:
        cnt = len(fixed_stones)
        fixed_stones[cnt+1] = (cur_y, cur_x, d)
        board[cur_y][cur_x] = cnt+1
        for i in range(4):
            board[cur_y+ydir[i]][cur_x+xdir[i]] = cnt+1

        bottoms = [(-cur_y, cur_x, d)]
        visited = [cnt+1]
        Q = deque([(cur_y, cur_x, d)])
        while Q:
            cur_y, cur_x, d = Q.popleft()
            exit_y, exit_x = cur_y+ydir[d], cur_x+xdir[d]
            for i in range(4):
                if 0 <= exit_y+ydir[i] < R and 0 <= exit_x+xdir[i] < C:
                    if board[exit_y+ydir[i]][exit_x+xdir[i]] != 0 and board[exit_y+ydir[i]][exit_x+xdir[i]] not in visited:
                        tmp_y, tmp_x, tmp_d = fixed_stones[board[exit_y + ydir[i]][exit_x + xdir[i]]]
                        Q.append((tmp_y, tmp_x, tmp_d))
                        heapq.heappush(bottoms, (-tmp_y, tmp_x, tmp_d))
                        visited.append(board[exit_y + ydir[i]][exit_x + xdir[i]])

        answer -= (bottoms[0][0]-2)

#0123 북동남서
print(answer)

# print(board)
# 0123
# 상우하좌

# 1. 남쪽으로 이동
# 2. 안되면 좌로 이동
# 3. 안되면 우로 이동
# 4. 셋다 안되면 정지
# 5. 정지헀는데 밖에 있으면, empty 숲
# 6. 맨 마지막 행 계산
##