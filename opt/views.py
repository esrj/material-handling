from django.shortcuts import render
import math
from django.http import JsonResponse, HttpResponse
from opt.opt import calculate_zone_distance,ARM,moving_time
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def opt(request):

    if request.method == 'POST':


        body_str = request.body.decode('utf-8')
        param = json.loads(body_str)
        data = param.get('from_to_chart', None)
        speed = float(param.get('speed',0.5))
        zone_distances = param.get('zone_distances',None)
        zone_distances = (zone_distances[1])
        width = param.get('width', None)
        coordinate = []

        for j,group in enumerate(width):
            for i, value in enumerate(group):
                x = sum(group[:len(group)-(i+1)])+group[len(group)-i-1]/2
                if j == 0:
                    y = 60
                else:
                    y = 0
                coordinate.append((x, y))
        all_zone_distance = []
        for i in range(8):
            for j in range(8):
                all_zone_distance.append([calculate_zone_distance(zone_distances, coordinate, i, j), i, j])

        all_zone_distance = sorted(all_zone_distance, key=lambda x: x[0], reverse=True)
        all_zone_distance = [sublist[1:] for sublist in all_zone_distance]

        num = 3
        temp = ARM(num)
        final_time = 0
        for coord in (all_zone_distance):
            if temp >= data[coord[0]][coord[1]]:
                temp -= int(data[coord[0]][coord[1]])

                final_time += data[coord[0]][coord[1]] / num * moving_time(zone_distances, coordinate, coord[0], coord[1],
                                                                           num, speed)
            else:

                final_time += temp / num * moving_time(zone_distances, coordinate, coord[0], coord[1], num, speed)

                data[coord[0]][coord[1]] -= temp

                num -= 1
                temp = ARM(num)
                temp -= math.ceil(data[coord[0]][coord[1]])
                final_time += data[coord[0]][coord[1]] / num * moving_time(zone_distances, coordinate, coord[0], coord[1], num, speed)

        return JsonResponse({'errno':0,'final_ans':math.ceil((final_time * 10 / 8) / (86400 * 30))})
    if request.method == 'GET':
        return render(request,'opt.html')

