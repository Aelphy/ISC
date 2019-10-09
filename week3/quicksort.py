def quicksort(array, left, right):
    pivot = # select the pivot somehow
    if left < right:
        pivot_idx = partition(array, left, right, pivot)
        quicksort(array, left, pivot_idx)
        quicksort(array, pivot_idx + 1, right)
