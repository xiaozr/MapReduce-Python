import pandas as pd
import pickle

data = pd.read_csv('data.csv')

#Slicing Data
slice1 = data.iloc[0:399,:]
slice2 = data.iloc[400:800,:]
slice3 = data.iloc[801:1200,:]
slice4 = data.iloc[1201:,:]

def mapper(data):
    
    mapped = []
    
    for index,row in data.iterrows():
        
        mapped.append((row['quality'],row['volatile acidity']))
        
    return mapped


map1 = mapper(slice1)
map2 = mapper(slice2)
map3 = mapper(slice3)
map4 = mapper(slice4)

shuffled = {
    3.0: [],
    4.0: [],
    5.0: [],
    6.0: [],
    7.0: [],
    8.0: [],
    
}

for i in [map1,map2,map3,map4]:
    for j in i:
        shuffled[j[0]].append(j[1])

file= open('shuffled.pkl','ab')
pickle.dump(shuffled,file)
file.close()

print("Data has been mapped. Now, run reducer.py to reduce the contents in shuffled.pkl file.")