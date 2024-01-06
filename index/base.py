


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

# zone 到 erank 的移動距離
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
def efficiency_ratio(total_moving_time,total_moves):
    average_time = total_moving_time/total_moves
    print(average_time)
    efficiency = []
    efficiency.append((average_time + calculate_loading_time(1)) / 1)
    efficiency.append((average_time + calculate_loading_time(2)) / 2)
    efficiency.append((average_time + calculate_loading_time(3)) / 3)

    print((efficiency[0]*1+efficiency[1]*2+efficiency[2]*2)/5)
    return ((efficiency[0]*1+efficiency[1]*2+efficiency[2]*2)/5)/efficiency[0]


# 總時間
def total_time(zone_distances,coordinate,data,speed):
    ans = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            ans += (data[i][j]*moving_time(zone_distances,coordinate,i,j,1,speed))

    return ans