class Stack(object):
    """栈"""

    def __init__(self):
        """
        初始化栈
        """
        self.__items = []

    def push(self, item):
        """
        压栈/入栈
        :return None
        """
        self.__items.append(item)

    def pop(self):
        """
        弹栈/出栈
        :return item
        """
        return self.__items.pop()

    def peek(self):
        """
        获取栈顶元素
        :return None or item
        """
        if self.__items:
            return self.__items[-1]
        else:
            return None

    def size(self):
        """
        元素个数
        :return Integer
        """
        return len(self.__items)

    def is_empty(self):
        """
        元素是否为空
        :return Boolean
        """
        return self.__items == []

    def clear(self):
        """
        清空元素
        :return None
        """
        self.__items = []


if __name__ == '__main__':
    s = Stack()
    s.push('one')
    s.push('two')
    s.push('three')
    s.push('four')
    print(s.pop())
    print(s.peek())
    print(s.size())
    print(s.is_empty())
    print(s.clear())
    print(s.size())
