from django.shortcuts import render
import requests
import json

def air_box(request):
    url = 'https://airbox.edimaxcloud.com/api/tk/query_now?token=ac59b57b-81fb-4fe2-a2e2-d49b25c7f8e5'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data_dict = json.loads(response.text)
        
        if data_dict['status'] == 'ok':
            place_data_dict = {}
            for data in data_dict['exclusion']:
                place_dict = {key: data[key] for key in ['pm25', 'pm10', 'pm1', 'co2', 'hcho', 'tvoc', 'co', 't', 'h', 'status', 'time']}
                place_dict['color'] = "white"  
                
                values_threshold = {'pm25': 35, 'pm10': 75, 'pm1' : 35, 'co2' : 1000, 'hchso' : 0.08, 'tvoc' : 0.56, 'co' :9}
                
                for key in values_threshold:
                    if place_dict[key] > values_threshold[key]:
                        place_dict['color'] = "red"
                        break
                
                place_data_dict[data['name']] = place_dict

            offline_place_data_dict = {}
            for data in data_dict['exclusion']:
                place_dict = {key: data[key] for key in ['status', 'time']}
                offline_place_data_dict[data['name']] = place_dict
            
            context = {
                'place_data_dict': place_data_dict,
                'offline_place_data_dict': offline_place_data_dict,
                'values_threshold': values_threshold,
            }
            return render(request, 'air_box/index.html', context)
    else:
        return render(request, 'error.html', {'message': 'API request failed.'})

