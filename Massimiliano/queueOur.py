class QueueOur:

    elements = []
    index = 0

    def push(self, other):
        self.elements.append(other)

    def pop(self):
        element = self.elements[self.index]
        self.index = self.index + 1
        return element