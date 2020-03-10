#-*- coding: utf-8 -*-

import discord
from discord.utils import get
import openpyxl
import asyncio
import random
import datetime
import os, sys
import time
import string
import math
import requests
import sqlite3
import json
from bs4 import BeautifulSoup
from googletrans import Translator
from selenium import webdriver

conn = sqlite3.connect("C:\\Users\\Administrator\\Desktop\\Game\\Python\\discordpy.db")
cur = conn.cursor()
client = discord.Client()
customcommand = []
ban = []
bbanegiwihangut = []
json_data = {}
with open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\discord.json", "r") as j:
    json_data = json.load(j)
    TOKEN = json_data['token']

for i in range(1, 201):
    cur.execute("select question from command")
    rows = cur.fetchall()
    for row in rows:
        customcommand.append(row[0])
        bbanegiwihangut.append(row)

for i in range(1,501):
    cur.execute("select discordID from Block")
    rows = cur.fetchall()
    for row in rows:
        ban.append(row[0])
        bbanegiwihangut.append(row)

@client.event
async def on_ready():
    print("\n┌" + "─" * 54 + "┐")
    print(f"│{client.user.name + ' online':^50}│")
    print(f"│{client.user.id:^50}    │")
    print("└" + "─" * 54 + "┘")
    servers = list(client.guilds)
    Users = list(client.users)
    games = ["닉줘야 도움 혹은 닉도를 입력해 명령어를 확인해!", "문의는 nickgive#5842 로!", "닉줘야 직업 직업이름 으로 닉줘야 시대를 체험해봐!",
            "닉줘야 시대 지금 알파 테스트중", str(len(servers)) + "개의 서버에 참여중", str(len(Users)) + "명의 사람과 함께 "]
    whatgame = random.randint(0,5)
    while True:
        game = discord.Game(games[whatgame])
        if whatgame == 5:
            whatgame = 0
        else: 
            whatgame += 1 
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)

@client.event
async def on_message(message):
    mos = message.content.startswith
    con = message.content
    chs = message.channel.send
    com = ["안녕!", "죽어라", "사망", "닉줘야를 시체로 결정", "샌즈", "야인시대", "사진", "치킨",
    "말배워", "말해", "공장초기화", "공초", "닉공초", "빌보드", "메타크리틱", "코로나", "핑", "닉핑", "프로필",
    "나무위키", "꺼무위키", "위키피디아", "위키백과", "Hello,World!","직업","보스","아이템","상점","글자뒤집기"]
    ie = ["C", "E", "G", "I", "K", "M", "O", "Q", "S", "U", "W", "Y"]
    hie = ["D", "F", "H", "J", "L", "N", "P", "R", "T", "V", "X", "Z"]
    global customcommand
    subcom = con.split(" ")
    now = datetime.datetime.now()

    def level_up(i, embed):
        cur.execute("""update nickga`me set exp = 0, "level" = "level" + 1,
	    damage = case 
            when job = '매지션' then damage * 1.15
		    else damage * 1.1
		    end,
	    maxHP = CASE
		    when job = '워리어' then maxHP * 1.3
		    else maxHP * 1.2
		    end,
	    maxMP = CASE
		    when job = '매지션' then maxMP * 1.3
		    else maxMP * 1.2
		    end,
	    avoid = CASE
		    when job = '아처' then avoid + 0.05
		    else avoid + 0.01
		    end,
	    defence = case
		    when job = '워리어' then defence + 2
		    else defence + 1
		    end,
	    maxexp = case
            when "level" <= 20 then maxexp * 1.2
            when "level" <= 50 and "level" > 20 then maxexp * 1.5
            when "level" <= 100 and "level" > 50 then maxexp * 1.8
            when "level" <= 200 and "level" > 100 then maxexp * 2
		    end
	    where discordID = ?""",(i[0],))
        cur.execute("update nickgame set HP = maxHP, MP = maxMP where discordID = ?", (i[0],))
        cur.execute("select * from nickgame where discordID = ?",(i[0],))
        row = cur.fetchall()[0]
        conn.commit()
        embed.add_field(name = "레벨업!", value = "Level up! {}님이 레벨 {}으로 레벨업 하셨습니다! \n 공/마 + {}% , HP + {}% MP + {}%, 회피율 + {}% , 방어력 + {}".format(i[1], row[3], row[9], row[6], row[10], row[8], row[11]), inline = False)
        return embed

    def item_get_def(item_get_percentage, how_many, play, what_item, embed, middle_percentage = None, how_many2 = None):
        cur.execute("select many from '{}' where item = ?".format(message.author.id), (what_item,))
        try:
            hom = cur.fetchall()[0][0]
        except:
            hom = 0
        if middle_percentage == None:
            cur.execute("insert or replace into '{}' (item, many) values (?, ?)".format(message.author.id), (what_item, hom + how_many))
            embed.add_field(name = "흭득!", value = "{}님이 {}(을)를 {}개 흭득하셨습니다!".format(play[1], what_item, how_many))
        else:
            if item_get_percentage >= middle_percentage:
                cur.execute("insert or replace into '{}' (item, many) values (?, ?)".format(message.author.id), (what_item, hom + how_many))
                embed.add_field(name = "흭득!", value = "{}님이 {}(을)를 {}개 흭득하셨습니다!".format(play[1], what_item, how_many))
            if item_get_percentage < middle_percentage:
                cur.execute("insert or replace into '{}' (item, many) values (?, ?)".format(message.author.id), (what_item, hom + how_many2))
                embed.add_field(name = "흭득!", value = "{}님이 {}(을)를 {}개 흭득하셨습니다!".format(play[1], what_item, how_many2))
        conn.commit()
        return embed
                                            
    def item_buy(what_item, how_many, how_much, embed, cur = cur, conn = conn):
        cur.execute("select many from '{}' where item = ?".format(message.author.id), (what_item,))
        try:
            hom = cur.fetchall()[0][0]
        except:
            hom = 0
        cur.execute("select money from nickgame where discordID = ?", (message.author.id,))
        if cur.fetchall()[0][0] < how_much:
            embed.add_field(name = "돈부족!", value = "{0}님의 돈이 모자랍니다. 그래서 못샀어요!".format(message.author.name))
            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/684698409701343232/asdf.png")
            return embed
        cur.execute("insert or replace into '{}' (item, many) values (?, ?)".format(message.author.id), (what_item, hom + how_many))
        cur.execute("update nickgame set money = money - ? where discordID = ?",(how_much,message.author.id))
        conn.commit()
        cur.execute("select nickname from nickgame where discordID = ?", (message.author.id,))
        embed.add_field(name = "구매!", value = cur.fetchall()[0][0] + "님이 HP포션 {0}개를 구매 하셨어요! 비용 :{1}원".format(how_many,how_much))
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/680292100562354189/669f6a624bc98f2a.png")
        return embed

    if message.author.bot:
        return None

    if message.author.id in ban:
        if mos("닉줘야"):
            await chs("응 너 차단당함 ㅅㄱ")
            return None

    if mos("닉줘야 차단"):
        if message.author.id == 488177920066715659:
            try:
                if subcom[2] == "추가":
                    sql = "INSERT INTO Block(discordName, discordID) VALUES (?,?)"
                    cur.execute(sql, (message.mentions[0].name, message.mentions[0].id))
                    conn.commit()
                    ban.append(int(message.mentions[0].id))
                    await chs(str(message.mentions[0]) + "님을 차단했습니다! ^^")
                if subcom[2] == "제거" or subcom[2] == "해제":
                    sql = "DELETE FROM Block WHERE discordID = ?"
                    cur.execute(sql, (message.mentions[0].id,))
                    conn.commit()
                    ban.remove(int(message.mentions[0].id))
                    await chs(str(message.mentions[0]) + "님의 차단을 해제했습니다! ^^")
            except IndexError:
                await chs("아니 개발자 조차도 커맨드 자체를 까먹으면 어떻카냐")
        else:
            await chs("응 개발자 아니면 차단 못해^^ 꼬우면 해킹하든가~")

    if mos("닉줘야 오프라인"):
        if message.author.id == 488177920066715659:
            await chs("닉줘야봇을 오프라인 합니다. 안녕히주무ㅅ...zzzz")
            sys.exit()
        else:
            await chs("응 개발자 아니면 차단 못해^^ 꼬우면 해킹하든가~")

    if mos("닉줘야 재부팅"):
        if message.author.id == 488177920066715659:
            await chs("재부팅을 시작합니다. 10초 자고 와야지^^")
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            await chs("응 개발자 아니면 차단 못해^^ 꼬우면 해킹하든가~")


    if mos("닉줘야 도움") or mos("닉도"): # 도움말
        embed = discord.Embed(title="닉줘야 도움말",description="닉줘야 (명령어) 로 사용가능합니다. 때론 닉줘야 대신 다르게 나올수 있음." ,color=discord.Colour.green())

        embed.add_field(name="대화 명령어", value="안녕!, 낙줘, (뒤에 커맨드 안붙임), 엿, 어휴, 에휴, 왜살아, 탈모르파티, 너 고소", inline=False)
        embed.add_field(name="사진, 짤 명령어", value="죽어라, 사망, 닉줘야를 시체로 결정, 샌즈, 야인시대, 사진 (사진 URL), 치킨", inline=False)
        embed.add_field(name="커스텀 명령어, 말하기, 삭제", value="말해 (말할 내용), 말배워 (질문)/(대답), (앞서 만든 질문), 공장초기화, 공초, 닉공초, 글자뒤집기, 초기화 (초기화할 질문), 커맨드조회, 메시지삭제", inline=False)
        embed.add_field(name="웹 크롤링", value="빌보드, 메타크리틱, 코로나", inline=True)
        embed.add_field(name="핑, 닉핑", value="퐁! 현재 핑 측정", inline=True)
        embed.add_field(name="프로필", value="프로필이 뜹니다", inline=True)
        embed.add_field(name="위키", value="나무위키, 꺼무위키, 위키피디아, 위키백과", inline=True)
        embed.add_field(name="Hello,World! (언어)", value="각 언어별 Hello, world!를 출력하는법을 띄웁니다", inline=True)
        embed.add_field(name="닉줘야 시대", value="직업, 보스, 아이템, 상점", inline=False)
        embed.add_field(name="닉줘야봇 개발자만 가능한거^^", value="차단, 오프라인, 재부팅")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed=embed)

    if mos("닉줘야 안녕!"): # 인사
        await chs("안녕! 나는 닉줘야봇이야!")

    if mos("닉줘야 닉줘"):
        await chs("뭐임마. 말을 제대로 해보쇼!")
    
    if message.content == "닉줘야":
        await chs("말했으면 말해 어? 뭐 말할지 모르겠으면 닉줘야 도움 써서 보든가")

    if mos("닉줘야 엿"):
        await chs("{}을 엿바꿔 먹어야지 ㅎㅎ".format(message.author.name))
    
    if mos("닉줘야 어휴") or mos("닉줘야 에휴"):
        await chs("어휴 봇에게 까지 그러는 니 인생이 **LEGENO**다 에ㅔㅔㅔㅔㅔ휴우ㅜ우우")
    
    if mos("닉줘야 왜살아"):
        await chs("그건 니가 알바 아닌데? 니 인생부터 **제대로** 살아보지 그래?")

    if mos("닉줘야 탈모르파티"):
        await chs("민머리 대머리 맨들맨들 빡빡이\nㅁㅁㄹ ㄷㅁㄹ ㅁㄷㅁㄷ ㅃㅃㅇ")

    if mos("닉줘야 너 고소"):
        await chs("판사님 전 봇입니다. 따라서 무생명체 이므로 잡아 넣을수 없을 것입니다. 네? 프로그램을 파괴 하라고요? ㅎㅎㅎㅎ 프로그래머가 백업하겠죠")

    if mos("닉줘야 사진"):
        embed = discord.Embed(color=discord.Colour.green())
        

        embed.set_image(url = subcom[2])
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await message.channel.purge(limit=1)
        await chs(embed=embed)

    if mos("닉줘야 죽어라") or mos("닉줘야 사망") or mos("닉줘야를 시체로 결정"):
        embed = discord.Embed(color=discord.Colour.green())

        embed.set_image(url="https://cdn.discordapp.com/attachments/669725992050229259/671246742490185738/528c60ed68a7186b.PNG")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        
        await chs(embed=embed)

    if mos("닉줘야 샌즈"):
        embed = discord.Embed(color=discord.Colour.green())

        embed.set_image(url="https://cdn.discordapp.com/attachments/507133558452912129/671298890406035466/9779f7a19091794b.png")
        embed.add_field(name = "~~와!~~", value = "~~샌즈 아시는구나! 겁.나.어.렵.습.니.다~~")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed=embed)

    if mos("닉줘야 야인시대"):
        
        image = ["http://i.imgur.com/DHshyTY.gif", "https://img2.quasarzone.co.kr/web/qn_hardware/1909/1909obj___1864774007.gif","https://thumbs.gfycat.com/WarpedLimitedAmmonite-size_restricted.gif", "https://app.jjalbang.today/action/jjalbang_download.php?cnum=1JY",
                 "https://media1.tenor.com/images/0d215c66fcc981633a1ea0dd5bcc8d3d/tenor.gif", "https://file3.instiz.net/data/file3/2019/02/23/a/9/f/a9f9d694ac2a60bb0c1b401c00f54fa9.gif","https://img.danawa.com/images/descFiles/5/74/4073992_1574302735894.gif", "https://cdn.ppomppu.co.kr/zboard/data3/2018/0528/1527512037_2249_3f95d4cd65c6cafe66527ad5d827f433.gif",
                 "https://cdn.discordapp.com/attachments/668376970358292493/668390908550447124/KakaoTalk_20200119_184548042.gif", "https://thumbs.gfycat.com/TangibleEntireImperatorangel-small.gif", "https://img.chuing.net/i/QeJQpNe/1.gif","https://media.tenor.com/images/da3ca2f1fb46a9a76b20b13500236614/tenor.gif","https://media.tenor.com/images/e52b598cdfa956ef36a994f150117a28/tenor.gif"]
        msg = ["내가 고자라니!", "님은 바로 사회주의 낙원을 말하는 것입니다 여러분!!!!", "XX를 만들어 주마", "개소리 집어쳐! 무슨님을 만난다는 거야!", "두한아! 일어나거라 어서! 상대는 공산당이다!", "중공군이라고? 어림도 없다! 아아암! 아아아ㅏ아아아암!",
               "1972년 11월 21일 김두한은 쓰러졌다.", "똥이나 처먹어 이XX들아!", "폭★8", "안되겠소 쏩시다!", "다음에 걸리면 죽을줄 알아?! 알겠어?!?!?!","All right! Four dollars!", "4딸라."]
        num = random.randint(0,12)
        embed = discord.Embed(title = msg[num],color=discord.Colour.green())
        embed.set_image(url=image[num])
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed=embed)

    if mos("닉줘야 치킨") or mos("ㄴ치"):
        embed = discord.Embed(title = "치느님을 영접해라", color = 0xFFFF00)
        chicken = ["https://economychosun.com/query/upload/303/20190608214338_gubchoja.jpg","https://t1.daumcdn.net/liveboard/interbiz/724b01edcbeb44dfa3fe10a3dbbda51f.JPG", "https://pds.joins.com/news/component/htmlphoto_mmdata/201903/08/52cf07ea-c8da-4574-b0e9-21e0e3b31118.jpg"
                   , "https://www.mpps.co.kr/kfcs_api_img/KFCS/goods/DL_2173537_20191205104235710.png"]
        embed.set_image(url = chicken[random.randint(0,3)])
        embed.set_footer(icon_url = message.author.avatar_url, text = "치킨 먹고 싶은 이 : {0} , 치킨 땡기는 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed = embed)

    if mos("닉줘야 말해"): # 뒤에있는 말을 말함
        if con[6:7] == " ":
            await message.channel.purge(limit=1)
            await chs(con[7:])
        else:
            await chs("올바른 사용법:닉줘야 말해 (말할내용)")

    if mos("닉줘야 글자뒤집기"):
        if con[9:10] == ' ':
            await chs(con[:9:-1])
        else:
            await chs("올바른 사용법:닉줘야 글자뒤집기 (말할내용)")

    if mos("닉줘야 말배워"): # 커맨드 만들기
        learn = con[8:].split("/")
        sql = "insert into command(question,answer) values (?, ?)"
        if learn[0] in com or learn[0] in customcommand:
            await chs("이미 있는 명령어는 추가할 수 없습니다.")
        else:
            cur.execute(sql, (learn[0], learn[1]))
            conn.commit()
            msg = await chs("질문 및 대답을 다운받는중...")
            await msg.edit(content="※다운 완료.※")
            customcommand.append(learn[0])

    if mos("닉줘야") and con[4:] in customcommand: # 대답한다
        sql = "select answer from command where question=?"
        cur.execute(sql, (con[4:],))
        await chs(cur.fetchall()[0][0])

    if mos("닉줘야 공장초기화") or mos("닉줘야 공초") or mos("닉공초"): # 공장초기화
        sql = "delete from command"
        cur.execute(sql)
        conn.commit()
        customcommand = []
        await chs("공장초기화 완료! 너네 누구냐")

    if mos("닉줘야 커맨드조회"):
        sql = "select * from command"
        embed = discord.Embed(title = "닉줘야봇 내에 있는 커스텀커맨드", color = 0xfd58d8)
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            embed.add_field(name = row[1], value = row[2], inline = False)
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)

    if mos("닉줘야 초기화"):
        sql = "delete from command where question = ?"
        subcom = con[8:]
        cur.execute(sql,(subcom,))
        conn.commit()
        await chs("선택하신 커맨드가 초기화되었습니다 ㅊㅋㅊㅋ")

    if mos("닉줘야 프로필"):
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        join = str(message.author.joined_at)
        join_as = join[:10].split("-")
        join_time = join[10:].split(":")
        join_date = join_as[0] +"년 "+ join_as[1] + "월 " + join[2] + "일 " + join_time[0] +"시 " + join_time[1] + "분 " +str(int(float(join_time[2]))) + "초"
        roles = [role for role in message.author.roles]
        status = None
        if message.author.status == discord.Status.online:
            status = "온라인"
        elif message.author.status == discord.Status.offline:
            status = "오프라인"
        elif message.author.status == discord.Status.idle:
            status = "자리 비움"
        elif message.author.status == discord.Status.dnd:
            status = "다른 용무 중"
        embed = discord.Embed(color = 0x00d4ff)
        embed.add_field(name = "이름", value = message.author.name + "#" +message.author.discriminator, inline = True)
        embed.add_field(name = "서버별명", value = message.author.display_name, inline = True)
        embed.add_field(name = "가입일", value = str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline = True)
        embed.add_field(name = "이 서버 들어온 날짜", value = join_date, inline = False)
        embed.add_field(name = "아이디", value = message.author.id, inline = False)
        embed.add_field(name = "가진 역할들", value = ", ".join([role.mention for role in roles]), inline = False)
        embed.add_field(name = "상태",value=status,inline=False)
        embed.set_thumbnail(url = message.author.avatar_url)
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)

    if mos("닉줘야 니정보"):
        date = datetime.datetime.utcfromtimestamp(((int(client.user.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(title="닉줘야 봇의 정보",color = 0x00d4ff)
        embed.add_field(name = "이름", value = client.user.name, inline = True)
        embed.add_field(name = "서버이름", value = client.user.display_name, inline = True)
        embed.add_field(name = "가입일", value = str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline = True)
        embed.add_field(name = "아이디", value = client.user.id, inline = True)
        embed.set_thumbnail(url = client.user.avatar_url)
        embed.set_footer(icon_url = client.user.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(client.user.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)

    if mos("닉줘야 핑") or mos("닉핑"):
        embed = discord.Embed(title = "퐁!", color = 0xff3399)
        image = ["https://image.fmkorea.com/files/attach/new/20160813/486616/169950/436635830/bed6cac34077fe6bebd5c011faf3493d.jpg","https://media0.giphy.com/media/l41m3ywjOxm9SzAhG/giphy.webp?cid=790b7611ed4e3e6c316fb1e65194c0fc26ded2991de6ca38&rid=giphy.webp",
                 "https://i.ytimg.com/vi/TrezFjGF-Kg/maxresdefault.jpg"]
        ping = round(client.latency * 1000)
        embed.add_field(name = client.user.name + "님의 핑은...", value = "{0} ms (0.{1}초)".format(ping, ping), inline = False)
        embed.set_thumbnail(url = image[random.randint(0,2)])
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed = embed)

    if mos("닉줘야 Hello,World!"):
        embed = discord.Embed(title = subcom[2] + "(으)로 Hello, World! 출력하는법", color = 0x3EB489)
        if subcom[2] == "LabVIEW":
            embed.set_image(url = "https://w.namu.la/s/40421e0e97325a784f39e04ba747859eff5d35f66bc081a5573fe3674cad1ed4ed62b90e7052825dea045076600e64cf6545a538e6c247d5fc313920d215028f74e82f03a00f76c94c2d3d337d06a0a7969eed57f53305a98b34c4d4345d3eec")
        elif subcom[2] == "스크래치" or subcom[2] ==  "엔트리":
            embed.set_image(url = "https://w.namu.la/s/639df83516b3c9f7d5310d32726341e429edd0f17474f4120e4c040a8ba7893cf258bc8871b375fd5a998a09937a753291fdbc917fe7d7ff1c6f28f7e44880e024e0d9e68e8754a8f4016e3a9554efbc0f18be203f3f48566c8d2c2f763076b6")
            embed.add_field(name = "왜 둘다 똑같은 사진 쓰는 이유", value = "어짜피 코딩 방법이 같아서 스크래치 사진 같이씀")
        else:
            f = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\Hello, World!\\" + subcom[2] + ".txt", 'r', encoding='UTF-8')
            if subcom[2] == "DNA#" or subcom[2] == "셰익스피어":
                f = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\Hello, World!\\" + subcom[2] + ".txt", 'r', encoding='UTF-8')
                f1 = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\Hello, World!\\" + subcom[2] + "-2.txt", 'r', encoding='UTF-8')
                if subcom[2] == "셰익스피어":
                    f2 = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\Hello, World!\\" + subcom[2] + "-3.txt", 'r', encoding='UTF-8')
            data = f.read()
            if subcom[2] == "DNA#" or subcom[2] == "셰익스피어":
                data1 = f1.read()
                if subcom[2] == "셰익스피어":
                    data2 = f2.read()
            embed.add_field(name = subcom[2], value = data)
            if subcom[2] == "DNA#" or subcom[2] == "셰익스피어":
                embed1 = discord.Embed(title = subcom[2] + "(으)로 Hello, World! 출력하는법 - 2", color = 0x3EB489)
                embed1.add_field(name = subcom[2], value = data1)
                embed1.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분\n출처:꺼무위키 나라".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                if subcom[2] == "셰익스피어":
                    embed2 = discord.Embed(title = subcom[2] + "(으)로 Hello, World! 출력하는법 - 3", color = 0x3EB489)
                    embed2.add_field(name = subcom[2], value = data2)
                    embed2.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분\n출처:꺼무위키 나라".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분\n출처:꺼무위키 나라".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)
        if subcom[2] == "DNA#" or subcom[2] == "셰익스피어":
            await chs(embed = embed1)
            if subcom[2] == "셰익스피어":
                await chs(embed = embed2)

    if mos("닉줘야 계산"):
        try:
            if subcom[3] == "+":
                answer = float(subcom[2]) + float(subcom[4])
            elif subcom[3] == "-":
                answer = float(subcom[2]) - float(subcom[4])
            elif subcom[3] == "*":
                answer = float(subcom[2]) * float(subcom[4])
            elif subcom[3] == "^":
                answer = float(subcom[2]) ** float(subcom[4])
            elif subcom[3] == "/":
                try:
                    if subcom[5] == "몫":
                        answer = float(subcom[2]) // float(subcom[4])
                    elif subcom[5] == "나머지":
                        answer = float(subcom[2]) % float(subcom[4])
                except IndexError:
                    answer = float(subcom[2]) / float(subcom[4])
            embed = discord.Embed(title = "닉줘야 봇 계산 완료!",color = 0xfffafa)
            embed.add_field(name = "{0} 의 값".format(con[7:]), value = con[7:] + "의 값은 %s입니다." % answer)
            embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            embed.set_thumbnail(url = "https://post-phinf.pstatic.net/MjAxNzEyMTJfMTI3/MDAxNTEzMDYzOTgwMjQ2.VNo-xWE1lMVsXbxWhlH9kKjybgqBqh9tsuM8z7EwOEYg.bwcpk1CSH9gVCk0o0Wgb5DipQ3WUNbkdK8boCo5lOusg.PNG/%EC%88%98%ED%95%99%EA%B3%B5%EB%B6%803.PNG?type=w1200")
            await chs(embed = embed)
        except:
            try:
                if subcom[2] == "루트":
                    answer = math.sqrt(float(subcom[3]))
                elif subcom[2] == "탄젠트":
                    answer = math.tan(math.radians(float(subcom[3])))
                    if subcom[3] == "90":
                        answer = "값을 정할수 없습니다."
                elif subcom[2] == "사인":
                    answer = math.sin(math.radians(float(subcom[3])))
                elif subcom[2] == "코사인":
                    answer = math.cos(math.radians(float(subcom[3])))
                elif message.content[-1] == "!":
                    answer = math.factorial(float(message.content[7:-1]))
                if answer == "값을 정할수 없습니다.":
                    embed = discord.Embed(title = "계산오류!",color = 0xfffafa)
                    embed.add_field(name = "계산오류", value = "탄젠트 90도는 정할수 없습니다.")
                else:
                    embed = discord.Embed(title = "닉줘야 봇 계산 완료!",color = 0xfffafa)
                    embed.add_field(name = "{0} 의 값".format(con[7:]), value = con[7:] + "의 값은 %s입니다." % answer)
                embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                embed.set_thumbnail(url = "https://post-phinf.pstatic.net/MjAxNzEyMTJfMTI3/MDAxNTEzMDYzOTgwMjQ2.VNo-xWE1lMVsXbxWhlH9kKjybgqBqh9tsuM8z7EwOEYg.bwcpk1CSH9gVCk0o0Wgb5DipQ3WUNbkdK8boCo5lOusg.PNG/%EC%88%98%ED%95%99%EA%B3%B5%EB%B6%803.PNG?type=w1200")
                await chs(embed = embed)
            except:
                embed = discord.Embed(title = "으악! 오류났다!", color = 0x00f0f0)
                embed.add_field(name = "닉줘야 봇 오류", value = "올바른 사용법 : (첫 번쨰 값) (+,-,*,/,^) (두번째 값) \n 또는 : (루트,탄젠트,사인,코사인) (값) \n 또는 : (값)! (팩토리얼은 임베드 길이제한 때문에 454! 넘으면 안됨)")
                embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                await chs(embed = embed)

    if mos("닉줘야 메시지삭제"):
        try:
            delete = int(subcom[2])
            if message.author.id == "488177920066715659":
                limit = int(subcom[2]) + 1
            else:
                limit = int(subcom[2]) + 1
                if limit > 11:
                    limit = 10
            await message.channel.purge(limit = limit)
            await chs("삭제 완료! ^^")
        except IndexError:
            await chs("삭제할 양을 고르세여!")

    if mos("닉줘야 끝말잇기"):
        try:
            f = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\끝말잇기\\한방.txt", "r", encoding = "UTF-8")
            words = f.readlines()
            word = words[random.randint(0,134)]
            if subcom[2] != None:
                await chs("아 나먼저 할거야 ㅅㄱ. " + word + "참고로 끄투에 있는 단어")
        except:
            f = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\끝말잇기\\한방.txt", "r", encoding = "UTF-8")
            words = f.readlines()
            word = words[random.randint(0,134)]
            await chs("안말하면 먼저함 ㅅㄱ. " + word + "참고로 끄투에 있는 단어")

    if mos("닉줘야 꺼무위키") or mos("닉줘야 나무위키"):
        embed = discord.Embed(title = "꺼무위키 나라", color = 0x00ff00)

        embed.add_field(name = "꺼무위키 검색 완료", value = "https://namu.wiki/w/" + subcom[2])
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/681753994242031626/681759913273458708/e41518abdb668825.jpg")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        
        await chs(embed = embed)

    if mos("닉줘야 위키피디아") or mos("닉줘야 위키백과"):
        embed = discord.Embed(title = "위키백과 우리 모두의 백과사전", color = 0xfefefe)

        embed.add_field(name = "위키피디아 검색 완료", value = "https://ko.wikipedia.org/wiki/" + subcom[2])
        embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Wikipedia-logo-v2-ko.svg/1200px-Wikipedia-logo-v2-ko.svg.png")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

        await chs(embed = embed)
    
    if mos("닉줘야 빌보드"):
        if __name__ == "__main__":
            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
            res = requests.get("https://www.billboard.com/charts/billboard-200", headers = headers)
            html = res.text
            bs = BeautifulSoup(html, 'html.parser')
            titles = bs.find_all("span" , {"class":"chart-element__information__song"})
            artists = bs.find_all("span", {"class":"chart-element__information__artist"})
            title = []
            artist = []
            try:
                try:
                    StartRank = int(subcom[2])
                    Rank = int(subcom[3])
                    if StartRank > Rank:
                        embed.add_field(name = "에러!", value = "시작랭크는 마지막 랭크보다 클수 없잖아요...")
                        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        await chs(embed = embed)
                        return None
                    if StartRank > 200 or Rank > 200:
                        embed.add_field(name = "에러!", value = "빌보드 차트는 200위 까지 있어요")
                        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        await chs(embed = embed)
                        return None
                except IndexError:
                    StartRank = 1
                    Rank = int(subcom[2])
                    if Rank > 200:
                        embed.add_field(name = "에러!", value = "빌보드 차트는 200위 까지 있어요")
                        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        await chs(embed = embed)
                        return None
            except IndexError:
                StartRank = 1
                Rank = 10
            embed = discord.Embed(title = "빌보드 차트 {}~{}위".format(StartRank, Rank), color = 0xfefefe)
            embed.set_thumbnail(url = "https://pbs.twimg.com/profile_images/999581468971024384/Qvmvzk0r_400x400.jpg")
            for t in titles:
                title.append(t.text)
            for a in artists:
                artist.append(a.text)
            for i in range(StartRank,Rank + 1):
                embed.add_field(name = str(i) + "위", value = "Song : {} \n Artist : {}".format(title[i-1], artist[i-1]), inline = False)
            embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            await chs(embed = embed)

    if mos("닉줘야 메타크리틱"):
        if __name__ == "__main__":
            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
            res = requests.get("https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=condensed", headers = headers)
            html = res.text
            bs = BeautifulSoup(html, 'html.parser')
            gametitles = bs.find_all("div" , {"class":"basic_stat product_title"})
            gamesscore = bs.find_all("div" , {"class":"basic_stat product_score brief_metascore"})
            UserScores = bs.find_all("li", {"class":"stat product_avguserscore"})
            dates = bs.find_all("li", {"class" : "stat release_date full_release_date"})
            gametitle = []
            gamescore = []
            UserScore = []
            date = []
            try:
                try:
                    StartRank = int(subcom[2])
                    Rank = int(subcom[3])
                    if StartRank > Rank:
                        embed = discord.Embed(title = "오류!", color = 0xADFF2F)
                        embed.add_field(name = "오류!", value = "시작 랭크는 마지막 랭크보다 클수 없잖아요...")
                except:
                    StartRank = 1
                    Rank = int(subcom[3])
            except:
                StartRank = 1
                Rank = 10
            embed = discord.Embed(title = "메타크리틱 {0}~{1}위".format(StartRank,Rank), color = 0xADFF2F)
            embed.set_thumbnail(url = "https://image.pitchbook.com/kRGblPOht3FlVoThYuhOT5OIBHZ1522672911088_200x200?uq=SNQbS2T5")
            for t in gametitles:
                gametitle.append(t.find('a').text)
            for a in gamesscore:
                gamescore.append(a.find("div", {"class":"metascore_w small game positive"}).text)
            for d in dates:
                date.append(d.find("span", {"class":"data"}).text)
            for i in range(StartRank,Rank + 1):
                embed.add_field(name = str(i) + "위", value = "Game : {0} \n MetaScore : {1} \n Release Date : {2} \n".format(str(gametitle[i-1]).strip(), gamescore[i-1], date[i-1]), inline = False)
            embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            await chs(embed = embed)

    if mos("닉줘야 코로나"):
        if __name__ == "__main__":
            msg = await chs("한 10초 정도 걸립니다. 잠시만 기달려주세요.")
            embed = discord.Embed(title = "코로나바이러스감염증-19(COVID-19) 감염자 현황\n(병원체 명칭:SARS-CoV-2)", color = 0xB40404)
            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"}
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            option.add_argument('window-size=1920x1080')
            option.add_argument('--disable-gpu')
            driver = webdriver.Chrome("D:\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=option)
            driver.get("https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6")
            driver.implicitly_wait(5)
            time.sleep(5)
            res = requests.get("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=&brdGubun=&ncvContSeq=&contSeq=&board_id=&gubun=", headers = headers)
            html = driver.page_source
            html2 = res.text
            trans = Translator()
            bs = BeautifulSoup(html, 'html.parser')
            bs2 = BeautifulSoup(html2, 'html.parser')
            total = bs.find_all("div", {"class" : "flex-fix allow-shrink indicator-center-text responsive-text flex-vertical ember-view"})
            asdf = bs2.find("div", {"class":"data_table mgt16"})
            aa = asdf.find_all("td", {"class":"w_bold"})
            string2 = []
            Korea = []
            for a in aa:
                Korea.append(a.text)
            for t in total:
                string2.append(t.find("text").text)
            embed.add_field(name = "한국 현황", value="감염자 : {0}\n격리해제 : {1}\n사망자 : {2}\n검사진행중 : {3}".format(Korea[0],Korea[1],Korea[2],Korea[3]), inline = True)
            embed.add_field(name = "세계 현황", value="감염자 : {0}명\n완치자 : {1}명\n사망자 : {2}명".format(string2[0],string2[2],string2[3]))
            embed.add_field(name = "업데이트 날짜", value=string2[1], inline = False)
            embed.add_field(name = "출처", value = "[Johns Hopkins CSSE](<https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6>)\n[한국질병관리본부](<http://ncov.mohw.go.kr/index_main.jsp>)", inline = False)
            embed.add_field(name = "코로나바이러스 정보", value = "[나무위키](<https://namu.wiki/w/%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4>)\n[위키피디아](<https://ko.wikipedia.org/wiki/%EC%BD%94%EB%A1%9C%EB%82%98%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4>)", inline = False)
            embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/681753994242031626/681761164367364097/Biohazard_symbol.png")
            embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            await msg.edit(content = None, embed = embed)

    if mos("닉줘야 직업"):
        job = ["워리어", "매지션", "아처"]
        if subcom[2] == "뭐있음?":
            await chs(str(job[:])[1:-1]+"이(가) 있습니다.")               
        elif subcom[2] == "닉네임변경":
            sql = "update nickgame set nickname = (?) where discordID = (?);"
            subsql = "select nickname from nickgame where discordID = ?"
            try:
                cur.execute(subsql, (message.author.id,))
                embed = discord.Embed(title = "닉네임 변경", color = 0x2a4e6f)
                embed.add_field(name = "닉네임변경!", value = cur.fetchall()[0][0] + "님의 닉네임이 " + subcom[3] + "(으)로 변경되었습니다")
                embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                cur.execute(sql, (subcom[3], message.author.id,))
                conn.commit()
                await chs(embed=embed)
            except IndexError:
                embed = discord.Embed(title = "오류!", color = 0x2a4e6f)
                embed.add_field(name = "오류!", value = "뒤에 이름을 적어줘야 닉네임을 변경하죠!")
                await chs(embed = embed)
            except ZeroDivisionError:
                embed = discord.Embed(title = "오류!", color = 0x2a4e6f)
                embed.add_field(name = "오류!", value = "가입먼저 하셔야죠! 만약 가입했는데 오류나면 nickgive#5842 로 문의 ㄱㄱ")
                await chs(embed = embed)
        elif subcom[2] in job:
            try:
                subsql = "select * from nickgame where discordID = ?"
                cur.execute(subsql,(message.author.id,))
                if message.author.id in cur.fetchall()[0]:
                    await chs("이미 있는 유저잖아. 낚시 지리네")
                    return None
            except:
                sql = "insert into nickgame values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                itemsql = """create table "{}" (
	                "item"	text NOT NULL,
	                "many"	INTEGER NOT NULL,
	                PRIMARY KEY("many","item")
                ); """.format(message.author.id)
                await chs("당신은 이제 "+ subcom[2] +" 입니다.")
                if subcom[2] == "워리어": # 직업마다 HP MP 다르게 설정
                    HP = 100
                    MP = 50
                    damage = 60
                    avoid = 0
                    defence = 5
                elif subcom[2] == "매지션":
                    HP = 50
                    MP = 100
                    damage = 80
                    avoid = 0
                    defence = 0
                elif subcom[2] == "아처":
                    HP = 70
                    MP = 70
                    damage = 70
                    avoid = 5
                    defence = 0
                cur.execute(sql,(message.author.id, message.author.name, subcom[2], 1, 0, 200, HP, HP, MP, MP, damage, avoid, defence, 500, None))
                cur.execute(itemsql)
                conn.commit()
        elif subcom[2] == "내정보": # 자기정보 말하기
            sql = "select * from nickgame where discordID = ?"
            try:
                cur.execute(sql,(message.author.id,))
                row = cur.fetchall()
                embed = discord.Embed(title = "{0}님의 정보".format(row[0][1]),colour=0x00ff00)

                embed.add_field(name = "닉네임", value = str(row[0][1]), inline = True)
                embed.add_field(name = "직업", value = str(row[0][2]), inline = True)
                embed.add_field(name = "레벨", value = str(row[0][3]) + "레벨", inline = True)
                embed.add_field(name = "HP", value = str(row[0][6]) + "/" + str(row[0][7]), inline = True)
                embed.add_field(name = "MP", value = str(row[0][8]) + "/" + str(row[0][9]), inline = True)
                embed.add_field(name = "EXP", value = str(row[0][4]) + "/" + str(row[0][5]), inline = True)
                embed.add_field(name = "공격력", value = str(row[0][10]), inline = True)
                embed.add_field(name = "회피율", value = str(row[0][11]) + "%", inline = True)
                embed.add_field(name = "방어력", value = str(row[0][12]), inline = True)
                if row[0][14] == None:
                    embed.add_field(name = "현재 레이드 중인 보스", value = "없음", inline = True)
                else:
                    embed.add_field(name = "현재 레이드 중인 보스", value = str(row[0][14]), inline = True)
                embed.add_field(name = "가지고 있는 돈", value = str(row[0][13]) + '원', inline = True)
                embed.set_thumbnail(url = message.author.avatar_url)
                embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))

                await chs(embed = embed)
            except:
                embed = discord.Embed(title = "오류!", color = 0x2a4e6f)
                embed.add_field(name = "오류!", value = "가입먼저 하셔야죠! 만약 가입했는데 오류나면 nickgive#5842 로 문의 ㄱㄱ")
                await chs(embed = embed)
        elif subcom[2] == "전직": # 전직
            await chs("아직 준비중입니다.")
        elif subcom[2] == "초기화": # 초기화
            sql = "delete from nickgame where discordID = ?"
            itemsql = "drop table '{}';".format(message.author.id)
            try:
                cur.execute(sql,(message.author.id,))
                cur.execute(itemsql)
                conn.commit()
                await chs("직업이 초기화가 완료되었습니다. 다시 1렙부터 올리세요 ㅋㅋㅋㅋ") 
            except ZeroDivisionError:
                await chs("등록이 안되었는데 어떻게하냐 ㅋㅋㅋㅋㅋ 아 물론 등록 되있었으면 문의하곸ㅋㅋㅋㅋ")
        elif subcom[2] == "직업정보":
            f = open("C:\\Users\\Administrator\\Desktop\\Game\\Python\\직업설명\\" + subcom[3] + ".txt", 'r')
            data = f.read()
            embed = discord.Embed(title = subcom[3], color = 0x3EB489)
            embed.add_field(name = "설명", value = data)
            if subcom[3] == "워리어":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/669725992050229259/674959356525281290/92724262477537f9.png")
            elif subcom[3] == "나이트":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/669725992050229259/674883818867392512/d389957c03df8748.png")
            elif subcom[3] == "버서커":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/507134172960260097/674966792505917479/143972f88c18e6be.png")
            elif subcom[3] == "카버리":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/669725992050229259/674969511228604426/9212c76a09a1f1a8.PNG")
            elif subcom[3] == "아처":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/669725992050229259/674982050050342942/dfa7b7ddbf1ab3c8.png")
            elif subcom[3] == "매지션":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/678869345493057536/4769d52a86e2c8e4.png")
            elif subcom[3] == "다크매지션":
                embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/678872543062523905/7df86a15e7351616.png")
            embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            await chs(embed = embed)
            await chs("그림 그려주실분 구합니다 (졸라맨 사절)")
        else:
            await chs("올바른 사용법 : 닉줘야 직업 (뭐있음?, (직업이름), 내정보, 전직, 정보, 직업정보, 닉네임변경)\n직업:" + str(job[:])[1:-1])
    
    if mos("닉줘야 아이템"):
        try:
            try:
                itemsql = "select item from '{}'".format(message.author.id)
                cur.execute(itemsql)
                rows = cur.fetchall()
                items = []
                for row in rows:
                    items.append(row[0])
                    bbanegiwihangut.append(row)
                if subcom[2] == "버리기":
                    try:
                        embed = discord.Embed(title = "버리기 퉷퉷", color =0x126adf)
                        sql = "delete from '{}' where = ?;".format(message.author.id)
                        if subcom[3] == "전체":
                            embed.add_field(name="전체 버리기!!!!!!!!!!", value = "다 버리셨군요 다시 모으셈 ㅋㅋㅋㅋㅋㅋㅋ")
                            sql = "delete from '{}'".format(message.author.id)
                            cur.execute(sql)
                        else:
                            embed.add_field(name="{} 버리기!!!!!!!!!!".format(subcom[3]), value = "{}(을)를 버리셨군요 다시 모으셈 ㅋㅋㅋㅋㅋㅋㅋ".format(subcom[3]))
                            cur.execute(sql, (subcom[3],))
                    except IndexError:
                        embed = discord.Embed(title = "와! 오류!", color = 0x45a2df)
                        embed.add_field(name="오류!",value="뒤에다 아이템 이름을 적거나 전체를 적으셔야죠;;;")
                    embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                elif subcom[3] in items and subcom[2] == "사용":
                    cur.execute("update '{0}' set many = many - 1 where item = '{1}'".format(message.author.id, subcom[3]))
                    cur.execute("select many from '{0}' where item = '{1}'".format(message.author.id, subcom[3]))
                    row = cur.fetchall()
                    if row[0][0] == 0:
                        cur.execute("delete from '{}' where many = 0".format(message.author.id))
                    if subcom[3] == "HP포션":
                        cur.execute("update nickgame set HP = HP + 25 where discordID = ?",(message.author.id,))
                        cur.execute("select * from nickgame where discordID = ?",(message.author.id,))
                        embed = discord.Embed(title = "아이템 사용", color = 0xff0000)
                        row = cur.fetchall()
                        if row[0][6] > row[0][7]:
                            cur.execute("update nickgame set HP = maxHP where discordID = ?",(message.author.id,))
                            cur.execute("select * from nickgame where discordID = ?",(message.author.id,))
                            row = cur.fetchall()
                        embed.add_field(name = "체력 회복!", value = row[0][1] + "님의 체력이 회복되었습니다. 현재 남은 체력:" + str(row[0][6]))
                        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/678865983942688788/0e8b5a65b1da61c9.png")
                        conn.commit()
            except IndexError:
                cur.execute("select * from nickgame where discordID = '{}'".format(message.author.id))
                embed = discord.Embed(title = cur.fetchall()[0][1] + "님의 인벤토리", color = 0x00ffad)
                embed.set_thumbnail(url = message.author.avatar_url)
                cur.execute("select item, many from '{}'".format(message.author.id))
                rows = cur.fetchall()
                for row in rows:
                    embed.add_field(name = row[0], value = str(row[1]) + '개')
        except:
            embed = discord.Embed(title = "오류!", colour = 0xff0000)
            embed.add_field(name = "오류가 났다!", value = "등록먼저 하고 오세여. 혹시 등록했는데 오류가 발생하면 문의 ㄱㄱ")
            embed.set_thumbnail(url = message.author.avatar_url)
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)
            
    if mos("닉줘야 상점"):
        try:
            x = int(subcom[4])
        except IndexError:
            x = 1
        try:
            embed = discord.Embed(title = "구매",color = 0x4cc4cc)
            if subcom[2] == "구매":
                if subcom[3] == "HP포션":
                    embed = item_buy(what_item="HP포션",how_many=x, how_much=x*150, embed=embed)
        except IndexError:
            embed = discord.Embed(title = "상점 1",color = 0x4cc4cc)
            embed.add_field(name = "HP포션", value = "150원")
            embed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/663660941291946025/678578586617118720/zzz.png")
        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
        await chs(embed = embed)

    if mos("닉줘야 보스"):
        boss = ["초보보스"]
        if subcom[2] == "뭐있음?":
            await chs(str(boss[:])[1:-1] + "이(가) 있습니다.")
        if subcom[2] == "포기":
            cur.execute("update nickgame set None where discordId = ?", (message.author.id,))
            conn.commit()
            embed = discord.Embed(title = "레이드 포기", color = 0x000000)
            embed.add_field(name = "포기!", value = message.author.name + "님이 레이드 중인 보스를 포기하셨습니다.")
            embed.set_footer(icon_url = message.author.avatar_url, text = "포기한 이 : {0} , 포기한 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
            await chs(embed = embed)
        if subcom[2] in boss:
            if subcom[2] == "초보보스":
                if subcom[3] == "정보":
                    cur.execute("select * from boss where = ?",(subcom[2],))
                    row = cur.fetchall()
                    embed = discord.Embed(color = 0xffffff)

                    embed.add_field(name = "이름", value = "초보보스", inline = True)
                    embed.add_field(name = "체력", value = str(row[0][3]) + "/1000", inline = True)
                    embed.add_field(name = "예상 경험치", value = str(row[0][4]) + "exp", inline = True)
                    embed.add_field(name = "공격력", value = str(row[0][2]), inline = True)
                    embed.add_field(name = "설명", value = """이 보스는 원래 초보자 마을 연습장의 연습용 인형이었습니다.\n어느날, 이 인형이 어떤 마녀의 마법에 의해 초보자를 공격하기를 시작했고 초보자들을 무차별 죽였습니다.\n과연 당신들은 힘을 합쳐 이 인형을 물리칠수 있을까요?""", inline = False)
                    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/679325374282465280/asdf.png")

                    await chs(embed = embed)
                if subcom[3] == "공격":
                    cur.execute("select * from nickgame where discordID = ?",(message.author.id,))
                    row = cur.fetchall()
                    if row[0][14] == None or row[0][14] == "초보보스":
                        cur.execute("select HP, Damage from Boss where Name = ?",(subcom[2],))
                        Bossrow = cur.fetchall()[0]
                        nowHP = row[0][6]
                        nowBHP = Bossrow[0]
                        Dam = 0 if Bossrow[1] - row[0][12] < 0 else Bossrow[1] - row[0][12]
                        HP = row[0][6] - Dam
                        BossHP = Bossrow[0] - row[0][10]
                        cur.execute("update nickgame set HP = ?, nowraid = '초보보스' where discordID = ?",(HP,message.author.id,))
                        cur.execute("update Boss set HP = ? where Name = '초보보스'",(BossHP,))
                        embed = discord.Embed(title = "닉줘야 보스 레이드 (초보보스)", color = 0x000000)
                        if BossHP > 0:
                            if random.uniform(1,100) <= row[0][11]:
                                embed.add_field(name = "회피!", value = "보스의 공격을 회피하였습니다!")
                                cur.execute("update nickgame set HP = ? where discordID = ?",(nowHP,message.author.id))
                            elif Dam == 0:
                                embed.add_field(name = "방어!", value = "보스의 공격을 막았습니다!")
                            elif HP <= 0:
                                embed.add_field(name = "사망!", value = "보스에게 " + str(Dam) + "의 데미지를 받았습니다.\n 당신은 죽었습니다. 경험치 일부를 잃었습니다.")
                                outEXP = 0 if row[0][4] - row[0][5] * 0.1 < 0 else row[0][4] - row[0][5] * 0.1
                                cur.execute("update nickgame set exp = ? where discordID = ?", (outEXP,message.author.id))
                                cur.execute("update Boss set HP = ? where Name = '초보보스'",(nowBHP,))
                                cur.execute("update nickgame set HP = maxHP where discordID = ?", (message.author.id,))
                            else:
                                embed.add_field(name = "피해 받음!", value = "보스에게 " + str(Dam) + "의 데미지를 받았습니다.\n 남은 내 체력:" + str(HP))
                        if BossHP > 0 and HP > 0:
                            embed.add_field(name = "공격!", value = "보스에게 " + str(row[0][10]) + "의 데미지를 주었습니다.\n 남은 보스 체력:" + str(BossHP))
                        elif BossHP <= 0:
                            embed.add_field(name = "처치!", value = "보스를 처치했습니다.\n 보상 : 경험치 + 100")
                            cur.execute("update Boss set HP = 1000 where Name = '초보보스'")
                            cur.execute("update nickgame set exp = exp + 100, money = money + ?,HP = ? where nowraid = '초보보스'",(random.randint(301,500),nowHP))
                            cur.execute("select * from nickgame where nowraid = '초보보스'")
                            raided = cur.fetchall()
                            for i in range(0,len(raided)):
                                item_get = random.randint(1,10)
                                if item_get <= 6: # 포션
                                    embed = item_get_def(item_get_percentage = item_get, how_many = 3, play = raided[i], embed = embed, what_item = "HP포션", middle_percentage = 4, how_many2=4 )
                                if item_get <= 3:
                                    embed = item_get_def(item_get_percentage = item_get, how_many = 1, play = raided[i], embed = embed, what_item = "초보자의 상하의")
                                if raided[i][4] >= raided[i][5]:
                                    embed = level_up(raided[i], embed)
                        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/678585834773151744/679325374282465280/asdf.png")
                        if BossHP > 0:
                            embed.set_footer(icon_url = message.author.avatar_url, text = "공격한 이 : {0} , 공격한 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        elif BossHP <= 0 and HP > 0:
                            embed.set_footer(icon_url = message.author.avatar_url, text = "막타친 이 : {0} , 막타친 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        conn.commit()
                        await chs(embed = embed)
                    else:
                        embed = discord.Embed(title = "오류!", color = 0x000000)
                        embed.add_field(name = "레이드 관한 오류", value = "레이드 중인 다른 보스가 있습니다.\n 만약 다른 보스를 상대하고 싶다면 '닉줘야 보스 포기'를 써주세요")
                        embed.set_footer(icon_url = message.author.avatar_url, text = "보낸 이 : {0} , 보낸 날짜 : {1}년 {2}월 {3}일 {4}시 {5}분".format(message.author.display_name, now.year, now.month, now.day, now.hour, now.minute))
                        await message.channel.send(embed = embed)
                        
client.run(TOKEN)