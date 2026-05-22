import streamlit as st

st.title("나눗셈 계산기")
st.write("두 수를 입력하면 나눗셈 결과를 계산해줍니다.")

dividend = st.number_input("첫 번째 숫자 (분자)", value=1.0, format="%.4f")
divisor = st.number_input("두 번째 숫자 (분모)", value=1.0, format="%.4f")

if st.button("계산하기"):
    if divisor == 0:
        st.error("0으로 나눌 수 없습니다. 다른 값을 입력해주세요.")
    else:
        result = dividend / divisor
        st.success(f"{dividend} ÷ {divisor} = {result}")

st.write("---")
st.markdown(
    "### 사용 예시\n"
    "- 10을 2로 나누면 5가 됩니다.\n"
    "- 소수도 입력 가능하며 5.5 ÷ 2.2처럼 계산됩니다."
)
