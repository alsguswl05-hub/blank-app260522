import streamlit as st

st.title("곱셈 계산기")
st.write("두 수를 입력하면 곱셈 결과를 계산해줍니다.")

factor1 = st.number_input("첫 번째 숫자", value=1.0, format="%.4f")
factor2 = st.number_input("두 번째 숫자", value=1.0, format="%.4f")

if st.button("계산하기"):
    result = factor1 * factor2
    st.success(f"{factor1} × {factor2} = {result}")

st.write("---")
st.markdown(
    "### 사용 예시\n"
    "- 3과 5를 입력하면 15를 출력합니다.\n"
    "- 소수도 입력 가능하며 2.5 × 1.2처럼 계산됩니다."
)
