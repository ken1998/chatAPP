import array

hoge = array.array('B')

# str to byte
str = 'あいうえお'
print(str)
bytes = str.encode('utf-8')
print(bytes)

# bytes to int[]
hoge.frombytes(bytes)
print(hoge)

# int[] to string
temp = B''
for char in hoge:
    temp += char.to_bytes(1, 'big')
print(temp.decode())
