
import math

def calculate_erack_distance(coordinate, start, end):
    if start == end:
        return 0
    if start < 0 or end >= len(coordinate):
        return "Invalid indices"

    start_point = coordinate[start]
    end_point = coordinate[end]
    horizontal_distance = abs(end_point[0] - start_point[0])
    vertical_distance = abs(end_point[1] - start_point[1])
    stair_distance = horizontal_distance + vertical_distance

    return stair_distance

# zone 到 zone 的移動距離
def calculate_zone_distance(zone_distances,coordinate,start, end):
    if start == end:
        return zone_distances[start]
    else:
        return (zone_distances[start] + zone_distances[end])/2 + 10 + calculate_erack_distance(coordinate,start,end)

# 交換時間
def calculate_loading_time(num_loads):
    if num_loads == 1:
        return 3 * 2 + 3 * 5 + 4 * 40
    elif num_loads == 2:
        return 4 * 2 + 6 * 5 + 8 * 40
    elif num_loads == 3:
        return 5 * 2 + 9 * 5 + 12 * 40

# 總移動次數
def total_moves(data):
    moves = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            moves += data[i][j]
    return moves

# 當趟總時間（不括交換時間）
def moving_time_without_loading(zone_distances,coordinate,start,end,speed):
    return calculate_zone_distance(zone_distances,coordinate,start,end ) /speed


# 當趟總時間（包括交換時間）
def moving_time(zone_distances,coordinate,start,end,num_loads,speed):
    return calculate_zone_distance(zone_distances,coordinate,start, end)/speed + calculate_loading_time(num_loads)

# 總移動時間（不包括交換時間）
def total_moving_time(zone_distances,coordinate,data,speed):
    ans = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            ans += (data[i][j]*moving_time_without_loading(zone_distances,coordinate,i,j,speed))
    return ans



# 計算效率比例
def weighted_average(total_moving_time,total_moves):
    average_time = (total_moving_time/total_moves)
    return [ 1/((average_time + calculate_loading_time(1))*10/8 ), 1/((average_time + calculate_loading_time(2))*10/8)*2 ,1/((average_time + calculate_loading_time(3))*10/8)*3 ]



# 總時間


zone_distances = [115,115,122.5,135.5,115,122.5,122.5,127.5]

data = [
    [88404, 24045, 2636,  753,   18506, 17268, 16120, 7136],
    [9266,  6865,  7133,  11018, 9717,  12595, 8676,  8087],
    [4580,  4758,  7679,  12046, 0,     21188, 350,   1644],
    [2309,  8825,  8193,  8793,  0,     28739, 659,   6122],
    [325,   139,   12,    68,    22848, 8859,  23568, 2357],
    [43694, 20717, 21597, 30046, 6323,  30430, 23817, 30752],
    [9268,  1240,  1409,  876,   377,   64066, 22784, 6250],
    [13326, 3481,  4133,  4095,  382,   22030, 10113, 13078]
]

coordinate = [
    (53 + 36 + 24 + 17 / 2, 115),
    (53 + 36 + 24 / 2, 115),
    (53 + 36 / 2, 115),
    (53 / 2, 115),
    (41 + 36 + 36 + 17 / 2, 55),
    (41 + 36 + 36 / 2, 55),
    (41 + 36 / 2, 55),
    (41 / 2, 55),
]

speed = 0.5

total_moving_time = total_moving_time( zone_distances , coordinate , data , speed )
total_move = total_moves( data )

AMR1_ratio = ( weighted_average(total_moving_time,total_move)[0]/sum(weighted_average(total_moving_time,total_move)) )
AMR2_ratio = ( weighted_average(total_moving_time,total_move)[1]/sum(weighted_average(total_moving_time,total_move)) )
AMR3_ratio =( weighted_average(total_moving_time,total_move)[2]/sum(weighted_average(total_moving_time,total_move)) )


total_time = 0
for i in range(8):
    for j in range(8):
        total_time+=data[i][j]


def ARM(num):
    if num == 1:
        return math.ceil(total_time*AMR1_ratio)
    if num == 2:
        return math.ceil(total_time*AMR2_ratio)
    if num == 3:
        return math.ceil(total_time*AMR3_ratio)
#
# print(ARM(1))
# print(ARM(2))
# print(ARM(3))
#
print(total_move)
print(ARM(1)+ARM(2)+ARM(3))




all_zone_distance = []
for i in range(8):
    for j in range(8):
        all_zone_distance.append([calculate_zone_distance(zone_distances,coordinate,i,j),i,j])



all_zone_distance = sorted(all_zone_distance, key=lambda x: x[0], reverse=True)
all_zone_distance = [sublist[1:] for sublist in all_zone_distance]

num = 3
temp = ARM(num)
final_time = 0
for coord in (all_zone_distance):
    if temp >= data[coord[0]][coord[1]]:
        temp -= int(data[coord[0]][coord[1]])

        final_time+=data[coord[0]][coord[1]]/num*moving_time(zone_distances,coordinate,coord[0],coord[1],num,speed)
    else :

        final_time+=temp/num*moving_time(zone_distances,coordinate,coord[0],coord[1],num,speed)


        data[coord[0]][coord[1]] -= temp

        num-=1
        temp = ARM(num)
        temp -= math.ceil(data[coord[0]][coord[1]])
        final_time+=data[coord[0]][coord[1]]/num*moving_time(zone_distances,coordinate,coord[0],coord[1],num,speed)

print(temp)

print(3*(final_time*10/8)/(86400*30))




