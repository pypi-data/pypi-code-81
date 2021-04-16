from typing import List

def binarysearch(a: List[int], target: int):
    mid = len(a)/2
    low = 0
    high = len(a)-1
    while (a[mid] != target and (low < high)):
        if a[mid] < target:
            low = mid + 1
        else:
            high = mid -1
        mid = int(len(a)/2)
    if a[mid] == target:
        return mid
    return -1
