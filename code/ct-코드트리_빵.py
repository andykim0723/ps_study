# heapq로 런타임에러 해결!

import sys
sys.stdin = open('data/ct-코드트리_빵.txt')

import heapq
from collections import deque

n, m = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(n)]
stores = [list(map(int, input().split())) for _ in range(m)]
stores = [(store[0]-1, store[1]-1) for store in stores]

base_camps = []
for i in range(n):
    for j in range(n):
        if board[i][j]:
            base_camps.append((i, j))

p_locs = [(-1, -1) for _ in range(m)]
cnt_go = [[False] * n for _ in range(n)]

dones = []
#상좌우하
ydir, xdir = [-1, 0, 0, 1], [0, -1, 1, 0]

def oor(y, x):
    if 0 <= y < n and 0 <= x < n:
        return False
    else:
        return True

def calc_min_dist(src, tgt):
    visited = []
    Q = deque([(src, 0)])
    while Q:
        cur_pos, cur_cnt = Q.popleft()
        if cur_pos == tgt:
            return cur_cnt
        for i in range(4):
            # 인접한 칸 중 갈 수 있는 칸 선정
            ## 격자 밖이 경우
            if oor(cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]):
                continue
            ## 지나 갈 수 없는 경우 (베이스캠프 출발, 편의점 도착)
            if cnt_go[cur_pos[0] + ydir[i]][cur_pos[1] + xdir[i]]:
                continue
            # cur_pos = (cur_pos[0] + ydir[i], cur_pos[1] + xdir[i])
            if (cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]) not in visited:
                Q.append(((cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]), cur_cnt + 1))
                visited.append((cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]))
    return n * n + 1

def action1():
    """격자에 있는 사람들은 목적지로 최단거리 1칸이동.(최단거리가 같으면 상좌우하 순으로 결정)"""
    # 각 사람위치마다 행동 수행
    for p_idx, p_loc in enumerate(p_locs):
        # 격자에 없으면 스킵
        if p_loc[0] == -1:
            continue
        else:
            # 각 사람의 최단 거리 계산
            ## 상좌우하 순으로 최단 거리 계산
            p_loc_min_dist, nxt_state = n * n + 1, None
            for i in range(4):
                # 인접한 칸 중 갈 수 있는 칸 선정
                ## 격자 밖이 경우
                if oor(p_loc[0] + ydir[i], p_loc[1] + xdir[i]):
                    continue
                ## 지나 갈 수 없는 경우 (베이스캠프 출발, 편의점 도착)
                if cnt_go[p_loc[0] + ydir[i]][p_loc[1] + xdir[i]]:
                    continue
                ## 최단 거리 선정
                min_dist = calc_min_dist((p_loc[0] + ydir[i], p_loc[1] + xdir[i]), stores[p_idx])
                ## 상좌우하 순이여서, 같은 거리면 알아서 우선순위가 알아서 결정됨

                if min_dist < p_loc_min_dist:
                    p_loc_min_dist = min_dist
                    nxt_state = (p_loc[0] + ydir[i], p_loc[1] + xdir[i])

            # 이동
            p_locs[p_idx] = nxt_state

def action2():
    """사람들이 편의점에 도착하면 해당 칸은 지나 갈 수 없음."""
    # 각 편의점마다 사람있는지 체크, 있으면 cnt_go 처리
    for store_idx, store in enumerate(stores):
        # 사람의 편의점에 도착했으면
        if p_locs[store_idx] == store:
            dones.append(store_idx)
            p_locs[store_idx] = (-1, -1)
            cnt_go[store[0]][store[1]] = True

def action3(t):
    """t시간에 t번째 사람은 목적 편의점과 최단거리 베이스 캠프에 들어감.(최단거리가 같으면 행이 작은 캠프, 열이 작은 캠프 순으로 결정). 이제 해당 베이스 캠프는 지나 수 없음"""
    # t번째 편의점과 베이스 캠프간의 최단거리 계산(행열 우선순위까지 처리)
    # find base camps

    visited = []
    camp_min_dist = n * n + 1
    close_base_camps = []
    tgt_base_camp = None
    store_Q = deque([(stores[cur_t], 0)])
    visited.append(stores[cur_t])
    while store_Q:
        cur_pos, cur_cnt = store_Q.popleft()
        # 최단거리보다 많이 가면 스킵
        if cur_cnt > camp_min_dist:
            continue
        for i in range(4):
            ## 격자 밖안 경우
            if oor(cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]):
                continue
            ## 지나 갈 수 없는 경우(베이스캠프 출발, 편의점 도착)
            if cnt_go[cur_pos[0] + ydir[i]][cur_pos[1] + xdir[i]]:
                continue
            # 베이스캠프면 결과 입력
            if board[cur_pos[0] + ydir[i]][cur_pos[1] + xdir[i]] == 1 and cur_cnt+1 <= camp_min_dist:
                # close_base_camps.append((cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]))
                heapq.heappush(close_base_camps, (cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]))
                camp_min_dist = cur_cnt + 1

            if (cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]) not in visited:
                visited.append((cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]))
                store_Q.append(([cur_pos[0] + ydir[i], cur_pos[1] + xdir[i]], cur_cnt+1))

    # 베이스캠프 우선순위 처리
    tgt_base_camp = close_base_camps[0]
    # if len(close_base_camps) > 1:
    #     for bc in close_base_camps[1:]:
    #         if bc[0] < tgt_base_camp[0]:
    #             tgt_base_camp = bc
    #         elif bc[1] < tgt_base_camp[1]:
    #             tgt_base_camp = bc
    p_locs[t] = tgt_base_camp
    cnt_go[tgt_base_camp[0]][tgt_base_camp[1]] = True

cur_t = 0
while True:
    if len(dones) >= m:
        break
    if cur_t > n * n + 1:
        break
    action1()
    action2()
    if cur_t < m:
        action3(cur_t)

    cur_t+=1

print(cur_t)
