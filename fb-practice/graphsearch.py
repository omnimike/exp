import pytest
import sys
from collections import deque

def search(graph, val, q, visited):
    node = q.pop()
    if node == val:
        return True
    for sibling in graph[node]:
        if not visited[sibling]:
            q.appendleft(sibling)
            visited[sibling] = True
    return False

def path_exists(graph, a, b):
    a_queue = deque([a])
    b_queue = deque([b])
    a_visited = [False for i in range(len(graph))]
    b_visited = [False for i in range(len(graph))]
    while len(a_queue) > 0 and len(b_queue) > 0:
        if search(graph, b, a_queue, a_visited):
            return True
        if search(graph, a, b_queue, b_visited):
            return True
    while len(a_queue) > 0:
        if search(graph, b, a_queue, a_visited):
            return True
    while len(b_queue) > 0:
        if search(graph, a, b_queue, b_visited):
            return True
    return False


def test_nodes_equal():
    graph = [[0], [1]]
    assert path_exists(graph, 0, 0) == True
    assert path_exists(graph, 1, 1) == True
    assert path_exists(graph, 0, 1) == False
    assert path_exists(graph, 1, 0) == False


def test_small_graph():
    graph = [[1], []]
    assert path_exists(graph, 0, 1) == True
    assert path_exists(graph, 1, 0) == True

def test_self_links():
    graph = [[0], [0]]
    assert path_exists(graph, 0, 0) == True
    assert path_exists(graph, 1, 1) == False

def test_loops():
    graph = [[1], [0], []]
    assert path_exists(graph, 0, 2) == False


if __name__ == '__main__':
    pytest.main(sys.argv)
