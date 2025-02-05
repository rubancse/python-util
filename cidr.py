### Solution Code
```python
def find_msb(x, y):
    z = x ^ y
    if z == 0:
        return -1  # or any value indicating no differing bits
    else:
        return z.bit_length() - 1

# Example usage:
x = 8  # binary 1000
y = 10 # binary 1010
print(find_msb(x, y))  # Output: 1 (since the highest differing bit is at position 2^1)
```

