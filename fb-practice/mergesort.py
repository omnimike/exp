
def merge_sort(arr):
    tmp = arr[:]
    chunk_size = 1
    while chunk_size < len(arr):
        offset = 0
        while offset < len(arr):
            part_a_start = offset
            part_a_end = min(offset + chunk_size, len(arr))
            part_b_start = part_a_end
            part_b_end = min(part_b_start + chunk_size, len(arr))
            a = part_a_start
            b = part_b_start
            while a < part_a_end and b < part_b_end:
                if arr[a] < arr[b]:
                    tmp[offset] = arr[a]
                    a += 1
                else:
                    tmp[offset] = arr[b]
                    b += 1
                offset += 1
            while a < part_a_end:
                tmp[offset] = arr[a]
                a += 1
                offset += 1
            while b < part_b_end:
                tmp[offset] = arr[b]
                b += 1
                offset += 1
        chunk_size *= 2
        s = tmp
        tmp = arr
        arr = s
    return arr


if __name__ == '__main__':
    examples = [
        [],
        ['a'],
        ['a', 'b'],
        ['b', 'a'],
        ['c', 'b', 'a'],
        ['c', 'b', 'a', 'd'],
        ['b', 'b', 'a', 'c'],
    ]
    for example in examples:
        print('expected', sorted(example), 'actual', merge_sort(example[:]))
