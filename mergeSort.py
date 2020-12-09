def mergeSort(playersDict):
    arr = playersDict.items()
    arr1 = []
    if len(playersDict) % 2 == 0:
        for i in range(0, len(playersDict), 2):
            arr1.append(merge(playersDict[i], playersDict[i + 1]))
    else:
        for i in range(0, len(playersDict) - 1, 2):
            arr1.append(merge(playersDict[i], playersDict[i + 1]))
        arr1.append(playersDict[-1])
    if len(arr1) > 1:
        arr1 = mergeSort(arr1)

    return arr1


def merge(arr1, arr2):
    arr3 = []
    try:
        while len(arr1) > 0 and len(arr2) > 0:
            if arr1[0].getPoints() < arr2[0].getPoints():
                arr3.append(arr1[0])
                del(arr1[0])
            else:
                arr3.append(arr2[0])
                del(arr2[0])
    except:
        print(arr1)
        print(arr2)
    if len(arr1) > 0:
        arr3 += arr1
    if len(arr2) > 0:
        arr3 += arr2
    del(arr1)
    del(arr2)
    return arr3