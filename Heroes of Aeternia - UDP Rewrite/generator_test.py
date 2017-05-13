import math,random

##for n in range(1,75):
##
##    print(100*1.05**n,n)
##
##    print(100 + 10*n)

test_out = open(".//Test map.txt","w")


heightmap = {}

x_size = 30

y_size = 30

for x in range(0,x_size + 1):

    for y in range(0,y_size + 1):

##        t[(x,y)] = round(math.sin(x)+math.sin(y))

        if random.randrange(1,10) == 2:

            heightmap[(x,y)] = random.randrange(1,20)

        else:

            heightmap[(x,y)] = 0

##    smoothing algorithm?

for x in range(0,5):

    for n in heightmap.keys():

        if n[0] > 0 and n[0] < x_size  and n[1] > 0 and n[1] < y_size:

            heightmap[n] = round((heightmap[(n[0]+1,n[1])] + heightmap[(n[0]-1,n[1])] + heightmap[(n[0],n[1]-1)] + heightmap[(n[0],n[1]+1)]) /4)



max_x = []

max_y = []
    
for k in heightmap.keys():

    max_x.append(k[0])

    max_y.append(k[1])

max_x = max(max_x)

max_y = max(max_y)

print(max_x,max_y)

height = []

for y in range(0,max_y+1):

    temp = []

    for x in range(0,max_x+1):

        temp.append(0)

    height.append(temp)

for k in heightmap.keys():

##    print(k)

    height[k[1]][k[0]] = heightmap[k]

for y in height:

    for h in y:

        for n in range(0,(3-len(str(h)))+1):

            test_out.write(" ")

        test_out.write(str(h))

    test_out.write("\n")

test_out.close()

print(height)


        
