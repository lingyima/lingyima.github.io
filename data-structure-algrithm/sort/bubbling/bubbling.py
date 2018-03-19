def bubbling_sort(li):
    n = len(li)
    for j in range(n-1):
        count = 0
        for i in range(0, n-1-j):
            if li[i] > li[i+1]:
                li[i], li[i+1] = li[i+1], li[i]
                count += 1

        if count == 0:
            return


li = [8, 2, 3, 7, 1, 9, 5, 6, 4]
print('排序前：', li)
bubbling_sort(li)
print('排序后：', li)