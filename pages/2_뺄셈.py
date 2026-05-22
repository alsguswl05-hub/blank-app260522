import streamlit as st

st.title("뺄셈 계산기")
st.write("두 수를 입력하면 뺄셈 결과를 계산해줍니다.")

minuend = st.number_input("첫 번째 숫자 (피감수)", value=0.0, format="%.4f")
subtrahend = st.number_input("두 번째 숫자 (감수)", value=0.0, format="%.4f")

if st.button("계산하기"):
    result = minuend - subtrahend
    st.success(f"{minuend} - {subtrahend} = {result}")

st.write("---")
st.markdown(
    "### 사용 예시\n"
    "- 10에서 3을 빼면 7이 됩니다.\n"
    "- 소수도 입력 가능하며 5.5 - 2.25처럼 계산됩니다."
)
