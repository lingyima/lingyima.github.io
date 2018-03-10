class Queue(object):
    """
    队列
    """

    def __init__(self):
        self.__items = []

    def enquue(self, item):
        """
        入队/入列
        :param item:
        :return:
        """
        self.__items.append(item)

    def dequeue(self, item):
        """
        出队/出列
        :param item:
        :return:
        """
        return self.pop(0)

    def is_empty(self):
        """
        是否为空
        :return:
        """
        return self.__items == []

    def size(self):
        """
        队列长度
        :return:
        """
        return len(self.__items)

if __name__ == '__main__':
    q = Queue()
