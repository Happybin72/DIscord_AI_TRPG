import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import yt_dlp
import re
import asyncio
import json
from datetime import datetime, timedelta

# ====== 환경 변수 로드 ======
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ====== Gemini API 설정 ======
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ====== 디스코드 봇 설정 ======
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="#t", intents=intents)

# ====== 진격의 거인 캐릭터 설정 ======
AOT_CHARACTERS = {
    "에렌": {"full_name": "에렌 예거", "titan": "진격의 거인", "origin": "시가시나구"},
    "미카사": {"full_name": "미카사 아커만", "titan": None, "origin": "아커만 일족"},
    "아르민": {"full_name": "아르민 아를레르트", "titan": "초대형 거인", "origin": "시가시나구"},
    "리바이": {"full_name": "리바이 아커만", "titan": None, "origin": "지하도시"},
    "한지": {"full_name": "한지 조에", "titan": None, "origin": "조사병단"},
    "에르빈": {"full_name": "에르빈 스미스", "titan": None, "origin": "조사병단"},
    "라이너": {"full_name": "라이너 브라운", "titan": "갑옷거인", "origin": "마레"},
    "베르톨트": {"full_name": "베르톨트 훅버", "titan": "초대형 거인", "origin": "마레"},
    "아니": {"full_name": "아니 레오나르트", "titan": "여성형 거인", "origin": "마레"},
    "지크": {"full_name": "지크 예거", "titan": "짐승거인", "origin": "마레"},
    "히스토리아": {"full_name": "히스토리아 레이스", "titan": None, "origin": "왕가"},
    "장": {"full_name": "장 키르시슈타인", "titan": None, "origin": "훈련병"},
    "코니": {"full_name": "코니 스프링거", "titan": None, "origin": "훈련병"},
    "사샤": {"full_name": "사샤 브라우스", "titan": None, "origin": "훈련병"},
}

# ====== 캐릭터별 이미지 URL 설정 ======
character_emotion_images = {
    "에렌": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Eren_peace.png",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_smile.gif",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_getui.jpg",
        "전투" : "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_move.jpg",
        "거인" : "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_kyozin.jpg",
        "거인_전투" : "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/eren_kyozin_battle.jpg"
    },
    "미카사": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/mikasa_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/mikasa_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/mikasa_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/miksa_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/mikasa_getui.jpg",
        "전투": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/mikasa_battle.jpg"
    },
    "아르민": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/armin_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/armin_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/armin_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/armin_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/armin_getui.jpg"
    },
    "리바이": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/ribai_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/ribai_peace.jpg",
        "전투": "https://github.com/Happybin72/DIscord_AI_TRPG/blob/main/images/ribai_battle.gif",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/ribai_getui.jpg"
    },
    "한지": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_getui.jpg",
        "전투" : "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/hanzi_battle.gif"
    },
        "에르빈": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/erbin_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/erbin_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/erbin_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/erbin_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/erbin_getui.jpg"
    },
        "라이너": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainer_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainer_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainer_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainer_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainer_getui.jpg",
        "거인":"https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/rainet_kyozin.gif",
    },
        "베르톨트": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_getui.jpg",
        "거인":"https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_kyozin.jpg",
        "거인_전투":"https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/bertolt_kyozin_battle.jpg"
    },
        "아니": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_getui.jpg",
        "거인_전투":"https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_kyozin.gif",
        "거인":"https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/annie_kyozin_battle.jpg"
    },
        "지크": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/Assets/images/eren_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/Assets/images/eren_calm.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/Assets/images/eren_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/Assets/images/eren_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/Assets/images/eren_determined.jpg"
    },
        "히스토리아": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Historia%20Reiss_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Historia%20Reiss_peace.png",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Historia%20Reiss_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Historia%20Reiss_getui.jpg"
    },
        "장": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Jean%20Kirstein_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Jean%20Kirstein_peace.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Jean%20Kirstein_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Jean%20Kirstein_getui2.jpg"
    },
        "코니": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Connie%20Springer_angry.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Connie%20Springer_getui.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Connie%20Springer_sad.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Connie%20Springer_getui2.jpg"
    },
        "샤샤": {
        "분노": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Sasha%20Blouse_getui.jpg",
        "평온": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Sasha%20Blouse_peace.jpg",
        "슬픔": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Sasha%20Blouse_sad.jpg",
        "기쁨": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Sasha%20Blouse_happy.jpg",
        "결의": "https://raw.githubusercontent.com/Happybin72/DIscord_AI_TRPG/refs/heads/main/images/Sasha%20Blouse_getui2.jpg"
    },
    # 필요에 따라 다른 캐릭터들도 추가 가능
}

# ====== 분위기별 BGM 설정 ======
atmosphere_music = {
    "전투": "https://youtu.be/vgD48EV7XdA?si=sNsog7jf1sLQ46Tv",
    "평온": "https://youtu.be/BXsjKvdEae4?si=Egu0eCbd-NLuWg3z",
    "긴장": "https://youtu.be/zroFzv7sFis?si=AHK2N8Aanj6Zf85Y", 
    "슬픔": "https://youtu.be/mRdIk4IJa_g?si=1q91ykA3j89n7F4O",
    "희망": "https://youtu.be/_NBqYUAvyx0?si=WG6Rr33TY7_8ZXR0",
    "절망": "https://youtu.be/qLNcTP-JpRw?si=IagabqlhQlYdpc9p",
    "감동": "https://youtu.be/mRdIk4IJa_g?si=1q91ykA3j89n7F4O"
}

# ====== 진격의 거인 세계관 설정 (원본 유지) ======
BASE_WORLD = """
애니메이션 진격의 거인 세계관 기반
##이하의 모든 설정들은 애니메이션 진격의 거인의 기본 설정 위에서 운영되는 TRPG 설정입니다.
세계관 설정
시대적 배경: 845년 시가시나 구 함락 이후 ~ 854년 마레 침공 전까지
주요 무대: 파라디 섬 내 월 마리아, 월 로제, 월 시나, 지하실, 마레 대륙

플레이어는 주인공들의 동기로써 플레이

【중요한 원작 설정 준수 사항】
- 갑옷거인: 라이너 브라운 (마레 전사)
- 초대형 거인: 베르톨트 훅버 → 아르민 (계승)
- 여성형 거인: 아니 레오나르트 (마레 전사)
- 진격의 거인: 에렌 예거 (그리샤로부터 계승)
- 짐승거인: 지크 예거 (에렌의 이복형)
- 전차거인: 피크 (마레)
- 턱거인: 포르코/마르셀 갈리아르드 (마레)
- 워해머 거인: 타이버 가문 (마레)
- 창시거인: 에렌 예거 (왕가 혈통과 접촉 시 발동)

캐릭터 시스템
기본 능력치
- 체력(HP): 0-100 (전투 및 생존력)
- 정신력(MP): 0-100 (입체기동장치 사용, 특수 능력)
- 용기: 0-100 (거인과의 전투 시 패닉 방지)
- 신뢰도: 0-100 (동료들과의 관계, 비밀 공유 가능성)
- 지식: 0-100 (세계의 진실에 대한 이해도)

주요 NPC 및 관계도 시스템
- 에렌 예거 (관계도: 0~100) - 충동적, 열정적, 복수심
- 미카사 아커만 (관계도: 0~100) - 냉정, 보호본능, 에렌 중심적  
- 아르민 아를레르트 (관계도: 0~100) - 지적, 전략적, 평화주의
- 리바이 병장 (관계도: 0~100) - 완벽주의, 현실적, 부하 보호
- 한지 조에 (관계도: 0~100) - 연구광적, 호기심, 거인 애호
- 에르빈 단장 (관계도: 0~100) - 야심적, 희생적, 진실 추구

게임 진행 시스템
주요 스토리 단계
1단계: 신병 훈련 (3-5세션)

목표: 기본 능력 습득, 동기들과 관계 형성
주요 이벤트: 훈련병 순위 결정, 소속 선택
분기점: 톱10 입성 여부에 따른 진로 변화

2단계: 첫 임무와 충격 (5-7세션)

목표: 거인의 공포 경험, 현실 직시
주요 이벤트: 거인과의 첫 접촉, 동료의 죽음
분기점: 전투 참여도, 생존자 구조 선택

3단계: 진실의 편린 (7-10세션)

목표: 세계의 진실에 대한 단서 수집
주요 이벤트: 여성형 거인 전투, 지하실 발견
분기점: 에렌 신뢰 여부, 조사병단 잔류 결정

4단계: 왕정편 음모 (10-13세션)

목표: 내부 적과의 갈등, 정치적 각성
주요 이벤트: 히스토리아 진실, 케니와의 대결
분기점: 혁명 참여도, 평민 vs 귀족 선택

5단계: 지하실의 진실 (13-16세션)

목표: 세계관 전환, 마레와의 갈등 이해
주요 이벤트: 그리샤의 기억, 바다 도달
분기점: 복수 vs 화해 노선 선택

6단계: 최종 결전 준비 (16-20세션)

목표: 마레 침공 또는 평화 협상
주요 이벤트: 시간 건너뛰기, 성장한 캐릭터들
분기점: 전쟁 vs 외교 선택


멀티 엔딩 시스템
A. 자유의 엔딩 (에렌 지지 루트)

조건: 에렌 관계도 80+, 마레 적대 행동
결과: 파라디 섬 완전 독립, 외부 세계와 단절
특징: 자유를 얻었지만 고립된 미래

B. 화해의 엔딩 (아르민 지지 루트)

조건: 아르민 관계도 80+, 외교 선택 다수
결과: 마레와의 평화 협정, 상호 이해
특징: 어려운 공존, 점진적 변화

C. 희생의 엔딩 (에르빈 추종 루트)

조건: 에르빈 관계도 80+, 인류 우선 선택
결과: 거대한 희생으로 얻은 진실 공개
특징: 많은 상실 속에서 얻은 새로운 시작

D. 복수의 엔딩 (리바이 동조 루트)

조건: 리바이 관계도 80+, 전투 우선 선택
결과: 철저한 적 소탕, 힘을 통한 평화
특징: 안정되었지만 경직된 세계

E. 진실의 엔딩 (한지 협력 루트)

조건: 한지 관계도 80+, 연구 우선 선택
결과: 거인의 비밀 완전 해명, 과학적 해결
특징: 기술 발전을 통한 새로운 시대

F. 비극의 엔딩 (실패 루트)

조건: 모든 관계도 낮음, 잘못된 선택 누적
결과: 파라디 섬 멸망, 캐릭터 죽음
특징: 플레이어 선택의 결과에 대한 경고


특별 시스템
기억 계승 시스템

거인의 힘을 얻을 기회 제공
전대 소유자의 기억으로 추가 정보 획득
수명 제한이라는 대가

비밀 정보 네트워크

NPC 신뢰도에 따른 정보 접근
잘못된 정보로 인한 함정 존재
플레이어 간 정보 공유 제한

도덕성 시스템

선택에 따른 도덕성 수치 변화
극단적 선택 시 특별 이벤트 발생
최종 엔딩에 큰 영향

생존 확률 시스템

위험한 선택 시 주사위 굴림
능력치와 장비에 따른 보정
죽음도 스토리의 일부로 인정


게임 마스터 가이드라인
분위기 조성

절망적이면서도 희망적인 톤 유지
플레이어의 선택이 세계에 미치는 영향 강조
원작 존중하되 새로운 가능성 제시

상호작용 원칙

NPC들은 각자의 신념에 따라 행동
플레이어의 행동에 일관성 있게 반응
예상치 못한 결과도 스토리로 연결

세션 운영

-매 세션마다 긴장감 있는 선택 제공
-플레이어 간 토론과 갈등 유도
-원작의 주요 장면을 새로운 관점에서 경험
"""

# ====== 유저 상태 및 BGM 관리 ======
player_states = {}
bgm_states = {}  # BGM 상태 관리

def get_player_state(user_id):
    if user_id not in player_states:
        player_states[user_id] = {
            "호감도": {
                "에렌": 50, "미카사": 50, "아르민": 50, 
                "리바이": 50, "한지": 50, "에르빈": 50
            },
            "능력치": {
                "체력": 100, "정신력": 100, "용기": 50, "신뢰도": 50, "지식": 30
            },
            "진행도": 1,  # 현재 스토리 단계
            "소속": None  # 조사병단, 수비대, 헌병단 등
        }
    return player_states[user_id]

def get_bgm_state(guild_id):
    if guild_id not in bgm_states:
        bgm_states[guild_id] = {
            "current_atmosphere": None,
            "last_changed": None,
            "change_cooldown": timedelta(minutes=3)  # 3분 쿨다운
        }
    return bgm_states[guild_id]

# ====== 캐릭터별 감정 이미지 추출 함수 ======
def extract_character_emotions(response_text):
    """응답에서 캐릭터별 감정을 추출"""
    character_emotions = {}
    
    # [캐릭터 감정] 태그에서 추출하는 패턴
    emotion_pattern = r'\[캐릭터 감정\](.*?)(?=\[|$)'
    emotion_match = re.search(emotion_pattern, response_text, re.DOTALL)
    
    if emotion_match:
        emotion_text = emotion_match.group(1).strip()
        # 각 줄에서 "캐릭터명: 감정" 형태 파싱
        lines = emotion_text.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    char_name = parts[0].strip()
                    emotion = parts[1].strip()
                    
                    # AOT 캐릭터인지 확인
                    if char_name in AOT_CHARACTERS:
                        character_emotions[char_name] = emotion
    
    return character_emotions

def extract_atmosphere(response_text):
    """응답에서 전반적인 분위기 추출"""
    atmosphere_patterns = ["전투", "평온", "긴장", "슬픔", "희망", "절망","감동"]
    
    # [분위기] 태그에서 추출
    atmosphere_match = re.search(r'\[분위기\]\s*(.+)', response_text)
    if atmosphere_match:
        atmosphere_text = atmosphere_match.group(1).strip()
        for pattern in atmosphere_patterns:
            if pattern in atmosphere_text:
                return pattern
    
    # 텍스트 전체에서 분위기 키워드 검색
    for pattern in atmosphere_patterns:
        if pattern in response_text:
            return pattern
    
    return "평온"  # 기본값

def get_character_image(character_name, emotion):
    """캐릭터와 감정에 맞는 이미지 URL 반환"""
    if character_name in character_emotion_images:
        char_images = character_emotion_images[character_name]
        if emotion in char_images:
            return char_images[emotion]
        elif "평온" in char_images:
            return char_images["평온"]  # 기본 이미지
    return None

# ====== 호감도 업데이트 함수 개선 ======
def update_player_stats(response_text, player_state):
    """호감도 및 능력치 업데이트"""
    # 호감도 변화 파싱
    likes_match = re.search(r'\[호감도 변화\](.*?)(?=\[|$)', response_text, re.DOTALL)
    if likes_match:
        likes_text = likes_match.group(1).strip()
        
        for npc in player_state["호감도"].keys():
            npc_pattern = f'{npc}.*?([+-]?\d+)'
            npc_match = re.search(npc_pattern, likes_text)
            if npc_match:
                change = int(npc_match.group(1))
                current = player_state["호감도"][npc]
                player_state["호감도"][npc] = max(0, min(100, current + change))
    
    # 능력치 변화 파싱
    stats_match = re.search(r'\[능력치 변화\](.*?)(?=\[|$)', response_text, re.DOTALL)
    if stats_match:
        stats_text = stats_match.group(1).strip()
        
        for stat in player_state["능력치"].keys():
            stat_pattern = f'{stat}.*?([+-]?\d+)'
            stat_match = re.search(stat_pattern, stats_text)
            if stat_match:
                change = int(stat_match.group(1))
                current = player_state["능력치"][stat]
                player_state["능력치"][stat] = max(0, min(100, current + change))

# ====== Gemini 호출 개선 ======
async def call_gemini(prompt, player_state):
    npc_likes = "\n".join([f"{npc}: {score}" for npc, score in player_state["호감도"].items()])
    abilities = "\n".join([f"{stat}: {value}" for stat, value in player_state["능력치"].items()])
    
    full_prompt = f"""
{BASE_WORLD}

현재 플레이어 상태:
호감도:
{npc_likes}

능력치:
{abilities}

진행도: {player_state.get("진행도", 1)}단계
소속: {player_state.get("소속", "미정")}

유저의 행동: {prompt}

반드시 다음 형식으로 정확히 답변하세요:
[상황]
상황 설명 (원작 설정을 철저히 준수하여 작성)

[대사]
캐릭터명 | 대사 내용

[등장인물]
이 장면에 나타난 인물과 간단한 설명

[캐릭터 감정]
캐릭터명: 감정 (분노, 평온, 슬픔, 기쁨, 결의, 걱정, 냉정, 광기, 사색 등)
(예: 에렌: 분노, 미카사: 걱정)

[분위기]
전투, 평온, 긴장, 슬픔, 희망, 절망 중 하나

[호감도 변화]
NPC별 호감도 변화 (예: 에렌 +5, 미카사 -2, 아르민 변화없음)

[능력치 변화]
능력치 변화가 있다면 기록 (예: 용기 +3, 체력 -5)

[다음 행동 선택지(예시)]
1. 첫 번째 선택지
2. 두 번째 선택지  
3. 세 번째 선택지

주의사항:
- 거인 변신 능력자는 원작 설정을 절대 변경하지 마세요
- 라이너는 갑옷거인, 베르톨트는 초대형 거인(아르민 계승 전), 아니는 여성형 거인입니다
- 에렌은 진격의 거인과 창시거인, 지크는 짐승거인입니다
- 캐릭터들의 성격과 관계는 원작을 따라주세요
"""
    
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API 에러: {e}")
        return "[상황]\n오류가 발생했습니다. 다시 시도해주세요.\n[분위기]\n평온"

# ====== 음악 재생 함수 (BGM 변경 제한 추가) ======
async def play_music_if_needed(voice_client, atmosphere, guild_id):
    """필요한 경우에만 BGM 변경"""
    bgm_state = get_bgm_state(guild_id)
    now = datetime.now()
    
    # 같은 분위기면 변경하지 않음
    if bgm_state["current_atmosphere"] == atmosphere:
        return False
    
    # 쿨다운 체크
    if (bgm_state["last_changed"] and 
        now - bgm_state["last_changed"] < bgm_state["change_cooldown"]):
        return False
    
    # 새로운 BGM 재생
    music_url = atmosphere_music.get(atmosphere)
    if music_url:
        try:
            if voice_client.is_playing():
                voice_client.stop()
                await asyncio.sleep(1)

            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'extractaudio': True,
                'audioformat': 'mp3',
                'quiet': True,
                'no_warnings': True,
            }
            
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(music_url, download=False)
                stream_url = info['url'] if 'url' in info else info['entries'][0]['url']

            source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_options)
            voice_client.play(source)
            
            # BGM 상태 업데이트
            bgm_state["current_atmosphere"] = atmosphere
            bgm_state["last_changed"] = now
            
            return True
        except Exception as e:
            print(f"음악 재생 에러: {e}")
            return False
    
    return False

# ====== TRPG 명령어 대폭 개선 ======
@bot.command(name="trpg")
async def trpg(ctx, *, action: str):
    user_id = ctx.author.id
    guild_id = ctx.guild.id
    player_state = get_player_state(user_id)

    # 로딩 메시지
    loading_msg = await ctx.send("🎲 진격의 거인 세계에서 이야기를 생성 중입니다...")
    
    try:
        # Gemini 호출
        llm_response = await call_gemini(action, player_state)
        
        # 캐릭터별 감정 추출
        character_emotions = extract_character_emotions(llm_response)
        
        # 전반적 분위기 추출
        atmosphere = extract_atmosphere(llm_response)
        
        # 상태 업데이트
        update_player_stats(llm_response, player_state)
        
        # 메인 Embed 생성
        embed = discord.Embed(
            title="⚔️ 진격의 거인 TRPG", 
            description=llm_response, 
            color=0x8B0000  # 진격의 거인 테마 색상 (다크 레드)
        )
        
        # 메인 이미지 설정 (첫 번째 등장 캐릭터의 이미지)
        main_image_set = False
        for char_name, emotion in character_emotions.items():
            image_url = get_character_image(char_name, emotion)
            if image_url and not main_image_set:
                embed.set_image(url=image_url)
                main_image_set = True
                break
        
        # 캐릭터 상태 정보
        likes_info = " | ".join([f"{npc}: {score}" for npc, score in player_state['호감도'].items() if score != 50])
        if likes_info:
            embed.add_field(name="💖 관계 변화", value=likes_info, inline=False)
        
        abilities_info = " | ".join([f"{stat}: {value}" for stat, value in player_state['능력치'].items()])
        embed.add_field(name="📊 현재 능력", value=abilities_info, inline=False)
        
        # 현재 분위기 표시
        embed.add_field(name="🌅 현재 분위기", value=f"{atmosphere}", inline=True)
        
        # 진행 단계 표시
        embed.add_field(name="📈 진행도", value=f"{player_state['진행도']}단계", inline=True)
        
        # 음성 채널에서 BGM 처리
        bgm_changed = False
        if ctx.author.voice:
            try:
                channel = ctx.author.voice.channel
                voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                
                if not voice_client:
                    voice_client = await channel.connect()
                elif not voice_client.is_connected():
                    await voice_client.move_to(channel)
                
                bgm_changed = await play_music_if_needed(voice_client, atmosphere, guild_id)
                
                if bgm_changed:
                    embed.add_field(name="🎵 BGM", value=f"{atmosphere} 테마로 변경", inline=True)
                else:
                    embed.add_field(name="🎵 BGM", value="현재 BGM 유지", inline=True)
                    
            except Exception as e:
                embed.add_field(name="🎵 BGM", value="음성 채널 연결 실패", inline=True)
                print(f"음성 채널 에러: {e}")
        else:
            embed.add_field(name="🔊 BGM", value="음성 채널에 접속해주세요", inline=True)
        
        # 로딩 메시지 업데이트
        await loading_msg.edit(content=None, embed=embed)
        
        # 캐릭터별 감정 이미지를 추가 메시지로 전송 (제한적으로)
        additional_images = []
        for char_name, emotion in list(character_emotions.items())[1:2]:  # 최대 1개 추가 이미지
            image_url = get_character_image(char_name, emotion)
            if image_url:
                additional_images.append((char_name, emotion, image_url))
        
        for char_name, emotion, image_url in additional_images:
            char_embed = discord.Embed(
                title=f"{char_name}의 감정: {emotion}",
                color=0x4A4A4A
            )
            char_embed.set_image(url=image_url)
            await ctx.send(embed=char_embed)
            await asyncio.sleep(0.5)  # 스팸 방지
            
    except Exception as e:
        await loading_msg.edit(content=f"❌ 오류가 발생했습니다: {str(e)}")
        print(f"TRPG 명령어 에러: {e}")

# ====== 캐릭터 정보 확인 명령어 ======
@bot.command(name="char")
async def character_info(ctx, character_name: str = None):
    if not character_name:
        char_list = ", ".join(AOT_CHARACTERS.keys())
        await ctx.send(f"📋 사용 가능한 캐릭터: {char_list}")
        return
    
    if character_name in AOT_CHARACTERS:
        char_info = AOT_CHARACTERS[character_name]
        embed = discord.Embed(
            title=f"👤 {char_info['full_name']}",
            color=0x8B0000
        )
        
        embed.add_field(name="🏠 출신", value=char_info['origin'], inline=True)
        if char_info['titan']:
            embed.add_field(name="👹 거인화 능력", value=char_info['titan'], inline=True)
        else:
            embed.add_field(name="👹 거인화 능력", value="없음", inline=True)
            
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ 존재하지 않는 캐릭터입니다.")

# ====== 상태 확인 명령어 개선 ======
@bot.command(name="status")
async def check_status(ctx):
    user_id = ctx.author.id
    player_state = get_player_state(user_id)
    
    embed = discord.Embed(title="📊 플레이어 상태", color=0x8B0000)
    
    # 호감도 정보
    likes_info = "\n".join([f"{npc}: {score}/100" for npc, score in player_state['호감도'].items()])
    embed.add_field(name="💖 NPC 호감도", value=likes_info, inline=False)
    
    # 능력치 정보
    abilities_info = "\n".join([f"{stat}: {value}/100" for stat, value in player_state['능력치'].items()])
    embed.add_field(name="⚡ 능력치", value=abilities_info, inline=False)
    
    # 진행 정보
    embed.add_field(name="📈 현재 진행도", value=f"{player_state['진행도']}단계", inline=True)
    embed.add_field(name="🏢 소속", value=player_state.get('소속', '미정'), inline=True)
    
    await ctx.send(embed=embed)
                       
# ====== 음성 채널 나가기 명령어 ======
@bot.command(name="leave")
async def leave_voice(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("👋 음성 채널에서 나갔습니다.")
    else:
        await ctx.send("❌ 음성 채널에 연결되어 있지 않습니다.")
                       

# ====== 봇 이벤트 ======
@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")
    print(f"📁 서버 수: {len(bot.guilds)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ 알 수 없는 명령어입니다. `#ttrpg`를 사용해보세요.")
    else:
        await ctx.send(f"❌ 오류 발생: {str(error)}")
        print(f"명령어 에러: {error}")

# ====== 봇 실행 ======
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)