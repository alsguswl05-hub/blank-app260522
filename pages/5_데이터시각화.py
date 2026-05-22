import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("데이터 시각화 예시")
st.write("matplotlib, seaborn, plotly를 사용한 간단한 데이터 시각화 예시입니다.")

# 1. Matplotlib 예시
st.header("1. Matplotlib 라인 그래프")
월 = ["1월", "2월", "3월", "4월", "5월", "6월"]
매출 = [120, 150, 170, 160, 180, 210]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(월, 매출, marker="o", color="#d95f97", linewidth=3)
ax.set_title("월별 매출 추이", fontsize=16)
ax.set_xlabel("월", fontsize=12)
ax.set_ylabel("매출 (백만원)", fontsize=12)
ax.grid(alpha=0.3)

st.pyplot(fig)

# 2. Matplotlib 막대그래프
st.header("2. Matplotlib 막대그래프")
제품 = ["A제품", "B제품", "C제품", "D제품"]
판매량 = [35, 28, 45, 30]

fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.bar(제품, 판매량, color="#8da0cb")
ax2.set_title("제품별 판매량", fontsize=16)
ax2.set_xlabel("제품", fontsize=12)
ax2.set_ylabel("판매량 (개)", fontsize=12)
for i, v in enumerate(판매량):
    ax2.text(i, v + 1, str(v), ha="center", fontsize=12)

st.pyplot(fig2)

# 3. Seaborn 예시
st.header("3. Seaborn 산점도")

tips = sns.load_dataset("tips")
tips = tips.rename(columns={"total_bill": "주문금액", "tip": "팁", "size": "인원수"})

fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=tips,
    x="주문금액",
    y="팁",
    hue="인원수",
    palette="magma",
    alpha=0.8,
    ax=ax3,
)
ax3.set_title("주문금액과 팁의 관계", fontsize=16)
ax3.set_xlabel("주문금액 (달러)", fontsize=12)
ax3.set_ylabel("팁 (달러)", fontsize=12)

st.pyplot(fig3)

# 4. Plotly 예시
st.header("4. Plotly 막대그래프")
과일 = ["사과", "바나나", "체리", "딸기"]
판매 = [40, 55, 30, 50]
plotly_df = pd.DataFrame({"과일": 과일, "판매량": 판매})

fig4 = px.bar(
    plotly_df,
    x="과일",
    y="판매량",
    text="판매량",
    color="과일",
    title="과일별 판매량",
)
fig4.update_layout(
    xaxis_title="과일",
    yaxis_title="판매량 (개)",
    legend_title="과일",
    plot_bgcolor="rgba(245,245,245,1)",
)
fig4.update_traces(textposition="outside")

st.plotly_chart(fig4, use_container_width=True)

# 5. Plotly 파이차트
st.header("5. Plotly 파이차트")
파이_df = pd.DataFrame({
    "카테고리": ["온라인", "매장", "전화 주문", "기타"],
    "비중": [45, 30, 15, 10],
})
fig5 = px.pie(
    파이_df,
    names="카테고리",
    values="비중",
    title="주문 채널 비중",
    hole=0.4,
)
fig5.update_traces(textinfo="percent+label")

st.plotly_chart(fig5, use_container_width=True)
