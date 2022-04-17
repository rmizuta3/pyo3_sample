import random
import time
import pyo3_salesman

def make_places():
    #地点データの作成
    places=[]
    #random.seed(111)
    while len(places)<100:
        x=random.randint(1,1000)
        y=random.randint(1,1000)
        if (x,y) not in places:
            places.append((x,y))
    return places

def make_distance_table(places):
    #マンハッタン距離のテーブルを作成
    distance_table = [[0 for _ in range(len(places))] for _ in range(len(places))]
    for i in range(len(places)):
        for j in range(len(places)):
            dist = abs(places[i][0]-places[j][0]) + \
                abs(places[i][1]-places[j][1])
            distance_table[i][j] = dist
    return distance_table

def calc_distance(route):
    dist=0
    for i in range(len(route)-1):
        dist += abs(places[route[i]][0]-places[route[i+1]][0]) + \
            abs(places[route[i]][1]-places[route[i+1]][1])
    return dist


def annealing(route, places):
    start_time = time.time()
    max_cost=calc_distance(route)
    route_history=[route]
    for i in range(1000000):
        if time.time()-start_time > 2:
            break
        swap_point1=random.randint(0,99)
        swap_point2=random.randint(0,99)
        if swap_point1==swap_point2:
            continue
        swap_route=route.copy()
        swap_route[swap_point1],swap_route[swap_point2]=route[swap_point2],route[swap_point1]
        #print(swap_route)
        swaproute_cost=calc_distance(swap_route)
        #print(swaproute_cost,max_cost)
        #print(max_cost,)
        if swaproute_cost<max_cost  or random.random()>0.99999:
            route=swap_route
            max_cost=swaproute_cost
            route_history.append(route)
            #print(i,max_cost)
    return max_cost, i

if __name__ == '__main__':

    route=[i for i in range(100)]
    random.shuffle(route)

    places = make_places()

    print("Rust")
    result_1 = 0
    result_2 = 0
    for i in range(10):
        result = pyo3_salesman.annealing(places,route)
        print(result[0],result[1])
        result_1+=result[0]
        result_2+=result[1]
    print(result_1/10,result_2/10)

    print("Python")
    result_1 = 0
    result_2 = 0
    for i in range(10):
        cost,loop_count = annealing(route, places)
        print(cost,loop_count)
        result_1+=cost
        result_2+=loop_count
    print(result_1/10,result_2/10)
