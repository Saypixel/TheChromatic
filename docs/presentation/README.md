## 1 페이지

### 자기소개
![logo](https://i.imgur.com/gmtxAGp.png)
안녕하세요! 저희 팀은 세이픽셀 팀입니다.\
게임 이름은 The Chromatic 입니다.

## 2 페이지

### 필요한 패키지 설치 및 게임 실행
![install&run](./shell.png)\
`pip install -r requirements.txt` 명령어를 쉘에 입력하면 The Chromatic 게임의 필요한 패키지를 설치됩니다.\
`python main.py` 명령어를 쉘에 입력하면 게임이 실행 됩니다.

## 3 페이지

### The Chromatic 게임의 구조
![architecture](./architecture.png)\
The Chromatic 게임의 구조는 이 사진과 동일합니다.\
처음에는 `main.py`` 파일에서 인수를 받아 `debug`, `fps`, `fullscreen`, `fullhd`, `quadhd`, `help` 명령어와 맞는 지 확인합니다.\
그리고 게임이 실행됩니다.

## 4 페이지

### 코드 설명

1. [`동적 카메라`](#동적-카메라)
2. [`업스케일링`](#업스케일링)
3. [`마우스 좌표`](../submission/mouse_position.md)
4. [`동적 텍스트 애니메이션`](../submission/dynamic_text_animation.md)
5. [`중력 & 점프`](../submission/gravity_and_jump.md)

## 6 페이지

### 동적 카메라

## 세계 크기 선언
![1](../images/dynamic_camera_1.png)

화면 및 카메라 크기를 정해준 뒤, 주인공이 돌아다니는 세계 크기도 정합니다.

## 카메라 좌표 선언
![2](../images/dynamic_camera_2.png)

카메라가 어디까지 움직였는지 저장할 좌표 변수 선언

## 동적 카메라 작동 원리
![3](../images/dynamic_camera_3.png)
![4](../images/dynamic_camera_4.png)
![5](../images/dynamic_camera_5.png)

1. 매 프레임 업데이트마다 플레이어가 어느만큼 움직였는지 X좌표를 계산
2. 카메라 좌표가 플레이어 중심으로 움직이게 설정
3. 세계 크기에서 오프셋을 카메라 좌표만큼 이동
4. 화면 (카메라) 크기만큼 잘라서 세계 좌표를 카메라 좌표로 변환

## 결과
![6](../images/dynamic_camera_6.gif)

세계 좌표는 움직이지 않고 고정이지만
카메라 좌표만 움직임.

모든 UI의 좌표를 변경하지 않아도 돼서
관리 및 유지 보수가 매우 편함.

## 참조
- [`config.py`](../../components/config.py)

## 7 페이지

### 업스케일링

## 8 페이지

### 마우스 좌표

## 9 페이지

### 동적 텍스트 애니메이션

## 10 페이지

### 중력 및 점프

## 11 페이지

### 플레이 영상

> TODO: 아직 게임이 완성되지 않아 플레이 영상이 존재하지 않습니다.

## 12 페이지

## 크레딧
![credit](./credit.png)\
저희는 최대한 할 수 있는 만큼 **BGM**, **Coding**, **Design**, **효과음**까지 순수 창작으로 이루어져 있습니다.\
게임 라이브러리인 **pygame**과 디버그 라이브러리인 **icecream**의 도움을 받았고 마지막으로 **Python 3.11** 버전을 기반으로 작성되어 있습니다.

## 13 페이지

### 끝
![end](./end.png)\
저희의 발표를 들어주셔서 감사합니다.
