import random
import operator

# 四則演算関数
ops = {
    "+": operator.add,
    "-": operator.sub,
    "×": operator.mul,
    "÷": operator.truediv,
}

def normalize_input(s):
    """入力文字列を正規化する"""
    return s.translate(str.maketrans("０１２３４５６７８９", "0123456789"))

def generate_problem(num_terms, min_digits, max_digits, operator_choice):
    """問題を生成する"""
    digits = []
    for _ in range(num_terms):
        d = random.randint(min_digits, max_digits)
        digits.append(random.randint(10 ** (d - 1), 10 ** d - 1))

    if operator_choice == "÷":
        result = digits[0]
        for i in range(1, len(digits)):
            d = random.randint(min_digits, max_digits)
            divisor = random.randint(10 ** (d - 1), 10 ** d - 1)
            result *= divisor
            digits[i] = divisor
        digits[0] = result

    return digits

def calculate_result(problems, operator):
    """計算結果を求める"""
    result = problems[0]
    for n in problems[1:]:
        try:
            result = ops[operator](result, n)
        except ZeroDivisionError:
            return float("inf")
    return result

def check_answer(user_answer, problems, operator):
    """答え合わせを行う"""
    try:
        user_answer = float(user_answer)
        result = calculate_result(problems, operator)
        return abs(user_answer - result) < 0.01, result
    except ValueError:
        return None, None

def generate_sequence(length, min_num=1, max_num=9):
    """連続して同じ数字が来ないように数字列を生成する"""
    sequence = []
    last_num = None
    
    for _ in range(length):
        available_nums = [n for n in range(min_num, max_num + 1) if n != last_num]
        num = random.choice(available_nums)
        sequence.append(num)
        last_num = num
    
    return sequence

def check_sequence(user_sequence, correct_sequence):
    """ユーザーの入力と正解を比較する"""
    if len(user_sequence) != len(correct_sequence):
        return False
    
    return all(u == c for u, c in zip(user_sequence, correct_sequence)) 