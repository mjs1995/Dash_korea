# 지도 시각화 웹 개발 [Link](https://korea-dashboard.herokuapp.com/)
![image](https://user-images.githubusercontent.com/47103479/125803097-452b72fe-d4be-475b-a6ba-38feb23fed01.png)

- Dash와 heroku를 이용하여 프로젝트 결과물을 웹 구현화 하였습니다.

![videoplay](https://media.giphy.com/media/uOc6AtZxVW9r1FlqSp/giphy.gif)

## Dash app project structure

#### Data
- 2018소멸위험지수.csv 
- map (7).zip.geojson

#### Project boilerplate

    apps
    ├── ...
    ├── Dash_korea              # app project
    │   ├── .gitignore          # Backup File, Log File
    │   ├── data                # data(2018소멸위험지수.csv / map (7).zip.geojson)
    │   ├── app.py              # dash application
    │   ├── Procfile            # used for heroku deployment 
    │   ├── requirements.txt    # project dependecies
    │   └── ...                 
    └── ...

