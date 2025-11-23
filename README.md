\# Omok Game (Gemini Ver.)



\## 프로젝트 소개

본 프로젝트는 Gemini API를 활용하여 AI 대전 기능을 구현한 오목 게임이다.

기존 과제에서 피드백을 반영하여 1인용 플레이 모드를 추가하고, 게임의 몰입도를 높이기 위해 효과음 기능을 도입하였다.



\## 개발 환경 및 도구

\- 언어: Python 3.12+

\- 패키지 관리: uv

\- 주요 라이브러리: pygame, numpy, google-generativeai



\## 실행 방법 (How to Run)

본 프로젝트는 uv를 통해 의존성을 관리하므로, 아래 절차를 따라 실행한다.



1\. 레포지토리 클론 및 의존성 설치

&nbsp;  git clone <레포지토리 주소>

&nbsp;  uv sync



2\. 환경 변수 설정 (API Key)

&nbsp;  Gemini API 사용을 위해 환경 변수 설정이 필수적이다.

&nbsp;  - Windows (PowerShell): $Env:GEMINI\_API\_KEY = "발급받은키"

&nbsp;  - Mac/Linux: export GEMINI\_API\_KEY="발급받은키"



3\. 게임 실행

&nbsp;  uv run omok\_game.py



\## 주요 개선 사항

1\. Gemini AI 연동 1인용 모드

&nbsp;  - 기존의 2인용 로직에 Google Gemini API를 연동하여 1인용 대전 모드를 구현함.

&nbsp;  - 단순 알고리즘이 아닌 LLM이 현재 보드 상태를 분석하여 착수 위치를 결정함.



2\. 효과음(Sound Effect) 추가

&nbsp;  - 돌 착수 시 청각적 피드백을 제공하여 게임 경험을 개선함.



3\. 프로젝트 구조 개선

&nbsp;  - uv 및 pyproject.toml을 도입하여 재현 가능한 개발 환경을 구성함.

