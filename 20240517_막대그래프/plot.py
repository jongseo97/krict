# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:43:46 2024

@author: user
"""

import matplotlib.pyplot as plt
import numpy as np

# 예제 데이터
models = ['cutoff-50', 'cutoff-100']
f1 = [0.57, 0.63]
auc_roc = [0.76, 0.79]

# 막대의 너비 및 위치 설정
bar_width = 0.35
index = np.arange(len(models))

# 막대 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 6))
bar1 = plt.bar(index, f1, bar_width, label='weighted f1-score', color='yellowgreen')
bar2 = plt.bar(index + bar_width, auc_roc, bar_width, label='weighted AUC-ROC', color='dodgerblue')

# 그래프에 제목과 레이블 추가
plt.title('Model Performance Comparison')
plt.xlabel('Models')
plt.ylabel('Scores')
plt.xticks(index + bar_width / 2, models)

# 각 막대 위에 값 표시
for bar in bar1:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2 , yval + 0.01, round(yval, 2), ha='center')
for bar in bar2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2 , yval + 0.01, round(yval, 2), ha='center')

# 범례 추가
plt.legend()

# 그래프 보여주기
plt.ylim(0, 1)
plt.show()