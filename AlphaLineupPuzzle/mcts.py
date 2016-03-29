# coding: utf-8


def select(gs, deep):
    optimal_move = None
    max_score = gs.score

    for idx, pos in gs.legal_moves():
        _gs = gs.copy()
        _gs.move(idx, pos)
        score = ext(_gs, idx, deep - 1)
        if score >= max_score:
            max_score = score
            optimal_move = (idx, pos)

    return optimal_move, max_score


def ext(gs, idx, deep):
    if deep == 0:
        return gs.score

    count = 0
    sum_score = 0
    for _gs in gs.ext(idx):     # 扩展
        count += 1
        _, score = select(_gs, deep)
        sum_score += score
    avg_score = float(sum_score) / count
    return avg_score

search = select
