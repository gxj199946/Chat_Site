import requests
from flask import current_app

def get_city_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/city/", timeout=5)
        if response.status_code == 200:
            city = response.text.strip()
            if city:
                current_app.logger.info(f"IP {ip} 对应的城市: {city}")
                return city
            else:
                current_app.logger.warning(f"IP {ip} 未返回城市信息")
        else:
            current_app.logger.warning(f"获取城市失败，状态码: {response.status_code}")
    except Exception as e:
        current_app.logger.error(f"获取城市时发生错误: {str(e)}")
    return "未知城市"

def get_location_from_coords(latitude, longitude):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 200:
        data = response.json()
        if 'address' in data:
            return data['address']
    return None