class extrapolate():

    def __init__(self,nodes=[[0,0,100,0],[50,50,50,25],[100,150,-50,50]]): # node: [x,y1,y2...], where 1,2... = series, IMPORTANT: Sorted by x

        self.nodes = nodes

    def extrapolate(self,value=1,series=1):

        nearest_nodes = []

        valid = True

        if value < self.nodes[0][0]:

            print("Value out of range: Too small")

            valid = False

        if value > self.nodes[len(self.nodes)-1][0]:

            print("Value out of range: Too big")

            valid = False

        if valid == True:

            for node in self.nodes:

                if node[0] == value:

                    print(node[series])

                if node[0] > value:

                    node_pair = [last_node,node]

                    print(node_pair)
                    
                    value = node_pair[0][series] + ((node_pair[1][series] - node_pair[0][series]) / (node_pair[1][0] - node_pair[0][0])) * (value - node_pair[0][0])

                    print(value)

                    return(value)


                last_node = node


ex=extrapolate()

ex.extrapolate(value=58.2,series=1)
