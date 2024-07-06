import requests
import base64
import cv2 as cv

# opencv 图片
# 定义函数，接受一个图像作为输入参数
def people_detect(img, people_information):
    # 定义百度AI平台车辆检测API的请求URL
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"
    # 使用cv.imencode将图像编码为JPEG格式，返回值是一个元组，包含一个标志和编码后的图像数据
    _, encoded_image = cv.imencode('.jpg', img)
    # 将编码后的图像数据进行Base64编码
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    # 将Base64编码后的图像数据放入字典中，作为POST的请求参数
    params = {"image": base64_image}
    # API认证的访问令牌
    access_token = 'API认证的访问令牌'
    # 将访问令牌附加到请求URL中
    request_url = request_url + "?access_token=" + access_token
    # 请求头
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    # 发送POST请求到API中，附加参数
    response = requests.post(request_url, data=params, headers=headers)
    num = 0
    found = 0
    # 处理返回数据
    if response:
        data = response.json()
        print("API响应数据:", data)  # 调试信息
        print(people_information)
        if 'person_num' in data and 'person_info' in data:
            num = data['person_num']
            for item in data['person_info']:
                if 'attributes' not in item or not item['attributes']:
                    print("未找到此人的属性信息。")
                    continue

                location = item['location']
                x1 = location['left']
                y1 = location['top']
                x2 = x1 + location['width']
                y2 = y1 + location['height']
                attributes = item['attributes']

                try:
                    if (attributes['gender']['name'] == people_information['gender'] and
                        attributes['age']['name'] == people_information['age'] and
                        attributes['upper_wear']['name'] == people_information['upper_wear'] and
                        attributes['lower_wear']['name'] == people_information['lower_wear']):
                        # 在图像上面绘制红色边框，显示人的位置
                        found = found + 1
                        if num <=0:
                            found = 0
                        cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        position = (x1, y1 - 2)
                        # 定义文字字体类型
                        font = cv.FONT_HERSHEY_SIMPLEX
                        # 定义字体缩放比例
                        font_scale = 1
                        color = (0, 0, 255)  # 红色
                        thickness = 2
                        img = cv.putText(img, str(position), position, font, font_scale, color, thickness, cv.LINE_AA)
                    else:
                        # 在图像上面绘制蓝色边框，显示人的位置
                        cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        position = (x1, y1 - 2)
                        # 定义文字字体类型
                        font = cv.FONT_HERSHEY_SIMPLEX
                        # 定义字体缩放比例
                        font_scale = 1
                        color = (255, 0, 0)  # 蓝色
                        thickness = 2
                        img = cv.putText(img, str(position), position, font, font_scale, color, thickness, cv.LINE_AA)
                    print("检测到目标")
                except KeyError as e:
                    print(f"在属性中未找到键: {e}")
        else:
            print("API响应中缺少 'person_num' 或 'person_info'")
    else:
        print("未能从API获取响应")
    return img, num, found
