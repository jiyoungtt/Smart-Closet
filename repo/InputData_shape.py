import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from sklearn.model_selection import train_test_split

BASE_PATH = "/Users/iseungjin/2020_3_2/capstone/inputdata"

# pattern_dir : 각각의 패턴폴더를 담은 폴더
# shape_dir : 종류폴더
# 중요 - 각 폴더별로 이미지갯수 비슷해야함!!!!!
shape_dir = '/Users/hayeong/Desktop/Capstone/DeepFashion DB/final_pattern_dir'
# ex) categories = ['flora', 'checked', 'stripe']

categories = os.listdir(shape_dir)
print('레이블 리스트입니다', categories)
# 총 분류할 클래스 개수 ( 줄무늬, 꽃무늬, 체크무늬 가 총 몇개인지)
class_number = len(categories)

X = []
y = []

# idx = 인덱스, cat = 인덱스값 여기서는 패턴이름들.
for idx, cat in enumerate(categories):
    # one-hot label 만들기 / 0으로 다 채운다음에 해당정답만 1로 바꾸기
    label = [0 for i in range(class_number)]
    label[idx] = 1

    # 포문을 돌면서 category마다 해당카테고리의 이미지파일만 저장할 폴더 생성.
    image_dir = shape_dir + '/' + cat
    # ex) files ='/Users/iseungjin/2020_3_2/capstone/cropImage/pattern/floral/img_00000002.jpg'
    # glob - 특정파일들만 뽑아서 저장.
    files = glob.glob(image_dir+'/*.jpg')
    print(cat, "파일 길이:", len(files))
    for i, f in enumerate(files):
        # 이미지 불러오기 , imread(파일경로, mode)-> mode로 적용할 초기상태 설정할수있음
        # ex) mode - IMREAD_UNCHANGED, IMREAD_GRAYSCALE,
        img = plt.imread(f)
        # 이미지 resize
        # 맨뒤 파라미터- 보간법 인데 이미지를 축소하는경우 inter_area라는 영역보간법을 가장많이 사용 / 확대는 inter_linear
        img_shape = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_LINEAR)

        if img_shape.shape == (64, 64, 3):
            # 해당이미지를 배열로 변경-- 형상은 높이*너비*
            data = np.asarray(img_shape)

            X.append(data)
            y.append(label)
            # 0번째 이미지 출력 / 그다음 700번째 이미지 출력 / 총몇개인지 세거나 에폭때문에 있는거같으나 일단 보류
            # if i % 700 == 0:
            #     print(cat,':', f)
        else:
            continue

    print(cat, "파일생성 완료....")

# X - 입력데이터 이미지값 / Y - 정답레이블 [1,0,0]이면 floral, [0,1,0]이면 checked 이러켕
X = np.array(X)
y = np.array(y)

# 각 데이터 형상
# X_train : (훈련데이터갯수, 높이, 너비, 채널수)
# X_test : (시험데이터갯수, 높이, 너비, 채널수)
# y_train : (훈련데이터갯수, 정답클래스 개수)
# y_test : (시험데이터갯수, 정답클래스 개수)
# default 비율말고 테스트셋은 0.2(대략 600개),
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
xy = (X_train/255.0, X_test/255.0, y_train, y_test)

# 여기서 저장된 image_data_npy파일을 불러서 이걸로 학습을 시키면 됨.
# ex ) X_train, X_test, y_train, y_test = np.load(BASE_PATH + '/image_data.npy') 이렇게 해서 불러오고 코딩하면댐!
np.save('/Users/hayeong/Downloads/image_data_pattern', xy)


# 패턴폴더안에 각각의 패턴이 존재 - 그것들이 카테고리가 됨 ( 카테고리의 개수는 정답레이블의 원소개수)
#
# x - 이미지데이터, y - 정답레이블
#
# enumerate(categories)에서는 idx가 인덱스, cat는 패턴카테고리가 됨(꽃, 줄무늬, 체크)
#
# enumerate(files) 에서  i는 인덱스, f는 이미지 하나당 경로가됨
#
# f를 값으로 가지는 배열이 files임