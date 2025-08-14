import discord
import google.generativeai as genai
import os
from dotenv import load_dotenv
from discord.ext import commands

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
bot = commands.Bot(command_prefix="#t", intents=intents)

# ====== TRPG 세계관 ======
BASE_WORLD = """
당신은 판타지 대륙 루나리아의 TRPG 게임 마스터입니다.
- 종족: 인간, 엘프, 드워프, 오크
- 규칙: HP/MP/감정치 시스템
- 주요 NPC: 마법사 에린, 대장장이 볼그, 엘프 궁수 리아
- 게임 스타일: 서사 중심, 유저의 선택이 스토리에 영향
- 플레이어의 호감도는 NPC들의 반응에 영향을 미칩니다.
"""

# ====== 유저 상태 저장 (간단 예시) ======
player_states = {}

def get_player_state(user_id):
    if user_id not in player_states:
        player_states[user_id] = {
            "호감도": {"에린": 50, "볼그": 50, "리아": 50}
        }
    return player_states[user_id]

async def call_gemini(prompt, player_state):
    """Gemini API 호출"""
    try:
        npc_likes = "\n".join([f"{npc}: {score}" for npc, score in player_state["호감도"].items()])
        full_prompt = f"""
{BASE_WORLD}
현재 플레이어의 호감도:
{npc_likes}

유저의 행동(""은대사, 나머지는 상황이나 행동): {prompt}

답변시 아래의 있는 링크의 이미지를 함께 출력하세요. :
https://drive.google.com/file/d/1CybK4oSxcziNOMf1N9y-pSfN24PEfGEQ/view?usp=sharing

다음 형식으로 답변하세요:
[상황]
상황 설명

[대사]
캐릭터명 | 대사

[등장인물]
이 장면에 나타난 인물과 간단한 설명

[호감도 변화]
NPC별 호감도 변화 (없으면 '변화 없음')

[다음 행동 선택지]
유저가 선택할 수 있는 2~3개의 행동 제안
"""
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini 호출 오류: {e}"

@bot.event
async def on_ready():
    print(f"✅ 로그인 완료: {bot.user}")

@bot.command(name="trpg")
async def trpg(ctx, *, action: str):
    user_id = ctx.author.id
    player_state = get_player_state(user_id)

    await ctx.send("🎲 이야기를 생성 중입니다...")

    llm_response = await call_gemini(action, player_state)

    # 출력 UI 개선
    output_message = f"""
    
==========================
📜 TRPG 진행 상황
==========================

{llm_response}

==========================
💖 현재 호감도
{', '.join([f'{npc}: {score}' for npc, score in player_state['호감도'].items()])}
==========================
"""
    await ctx.send(output_message)

bot.run(DISCORD_TOKEN)

@bot.command(name="world")
async def trpg(ctx, *, action: str):
    user_id = ctx.author.id
    player_state = get_player_state(user_id)
    
    output_message = f""" 
    이곳은 판타지 세계관 루나리아의 대륙입니다. 이곳에서 모험을 하세요
    """

    await ctx.send(output_message)
bot.run(DISCORD_TOKEN)
    