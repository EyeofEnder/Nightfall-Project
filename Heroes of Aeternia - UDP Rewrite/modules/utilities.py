def read_text_file(file_path = None,linewise = True):

    file = None

    line = None

    temp = []

    if type(file_path) == str:

        try:

            if linewise == True:

                file = open(file_path)

                line = file.readline()

                while line != "":

                    temp.append(line)

                    line = file.readline()

            else:

                file = open(file_path)

                temp = file.read()

        except:

            pass

    return temp

class extrapolate(self,values=[[1,1,10],[10,10,1]],curve="linear"):

    self.values = values

    self.curve = curve

    def extrapolate(self,value=1,series=1):

        temp_values = []

        for value in self.values:

            temp_values.append[series]

        print(temp_values)

    

            

        
