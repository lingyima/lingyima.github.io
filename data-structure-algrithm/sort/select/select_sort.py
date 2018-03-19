def select_sort(li):
    n = len(li)
    for i in range(n-1):

        min_index = i
        for j in range(i+1, n):
            if li[min_index] > li[j]:
                min_index = j
                
        li[i], li[min_index] = li[min_index], li[i]


li = [3, 2, 4, 1, 5]
print('排序前：', li)
select_sort(li)
print('排序后：', li)