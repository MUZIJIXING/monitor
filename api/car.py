import requests
import base64
import cv2 as cv

# 定义函数，接受一个图像作为输入参数
def vehicle_detect(img, car_id):
    # 定义百度AI平台车辆检测API的请求URL
    request_url_id = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
    request_url_num = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"

    # 使用cv.imencode将图像编码为JPEG格式，返回值是一个标志和编码后的图像数据
    _, encoded_image = cv.imencode('.jpg', img)
    # 将编码后的图像数据进行Base64编码
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    # 将Base64编码后的图像数据放入字典中，作为POST的请求参数
    params = {"image": base64_image}
    # API认证的访问令牌
    access_token = 'API认证的访问令牌'
    # 将访问令牌附加到请求URL中
    request_url_id = request_url_id + "?access_token=" + access_token
    request_url_num = request_url_num + "?access_token=" + access_token
    # 请求头
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    # 发送POST请求到API中，附加参数
    response_id = requests.post(request_url_id, data=params, headers=headers)
    response_num = requests.post(request_url_num, data=params, headers=headers)

    num = 0
    found = 0
    car_num = {"car": 0, "truck": 0, "bus": 0}

    # 处理车牌识别返回数据
    if response_id:
        data_id = response_id.json()
        if 'words_result' in data_id and len(data_id['words_result']) > 0:
            result_id = data_id['words_result']['number']
            if result_id == car_id:
                found = 1
                id_location = data_id['words_result']['vertexes_location']
                x1 = id_location[0]['x']
                y1 = id_location[0]['y']
                x2 = id_location[2]['x']
                y2 = id_location[2]['y']
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # 处理车辆检测返回数据
    if response_num:
        data_num = response_num.json()
        if 'vehicle_num' in data_num and 'vehicle_info' in data_num:
            vehicle_info = data_num['vehicle_info']
            car_num['car'] = data_num['vehicle_num']['car']
            car_num['bus'] = data_num['vehicle_num']['bus']
            car_num['truck'] = data_num['vehicle_num']['truck']
            num = car_num['car'] + car_num['bus'] + car_num['truck']

            for item in vehicle_info:
                if item['type'] == 'carplate':
                    continue
                location = item['location']
                x1 = location['left']
                y1 = location['top']
                x2 = x1 + location['width']
                y2 = y1 + location['height']
                # 在图像上面绘制红色边框，显示车辆位置
                cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                # 定义要绘制的文字
                text = item['type']
                position = (x1, y1 - 2)
                # 定义文字字体类型
                font = cv.FONT_HERSHEY_SIMPLEX
                # 定义字体缩放比例
                font_scale = 1
                color = (255, 0, 0)  # 蓝色
                thickness = 2
                # 在车辆上绘制车辆类型文字，附加字体设置
                img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)

    # 返回图像及车辆数目
    return img, num, car_num, found
