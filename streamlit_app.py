import ast
import re
from decimal import Decimal, InvalidOperation, getcontext
from fractions import Fraction

import streamlit as st

getcontext().prec = 28

st.set_page_config(page_title="혼합 계산기", page_icon="🧮", layout="wide")
st.title("🧮 혼합 계산기")
st.write("혼합 계산, 분수와 소수를 모두 지원하는 스마트 계산기입니다.")


def normalize_mixed_numbers(expression: str) -> str:
    pattern = r"(?P<int>\d+)\s+(?P<num>\d+)/( ?P<den>\d+)"
    return re.sub(
        r"(?P<int>\d+)\s+(?P<num>\d+)/( ?P<den>\d+)",
        lambda m: f"Fraction({int(m.group('int')) * int(m.group('den')) + int(m.group('num'))},{m.group('den')})",
        expression,
    )


def preprocess_expression(expression: str) -> str:
    expression = expression.strip()
    expression = re.sub(r"(?<![\w.])(\d+)\s+(\d+)/(\d+)(?![\w.])", lambda m: f"Fraction({int(m.group(1)) * int(m.group(3)) + int(m.group(2))},{m.group(3)})", expression)
    expression = re.sub(r"(?<![\w.])(\d+)\s*/\s*(\d+)(?![\w.])", r"Fraction(\1,\2)", expression)
    expression = re.sub(r"(?<![\w.])(\d+\.\d+)(?![\w.])", r'Decimal("\1")', expression)
    return expression


def safe_eval(node):
    operators = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Pow: lambda a, b: a ** b,
        ast.USub: lambda a: -a,
        ast.UAdd: lambda a: a,
        ast.Mod: lambda a, b: a % b,
    }

    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op = type(node.op)
        if op not in operators:
            raise ValueError("허용되지 않은 연산입니다.")
        return operators[op](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op = type(node.op)
        if op not in operators:
            raise ValueError("허용되지 않은 연산입니다.")
        return operators[op](operand)
    if isinstance(node, ast.Call):
        func = safe_eval(node.func)
        args = [safe_eval(arg) for arg in node.args]
        if func not in (Fraction, Decimal):
            raise ValueError("허용되지 않은 함수 호출입니다.")
        return func(*args)
    if isinstance(node, ast.Name):
        if node.id == "Fraction":
            return Fraction
        if node.id == "Decimal":
            return Decimal
    raise ValueError("허용되지 않은 표현식입니다.")


def calculate_expression(expression: str):
    if not expression:
        raise ValueError("계산식을 입력해주세요.")

    normalized = preprocess_expression(expression)
    tree = ast.parse(normalized, mode="eval")
    return safe_eval(tree)


def format_fraction(value):
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, Decimal):
        return str(Fraction(value))
    return str(Fraction(value))


def format_decimal(value):
    if isinstance(value, Decimal):
        return str(value.normalize())
    if isinstance(value, Fraction):
        return str(Decimal(value.numerator) / Decimal(value.denominator))
    return str(Decimal(value))


with st.expander("혼합 계산기 사용 방법", expanded=True):
    st.write("- 일반 산술식, 분수, 소수, 혼합 숫자를 모두 입력할 수 있습니다.")
    st.write("- 예: `1/2 + 0.75 * (3 - 1)`, `1 1/2 + 2/3`, `2.5 * 4`, `3/4 / 0.5`")
    st.write("- 결과 형태를 '자동', '분수', '소수' 중 하나로 선택할 수 있습니다.")

expression = st.text_input("계산식 입력", "1/2 + 0.75 * (3 - 1)")
output_type = st.radio("결과 형태 선택", ["자동", "분수", "소수"], index=0)
if st.button("계산하기"):
    try:
        result = calculate_expression(expression)
        if output_type == "분수":
            result_text = format_fraction(result)
        elif output_type == "소수":
            result_text = format_decimal(result)
        else:
            if isinstance(result, Fraction):
                result_text = f"{result} (소수: {format_decimal(result)})"
            elif isinstance(result, Decimal):
                result_text = f"{result} (분수: {format_fraction(result)})"
            else:
                result_text = str(result)

        st.success(f"결과: {result_text}")
    except (ValueError, SyntaxError, ZeroDivisionError, InvalidOperation) as error:
        st.error(f"계산 중 오류가 발생했습니다: {error}")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("분수 계산기")
    frac1 = st.text_input("첫 번째 분수", "3/4")
    frac2 = st.text_input("두 번째 분수", "1/2")
    frac_op = st.selectbox("연산", ["+", "-", "*", "/"])
    if st.button("분수 계산 실행"):
        try:
            expr = f"{frac1} {frac_op} {frac2}"
            result = calculate_expression(expr)
            st.success(f"분수 결과: {format_fraction(result)}")
            st.info(f"소수 결과: {format_decimal(result)}")
        except Exception as error:
            st.error(f"계산 중 오류: {error}")

with col2:
    st.subheader("소수 계산기")
    dec1 = st.text_input("첫 번째 소수", "1.25")
    dec2 = st.text_input("두 번째 소수", "0.5")
    dec_op = st.selectbox("연산", ["+", "-", "*", "/"], index=0, key="decimal_op")
    if st.button("소수 계산 실행"):
        try:
            expr = f"{dec1} {dec_op} {dec2}"
            result = calculate_expression(expr)
            st.success(f"소수 결과: {format_decimal(result)}")
            st.info(f"분수 결과: {format_fraction(result)}")
        except Exception as error:
            st.error(f"계산 중 오류: {error}")
