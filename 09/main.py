import re

class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next
    def insert_after(self, value):
        x = Node(value, prev=self, next=self.next)
        self.next.prev = x
        self.next = x
        return x
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev

def winning_score(num_players, last_marble):
    players = [0]*num_players
    cur = Node(0)
    cur.prev = cur
    cur.next = cur
    x = 1
    while x < last_marble:
        if x % 23 == 0:
            p = x%len(players)
            players[p] += x
            for _ in range(7):
                cur = cur.prev
            players[p] += cur.value
            cur.remove()
            cur = cur.next
        else:
            cur = cur.next.insert_after(x)
        x += 1
    return max(players)

with open("input") as file:
    num_players, last_marble = map(int, re.findall("\d+", file.read()))

print(winning_score(num_players, last_marble))
print(winning_score(num_players, last_marble*100))