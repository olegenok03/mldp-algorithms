class MyQueue:
    def __init__(self) -> None:
        self.stack1 = []
        self.stack2 = []

    def push(self, x: int) -> None:
        self.stack1.append(x)

    def pop(self) -> int:
        if len(self.stack2) == 0:
            while len(self.stack1) != 0:
                elem = self.stack1.pop()
                self.stack2.append(elem)
        return self.stack2.pop()

    def peek(self) -> int:
        if len(self.stack2) == 0:
            while len(self.stack1) != 0:
                elem = self.stack1.pop()
                self.stack2.append(elem)
        return self.stack2[-1]

    def empty(self) -> bool:
        return len(self.stack1) == 0 and len(self.stack2) == 0
