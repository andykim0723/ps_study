import sys
sys.stdin = open('data/ct-미지의_공간_탈출.txt')

N, M, F = list(map(int, input().split()))
uk_board = [list(map(int, input().split())) for _ in range(N)]

time_wall = []
for _ in range(5):
    tmp_board = []
    for _ in range(M):
        tmp_row = [list(map(int, input().split()))]
        tmp_board.append(tmp_row)
    time_wall.append(tmp_board)
ghosts = [list(map(int, input().split()))+[0] for _ in range(F)]

# 시간의벽 좌표 구하기
def find_tw_lt():
    for i in range(N):
        for j in range(N):
            if uk_board[i][j] == 3:
                return i, j
tw_lt = find_tw_lt()
# 초기 이상 현상 처리
for g in ghosts:
    uk_board[g[0]][g[1]] = 5

# 0123
# 동서남북
ydir, xdir = [0, 0, -1, 1], [1, -1, 0, 0]
def move_ghost(cur_turn):
    for g_idx in range(len(ghost)):
        r, c, d, v, status = ghost[g_idx]
        # 차례가 아니거나, 이미 끝났으면
        if cur_turn % v != 0 or status == -2:
            continue
        # 미지의 세계에 있으면
        if status == 0:
            pass
        # 시간의 벽에 있으면
        if status == 1:
            pass


max_turn = N * N + M * M * 5
cur_turn = 0
for cur_turn in range(1, max_turn):
    # ghost 이동
    move_ghost(cur_turn)


# 탈출 bfs



#       0 0 0
#       0 0 0
#       0 0 0
# 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0
#       0 0 0
#       0 0 0
#       0 0 0
#
# # 좌상
# 0, 0 -> 0, 0
# 0, 1 -> 1, 0
# 0, 2 -> 2, 2
#
# # 우상
# 0, 0 -> 2, 2
# 0, 1 -> 1, 2
# 0, 2 -> 0, 2
#
# # 좌하
# 2, 2 -> 0, 0
# 1, 2 -> 1, 0
# 0, 2 -> 2, 0
#
# # 우하
# 2, 0 -> 0, 2
# 2, 1 -> 1, 2
# 2, 2 -> 2, 2