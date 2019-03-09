import array

hoge = array.array('B')

# str to byte
str = '隣の客はよく柿食う客だ'
print(str)
baito: bytes = str.encode('utf-16')
print(baito)

# bytes to int[]
hoge.frombytes(baito)
print(hoge)

# int[] to string
temp = B''
for char in hoge:
    temp += char.to_bytes(1, 'big')
print(temp.decode('utf-16'))
