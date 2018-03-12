class Node(object):
    """
    双向循环链表节点类
    """

    def __init__(self, item):
        """
        初始化节点
        :param item:
        """

        self.item = item
        self.next = None
        self.prev = None


class DoubleRoopLinkList(object):
    def __init__(self, node=None):
        """
        初始化单项链表
        """
        if node != None:
            self.__head = Node(node)
            self.__head.next = self.__head
            self.__head.prev = self.__head
        else:
            self.__head = None

    def is_empty(self):
        """
        链表是否为空
        """
        return self.__head == None

    def length(self):
        """
        链表长度
        :return: count
        """

        if self.is_empty():
            return 0

        count = 1
        current = self.__head
        while current.next != self.__head:
            count += 1
            current = current.next
        return count

    def travel(self):
        """
        遍历链表
        """

        if self.__head:
            current = self.__head
            while current.next != self.__head:
                print('prev: %i <= current: %i => next: %i' %(current.prev.item, current.item, current.next.item))
                current = current.next

            print('prev: %i <= current: %i => next: %i' % (current.prev.item, current.item, current.next.item))

        else:
            return None

    def add(self, item):
        """
        链表头插入
        """
        if self.is_empty():
            self.__head = Node(item)
            self.__head.next = self.__head
            self.__head.prev = self.__head
        else:
            current = self.__head
            while current.next != self.__head:
                current = current.next

            node = Node(item)
            current.next = node
            node.prev = current

            self.__head.prev = node
            node.next = self.__head
            self.__head = node


    def append(self, item):
        """
        链表尾插入
        """
        if self.is_empty():
            # 第一个节点付给头部节点
            self.__head = Node(item)
            self.__head.next = self.__head
            self.__head.prev = self.__head

        else:
            # 是否存在头节点，存在
            current = self.__head
            while current.next != self.__head:
                current = current.next

            node = Node(item)

            current.next = node
            node.prev = current

            node.next = self.__head
            self.__head.prev = node

    def insert(self, pos, item):
        """
        指定位置插入节点
        """

        if pos <= 0:
            self.add(item)

        elif pos > (self.length()-1):
            self.append(item)

        else:
            index = 0
            previous = self.__head

            while index < pos -1:
                index += 1
                previous = previous.next

            node = Node(item)
            node.next = previous.next
            previous.next = node
            node.prev = previous
            node.next.prev = node

    def remove(self, item):
        """
        删除节点
        """

        if self.is_empty():
            return

        if self.__head.item == item:
            self.__head = self.__head.next
            self.__head.prev = None
            return

        current = self.__head
        previous = None

        while current:
            if current.item == item:
                previous.next = current.next
                current.next.prev = previous
                break
            else:
                previous = current
                current = current.next

    def search(self, item):
        """
        查找节点是否存在
        """
        if self.is_empty():
            return False

        current = self.__head
        while current.next != self.__head:
            if current.item == item:
                return True
            current = current.next

        if current.item == item:
            return True
        return False

if __name__ == '__main__':
    sll = DoubleRoopLinkList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.add(4)
    sll.insert(2, 5)
    sll.travel()
    print("========")
    sll.remove(5)
    sll.travel()
    print(sll.search(5))