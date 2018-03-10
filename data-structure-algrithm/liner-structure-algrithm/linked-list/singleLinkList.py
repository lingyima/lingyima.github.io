class Node(object):
    """
    单项链表节点类
    """

    def __init__(self, item):
        """
        初始化节点
        :param item:
        """

        self.item = item
        self.next = None

class SingleLinkList(object):
    def __init__(self, node=None):
        """
        初始化单项链表
        """
        self.__head = node

    def is_empty(self):
        """
        链表是否为空
        :return:
        """
        return self.__head == None

    def length(self):
        """
        链表长度
        :return: count
        """
        count = 0
        current = self.__head
        while current:
            count += 1
            current = current.next
        return count

    def travel(self):
        """
        遍历链表
        :return:
        """
        if self.__head:
            current = self.__head
            while current:
                print(current.item)
                current = current.next
        else:
            return None

    def add(self, item):
        """
        链表头插入
        :param item:
        :return:
        """
        if self.is_empty():
            self.__head = Node(item)
        else:
            current = self.__head
            self.__head = Node(item)
            self.__head.next = current

    def append(self, item):
        """
        链表尾插入
        :param item:
        :return:
        """
        if self.is_empty():
            # 第一个节点付给头部节点
            self.__head = Node(item)
        else:
            # 是否存在头节点，存在
            current = self.__head
            while current.next:
                current = current.next
            current.next = Node(item)

    def insert(self, pos, item):
        """
        指定位置插入节点
        :param pos:
        :param item:
        :return:
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

    def remove(self, item):
        """
        删除节点
        :param item:
        :return:
        """
        current = self.__head
        previous = None
        if current.item == item:
            self.__head == self.__head.next
        else:
            while current:
                if current.item == item:
                    previous.next = current.next
                    break
                else:
                    previous = current
                    current = current.next




    def search(self, item):
        """
        查找节点是否存在
        :param item:
        :return:
        """
        current = self.__head
        while current:
            if current.item == item:
                return True
            current = current.next
        return False

if __name__ == '__main__':
    sll = SingleLinkList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.add(4)
    sll.insert(2, 100)
    sll.insert(-4, -400)
    sll.insert(10, 88)
    sll.remove(4)
    sll.travel()
    print(sll.search(101))