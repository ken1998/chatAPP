import array

hoge = array.array('B')

bytes = 'あ'.encode('utf-8')
btoint = int.from_bytes(bytes,'big')

hoge.append(btoint)
