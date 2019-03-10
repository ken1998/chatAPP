import multiprocessing as mp
import array

hoge = mp.Array('u', 0)

# str to byte
str = 'ほげええええええ'
print(str)
baito: bytes = str.encode('utf-16le')
print(baito)

# bytes to int[]
testarray = array.array('u')
testarray.frombytes(baito)
with hoge.get_lock():
    hoge = testarray
    print(hoge)

# hoge = testarray

# int[] to string
temp = B''
"""
for char in hoge:
    temp += char.to_bytes(1, 'big')
"""
temp += hoge

strings = hoge
strings = strings.decode('utf-16le')
print (strings)
print(hoge)
print(temp.decode('utf-16le'))
