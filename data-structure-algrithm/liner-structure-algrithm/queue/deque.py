class Deque(object):
    """
    双端队列
    """

    def __init__(self):
        self.__items = []

    def add_front(self, item):
        """
        头部入列元素
        :param item:
        :return:
        """
        self.__items.insert(0, item)

    def add_rear(self, item):
        """
        尾部入列元素
        :param item:
        :return:
        """
        self.__items.append(item)

    def pop_front(self, item):
        """
        头部出列元素
        :param item:
        :return:
        """
        return self.pop(0)

    def pop_rear(self, item):
        """
        尾部出列元素
        :param item:
        :return:
        """
        return self.pop()

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
