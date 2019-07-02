from math import sqrt


# iris object definition
class Iris():
    def __init__(self, x1=None, x2=None, x3=None, x4=None, name=None):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.name = name


# iris distance object definition
class DistIris():
    def __init__(self, distance=None, name=None):
        self.distance = distance
        self.name = name


class ResultIris():
    def __init__(self, name=None, guess=None):
        self.name = name
        self.guess = guess


# read data from specified path
def readData(path):
    file = open(path, "r")
    data = [];
    for x in file:
        data.append(x)
    file.close()
    return data


def printArr(arr):
    for x in arr:
        print(arr)


# split data with given parameters
# test_siz->number of test size in every species
def split_data(data, test_size, numberof_species):
    species_size = int(len(data) / numberof_species)
    split_train, split_test = [], []
    for i in range(numberof_species):
        train_data = data[i * species_size:((i + 1) * species_size - test_size)]
        test_data = data[(i + 1) * species_size - test_size:(i + 1) * species_size]
        split_train += train_data
        split_test += test_data
    return split_train, split_test


def parse_arr(data):
    obj_list = []
    for i in data:
        temp = i.split(',')
        obj_list.append(Iris(float(temp[0]), float(temp[1]), float(temp[2]), float(temp[3]), temp[4]))
    return obj_list


# euclidean distance
# for manhattan p=1, for euclidean p=2
def distance_calc(test, train, p):
    distance_list = []
    for i in train:
        dist = abs(test.x1 - i.x1) ** p + abs(test.x2 - i.x2) ** p + abs(test.x3 - i.x3) ** p + abs(test.x4 - i.x4) ** p
        if p == 2:
            dist = sqrt(dist)
        distance_list.append(DistIris(dist, i.name))
    return distance_list


def knn(train, test, k_value, p_value):
    result = []
    for i in test:
        distance_list = distance_calc(i, train, p_value)
        distance_list.sort(key=lambda x: x.distance, reverse=False)
        nearest = distance_list[:k_value]
        common = most_frequent(nearest)
        result.append(ResultIris(i.name, common))
    return result


def most_frequent(list):
    species_list = []
    for i in list:
        species_list.append(i.name)
    return max(set(species_list), key=species_list.count)


def success_rate(list):
    count = 0
    for i in list:
        if i.name == i.guess:
            count += 1
    return count / len(list)


def predict_result(list, test_size):
    base_matrix = ["Iris-setosa\n", "Iris-versicolor\n", "Iris-virginica\n"]
    temp = [0, 0, 0]
    conf_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    count, i = 0, 0
    while i < len(base_matrix):
        arr = list[i * test_size:(i + 1) * test_size]
        for j in arr:
            if j.name == j.guess:
                count += 1
            else:
                index = base_matrix.index(j.guess)
                temp[index] += 1
        print(list[test_size * i].name + "true success times is" + str(count))
        conf_matrix[i] = temp
        conf_matrix[i][i] = count
        count = 0
        temp = [0, 0, 0]
        i += 1
    return conf_matrix


if __name__ == '__main__':
    data = readData("iris.data")
    list = parse_arr(data)
    test_size = 17
    train, test = split_data(list, test_size, 3)  # last parameter is number of species type
    result = knn(train, test, 5, 2)  # 5 is k values, 2 is p values
    print("success rate is " + str(success_rate(result)))
    conf_matrix = predict_result(result, test_size)
    print(conf_matrix)
