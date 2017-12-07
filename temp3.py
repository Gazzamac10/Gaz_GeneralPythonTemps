X = [1,3,2,4,6,7,5,3]
Y = [9,6,5,4,3,4,5,6]

t = [x for y, x in sorted(zip(X, Y))]

print (t)