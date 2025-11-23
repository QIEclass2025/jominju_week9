# ai_logic.py
import google.generativeai as genai
import os
import random

# API Key는 환경변수에서 로드 (보안 필수)
API_KEY = os.environ.get("GEMINI_API_KEY")

def get_best_move(board):
    """
    Gemini API에게 보드 상태를 주고 최적의 수를 받아옵니다.
    """
    # 키가 없으면 랜덤으로 둬서 에러 방지
    if not API_KEY:
        print("!! 경고: GEMINI_API_KEY가 설정되지 않았습니다. 랜덤으로 둡니다.")
        return get_random_move(board)

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # 보드를 보기 좋게 문자열로 변환
        board_str = ""
        for row in board:
            board_str += " ".join(map(str, map(int, row))) + "\n"

        # 프롬프트 수정: 정중하고 명확한 지시문으로 변경
        prompt = f"""
        당신은 오목 게임의 고수 AI입니다. 
        0은 빈칸, 1은 흑돌(상대방), 2는 백돌(당신)입니다.
        현재 당신이 '2'(백돌)를 둘 차례입니다.
        
        [현재 보드 상태]
        {board_str}
        
        규칙:
        1. 이미 돌이 놓인 곳(1 또는 2)에는 절대 착수할 수 없습니다.
        2. 승리할 수 있는 위치 혹은 상대의 공격을 방어하는 최적의 좌표를 계산하십시오.
        3. 답변은 오직 '행,열' 숫자 형식으로만 제공하십시오. (예: 7,7)
        다른 부가 설명은 생략하십시오.
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        y, x = map(int, text.split(','))
        
        # 만약 AI가 이미 둔 곳을 말하면 랜덤 처리
        if board[y][x] != 0:
            return get_random_move(board)
            
        return y, x

    except Exception as e:
        print(f"AI 응답 오류: {e}")
        return get_random_move(board)

def get_random_move(board):
    empty = []
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == 0:
                empty.append((y, x))
    return random.choice(empty) if empty else (0,0)