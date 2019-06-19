
class Model3:
    def __init__(self):
        self.i = 0
        self.seed = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ]

    def __iter__(self):
        return self

    def next(self):
        if self.i >= len(self.seed):
            raise StopIteration()

        n = self.seed[self.i]
        self.i += 1
        return n


m = Model3()


def analyze(frame):
    return m.next()
