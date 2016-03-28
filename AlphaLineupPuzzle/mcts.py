# coding: utf-8


def search(gs, deep):
    optimal_move = None
    max_score = gs.score

    if deep == 0:
        return optimal_move, max_score

    for idx, pos in gs.legal_moves():
        _gs = gs.copy()
        _gs.move(idx, pos)
        count = 0
        sum_score = 0
        for _gs in _gs.ext(idx):
            count += 1
            _, score = search(_gs, deep - 1)
            sum_score += score
        avg_score = float(sum_score) / count
        if avg_score >= max_score:
            max_score = avg_score
            optimal_move = (idx, pos)

    return optimal_move, max_score
