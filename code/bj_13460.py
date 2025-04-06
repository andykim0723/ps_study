from collections import deque
import sys

sys.path.append('..')
sys.stdin = open("data/bj_13460.txt")
input = sys.stdin.readline

N, M = list(map(int, input().split()))
board = []
for _ in range(N):
    board.append(list(input().rstrip()))

visited = []
ydir, xdir = [1, -1, 0, 0], [0, 0, -1, 1]
totalcnt = 0

def get_pos(tgt):
    for tmpy in range(N):
        for tmpx in range(M):
            if board[tmpy][tmpx] == tgt:
                return tmpy, tmpx

def move(y, x, y2move, x2move):
    # cnt = 0
    # while True:
    #     if oor(y+y2move, x+x2move):
    #         break
    #     if board[y+y2move][x+x2move] == '#' and board[y][x] == 'O':
    #         break
    #     y+=y2move
    #     x+=x2move
    #     cnt+=1
    #
    # return y, x, cnt
    cnt = 0
    # 이동하는 위치가 벽이아니고, 구멍에 들어가지 않을 동안 반복
    while board[y + y2move][x + x2move] != "#" and board[y][x] != "O":
        x += x2move
        y += y2move
        cnt +=1
    return y, x, cnt

def oor(y, x):
    if 0 <= y < N and 0 <= x < M:
        return False
    else:
        return True

result = -1
# 상하좌우

Ry, Rx = get_pos('R')
By, Bx = get_pos('B')

Q = deque([(Ry, Rx, By, Bx, 0)])
visited.append((Ry, Rx, By, Bx))

while Q:
    Ry, Rx, By, Bx, totalcnt = Q.popleft()

    if totalcnt > 10:
        break
    for i in range(4):
        # move
        Ry, Rx, Rcnt = move(Ry, Rx, ydir[i], xdir[i])
        By, Bx, Bcnt = move(By, Bx, ydir[i], xdir[i])

        if board[By][Bx] == 'O':
            continue
        if board[Ry][Rx] == 'O':
            result = totalcnt
            Q.clear()
            break

        # if same pos, move the less moved one
        if Ry == By and Rx == Bx:
            if Rcnt > Bcnt:
                Ry-=ydir[i]
                Rx-=xdir[i]
            else:
                By-=ydir[i]
                Bx-=xdir[i]


        if (Ry, Rx, By, Bx) not in visited:
            visited.append((Ry, Rx, By, Bx))
            Q.append((Ry, Rx, By, Bx, totalcnt+1))

print(result)

