
# Python program to demonstrate Range Update 
# and Range Queries using BIT 
  
# Returns sum of arr[0..index]. This function assumes 
# that the array is preprocessed and partial sums of 
# array elements are stored in BITree[] 
def get_sum(BITree: list, index: int) -> int: 
    summ = 0 # Initialize result 
  
    # index in BITree[] is 1 more than the index in arr[] 
    index = index + 1
  
    # Traverse ancestors of BITree[index] 
    while index > 0: 
  
        # Add current element of BITree to sum 
        summ += BITree[index] 
  
        # Move index to parent node in getSum View 
        index -= index & (-index) 
    return summ 
  
# Updates a node in Binary Index Tree (BITree) at given 
# index in BITree. The given value 'val' is added to 
# BITree[i] and all of its ancestors in tree. 
def update_bit(BITTree: list, n: int, index: int, val: int) -> None: 
  
    # index in BITree[] is 1 more than the index in arr[] 
    index = index + 1
  
    # Traverse all ancestors and add 'val' 
    while index <= n: 
  
        # Add 'val' to current node of BI Tree 
        BITTree[index] += val 
  
        # Update index to that of parent in update View 
        index += index & (-index) 
  
  
# Returns the sum of array from [0, x] 
def summation(x: int, BITTree1: list, BITTree2: list) -> int: 
    return (get_sum(BITTree1, x) * x) - get_sum(BITTree2, x) 
  
  
def update_range(BITTree1: list, BITTree2: list, n: int, val: int, l: int, 
                r: int) -> None: 
  
    # Update Both the Binary Index Trees 
    # As discussed in the article 
  
    # Update BIT1 
    update_bit(BITTree1, n, l, val) 
    update_bit(BITTree1, n, r + 1, -val) 
  
    # Update BIT2 
    update_bit(BITTree2, n, l, val * (l - 1)) 
    update_bit(BITTree2, n, r + 1, -val * r) 
  
def range_sum(l: int, r: int, BITTree1: list, BITTree2: list) -> int: 
  
    # Find sum from [0,r] then subtract sum 
    # from [0,l-1] in order to find sum from 
    # [l,r] 
    return summation(r, BITTree1, BITTree2) - summation( l - 1, BITTree1, BITTree2) 

# This code is contributed by 
# sanjeev2552

# https://www.geeksforgeeks.org/binary-indexed-tree-range-update-range-queries/?ref=lbp