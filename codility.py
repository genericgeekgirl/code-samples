import collections
import copy

class Solution(object):
    def __init__(self):
        self.items = collections.deque()
        self.transactions = []

    def push(self,value):
        self.items.appendleft(value)

    def top(self):
        if not self.items:
            return 0
        return self.items[0]

    def pop(self):
        if self.items:
            self.items.popleft()

    def begin(self):
        self.transactions.append(copy.copy(self.items))

    def rollback(self):
	if self.transactions:
            self.items = self.transactions.pop()
            return True
        return False

    def commit(self):
        if self.transactions:
            self.transactions.pop()
            return True
        return False


def test():
    # Define your tests here
    sol = Solution()
    sol.push(42)
    assert sol.top() == 42, "top() should be 42"