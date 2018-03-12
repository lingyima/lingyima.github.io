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


class SingleRoopLinkList(object):
    """
    单项循环链表
    """

    def __init__(self, node=None):
        """
        初始化单项链表
        """
        self.__head = node
        if node:
            node.next = node;

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
        if self.is_empty():
            return None

        current = self.__head
        while current.next != self.__head:
            print(current.item, '=>next:', current.next.item)
            current = current.next
        print(current.item, '=>next:', current.next.item)


    def add(self, item):
        """
        链表头插入
        """
        if self.is_empty():
            self.__head = Node(item)
            self.__head.next = self.__head
            return None

        node = Node(item)
        current = self.__head

        while current.next != self.__head:
            current = current.next

        node.next = self.__head
        self.__head = node
        current.next = self.__head

    def append(self, item):
        """
        链表尾插入
        """
        if self.is_empty():
            # 第一个节点付给头部节点
            self.__head = Node(item)
            self.__head.next = self.__head
            return None

        current = self.__head
        while current.next != self.__head:
            current = current.next

        current.next = Node(item)
        current.next.next = self.__head

    def insert(self, pos, item):
        """
        指定位置插入节点
        """
        if pos <= 0:
            self.add(item)
            return

        if pos > (self.length() - 1):
            self.append(item)
            return

        index = 0
        previous = self.__head

        while index < pos - 1:
            index += 1
            previous = previous.next

        node = Node(item)
        node.next = previous.next
        previous.next = node

    def remove(self, item):
        """
        删除节点
        """
        current = self.__head

        if current.item == item:
            # 第一个节点元素相等

            # 从第二个节点到最后第二个节点遍历
            while current.next != self.__head:
                current = current.next

            # 最后一个节点的元素的下一个指向第二个对象
            current.next = self.__head.next
            self.__head = self.__head.next
            return

        previous = self.__head

        # 从第二个节点到最后第二个节点遍历比较元素是否相等
        while current.next != self.__head:
            if current.item == item:
                previous.next = current.next
                break

            previous = current
            current = current.next

        # 与最后一个节点元素相等
        if current.item == item:
            previous.next = self.__head

    def search(self, item):
        """
        查找节点是否存在
        """

        current = self.__head

        # 第二个节点元素到最后第二个节点元素比较
        while current.next != self.__head:
            if current.item == item:
                return True

            current = current.next

        # 最有一个节点元素是否相等
        if current.item == item:
            return True

        return False


if __name__ == '__main__':
    sll = SingleRoopLinkList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.add(4)
    sll.add(5)
    sll.insert(2, 6)
    # print(sll.length())
    sll.travel()
    print("-------------")
    sll.remove(4)
    sll.travel()
    print("-------------")
    print(sll.search(60))
    # print(sll.search(4))
