import streamlit as st

st.title("덧셈 계산기")
st.write("두 수를 입력하면 덧셈 결과를 계산해줍니다.")

left_value = st.number_input("첫 번째 숫자", value=0.0, format="%.4f")
right_value = st.number_input("두 번째 숫자", value=0.0, format="%.4f")

if st.button("계산하기"):
    result = left_value + right_value
    st.success(f"{left_value} + {right_value} = {result}")

st.write("---")
st.markdown(
    "### 사용 예시\n"
    "- 3과 5를 입력하면 8을 출력합니다.\n"
    "- 소수도 입력 가능하며 2.5 + 1.25처럼 계산됩니다."
)
