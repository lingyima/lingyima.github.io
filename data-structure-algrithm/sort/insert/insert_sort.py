def insert_sort(li):
    n = len(li)
    for i in range(n-1):
        for j in range(i+1, 0, -1):
            if li[j] < li[j-1]:
                li[j], li[j-1] = li[j-1], li[j]

            else:
                break

                
li = [3, 2, 4, 1, 5]
print('排序前：', li)
insert_sort(li)
print('排序后：', li)