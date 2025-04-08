import sys
sys.stdin = open('data/ct-고대_문명_유적_탐사.txt')

import heapq
import copy
from collections import deque

K, M = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(5)]
nums_in_wall = list(map(int, input().split()))
ydir, xdir = [-1, 1, 0, 0], [0, 0, -1, 1]


# 탐사 진행
## 유물이 최대화 되는 방식으로 회전
## 동률 시, 가장 회전 각도가 작은 방식 선택
## 동률 시, 회전 중심 좌표의 숫자가 가장 작은 경우

# 유물 획득
## 같은 숫자가 3개 이상일 경우, 유물로 변해서 보드에서 사라짐
## 빈 칸들을 벽에 있는 숫자들을 순서대로 채워야 함.
## 열 번호가 "작은" 순서, 행 번호가 "큰" 순서대로 채움.

def oor(tmp_y, tmp_x):
    if 0 <= tmp_y < 5 and 0 <= tmp_x < 5:
        return False
    else:
        return True

def rotate_90(sy, sx, length, tmp_board, new_arr):
    for y in range(sy, sy + length):
        for x in range(sx, sx + length):
            oy, ox = y - sy, x - sx
            ry, rx = ox, length - oy - 1
            new_arr[sy + ry][sx + rx] = tmp_board[y][x]

    for y in range(sy, sy + length):
        for x in range(sx, sx + length):
            tmp_board[y][x] = new_arr[y][x]

def find_treasures(tmp_board):
    treasures = []
    for i in range(5):
        for j in range(5):
            t_idx = tmp_board[i][j]
            found_treasures = [(i, j)]
            visited = [(i, j)]
            Q = deque([(i, j)])
            while Q:
                cur_y, cur_x = Q.pop()
                visited.append((cur_y, cur_x))
                for dir_idx in range(4):
                    if oor(cur_y+ydir[dir_idx], cur_x+xdir[dir_idx]):
                        continue
                    if (cur_y+ydir[dir_idx], cur_x+xdir[dir_idx]) not in visited and t_idx == tmp_board[cur_y+ydir[dir_idx]][cur_x+xdir[dir_idx]]:
                        if (cur_y+ydir[dir_idx], cur_x+xdir[dir_idx]) not in found_treasures:
                            found_treasures.append((cur_y+ydir[dir_idx], cur_x+xdir[dir_idx]))
                        Q.append((cur_y+ydir[dir_idx], cur_x+xdir[dir_idx]))

            if len(found_treasures) > 2:
                treasures.extend(found_treasures)

    return list(set(treasures))


wall_cnt = 0
answers = []

# 회전 방식 찾기
for _ in range(K):
    answer = 0
    rotation_results = []
    for i in range(3):
        for j in range(3):
            tmp_board = copy.deepcopy(board)
            for k in range(3):
                new_arr = [[0] * 5 for _ in range(5)]
                rotate_90(i, j, 3, tmp_board, new_arr)
                treasures = find_treasures(tmp_board)
                # 유뮬갯수, 회전수, 중심 열, 중심 행
                heapq.heappush(rotation_results, (-(len(treasures)+1), k, j, i))

    rot_info = rotation_results[0]
    # 탐사 과정 중 유물을 차지 못하면 중단
    if rot_info[0] == -1:
        break
    # 회전 진행
    new_arr = [[0] * 5 for _ in range(5)]
    rotate_90(rot_info[3], rot_info[2], 3, board, new_arr)

    # 유물 갯수 찾기
    while True:
        treasures = find_treasures(board)
        # 광석이 없을때까지 진행
        if len(treasures) == 0:
            break
        # 새로운 광석 넣는 작업: 없애고 집어넣고
        new_treasures = []
        # 우선순위 설정
        for y,x in treasures:
                heapq.heappush(new_treasures, (x+1, -(y+1)))
        while new_treasures:
            x, y = heapq.heappop(new_treasures)
            board[y*-1-1][x-1] = nums_in_wall[wall_cnt]
            wall_cnt += 1
        answer += len(treasures)

    if answer:
        answers.append(str(answer))


answers = ' '.join(answers)
print(answers)

