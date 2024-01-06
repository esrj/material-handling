from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from index.base import total_time,efficiency_ratio,total_moving_time,total_moves

# from index.opt import
import math
import json

@csrf_exempt
def index(request):
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
        final_ans = ((total_time(zone_distances,coordinate,data,float(speed))*10/8) / (86400*30))*efficiency_ratio(total_moving_time(zone_distances,coordinate,data,float(speed)),total_moves(data))
        average_times = total_time(zone_distances,coordinate,data,speed)/total_moves(data)
        return JsonResponse({'errno':0,"final_ans":math.ceil(final_ans),"average_time":average_times})
    else:
        return render(request, 'index.html')





