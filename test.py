# x = 100

# def myfunc():
#     print(x)
#     x = 200
    
    
# myfunc()

x = 100
def f():
    global x
    print("a trong f la = ",x)
    x = 200
    print("a trong f la = ",x)
print(x)
f()



# def f():
# 	print(s)

# 	# This program will NOT show error
# 	# if we comment below line.
# 	s = "Me too."

# 	print(s)


# # Global scope
# s = "I love Geeksforgeeks"
# f()


