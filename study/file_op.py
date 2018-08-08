#文件操作

#写入
file1 = open('sanguo.txt','w')  #w表示写，r表示读（默认r）
file1.write("诸葛亮 \n")
file1.close() #关闭并保存文件


file3 = open('sanguo.txt','a')  #w表示写，r表示读（默认r）,a表示追加
file3.write("诸葛亮 ")
file3.close() #关闭并保存文件


#读取
file2 = open('sanguo.txt')
print(file2.read())
file2.close()

#读取一行
file4 = open('sanguo.txt')
print(file4.readline())
file4.close()

#读取所有行
file5 = open('sanguo.txt')
for content in file5.readlines():
    print(content)

#指针
file6 = open('sanguo.txt','rb')
print(file6.tell())   ##tell()  打印指针的位置

print(file6.read(1))  ##读取第一个

file6.seek(3)  ##seek可以控制指针的位置的偏移（默认），并读取字符

# 第一个参数代表偏移位置，第二个参数  0 表示从文件开头偏移  1表示从当前位置偏移，   2 从文件结尾
file6.seek(3,2)  #默认1

print(file6.tell())

file6.close()
