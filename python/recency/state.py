"""Exact relative-recency state (section 6 contract).

rho(P): list of distinct seen keys, most-recently-accessed first.
Unseen keys are the complement in [n] (tied below all seen keys).
No absolute timestamps are retained.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def empty_rho() -> tuple:
    return ()


def update_rho(rho: tuple, x: int) -> tuple:
    # Remove x if present, prepend x. Preserves strict last-access order.
    if x in rho:
        rho = tuple(k for k in rho if k != x)
    return (x,) + rho


def unseen_keys(rho: tuple, n: int) -> tuple:
    seen = set(rho)
    return tuple(k for k in range(1, n + 1) if k not in seen)


def replay_order(history: list[int]) -> tuple:
    # Relative last-access order reconstructed from a key history.
    rho: tuple = ()
    for x in history:
        rho = update_rho(rho, x)
    return rho


def check_relative_order(rho: tuple, history: list[int]) -> bool:
    # True iff rho encodes the relative last-access order of history.
    last: dict = {}
    for i, x in enumerate(history):
        last[x] = i
    seen = sorted(last, key=lambda k: -last[k])
    return tuple(seen) == rho


def keep_successor(state: tuple, x: int, splay_after_A: int, splay_after_B: int) -> tuple:
    # state = (A, B, rho_X, rho_Y); KEEP updates both streams.
    A, B, rho_X, rho_Y = state
    return (splay_after_A, splay_after_B, update_rho(rho_X, x), update_rho(rho_Y, x))


def delete_successor(state: tuple, x: int, splay_after_A: int) -> tuple:
    # DELETE updates rho_X only; B and rho_Y unchanged.
    A, B, rho_X, rho_Y = state
    return (splay_after_A, B, update_rho(rho_X, x), rho_Y)


def initial_state(T: int) -> tuple:
    return (T, T, (), ())


def relabel(state: tuple, n: int, perm: dict) -> tuple:
    # Order-preserving relabeling support: apply key bijection to trees + recency.
    A, B, rho_X, rho_Y = state
    return (A, B, tuple(perm[k] for k in rho_X), tuple(perm[k] for k in rho_Y))
