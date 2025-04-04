import pandas as pd
import pickle

def mapper(data):
    mapped = []
    for _, row in data.iterrows():
        mapped.append((row['quality'], row['volatile acidity']))
    return mapped

if __name__ == '__main__':
    data = pd.read_csv('data.csv')

    slice1 = data.iloc[0:399, :]
    slice2 = data.iloc[400:800, :]
    slice3 = data.iloc[801:1200, :]
    slice4 = data.iloc[1201:, :]

    map1 = mapper(slice1)
    map2 = mapper(slice2)
    map3 = mapper(slice3)
    map4 = mapper(slice4)

    shuffled = {
        3.0: [], 4.0: [], 5.0: [],
        6.0: [], 7.0: [], 8.0: [],
    }

    for m in [map1, map2, map3, map4]:
        for q, v in m:
            shuffled[q].append(v)

    with open('shuffled.pkl', 'ab') as file:
        pickle.dump(shuffled, file)

    print("Data has been mapped. Now, run reducer.py to reduce the contents in shuffled.pkl file.")
