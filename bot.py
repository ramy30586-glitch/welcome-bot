import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os


# إعداد الصلاحيات
intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# عند تشغيل البوت
@bot.event
async def on_ready():
    print(f"تم تشغيل البوت: {bot.user}")


# عند دخول عضو جديد
@bot.event
async def on_member_join(member):

    # فتح صورة الخلفية
    img = Image.open("welcome.png").convert("RGBA")

    draw = ImageDraw.Draw(img)


    # الخط
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()


    # اسم العضو
    text = f"Welcome {member.name}"


    # حساب مكان النص
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]

    x = (img.width - width) // 2
    y = img.height - 200


    # كتابة الاسم
    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255)
    )


    # تحميل صورة العضو
    avatar = member.display_avatar
    avatar_bytes = await avatar.read()


    with open("avatar.png", "wb") as f:
        f.write(avatar_bytes)


    avatar_img = Image.open("avatar.png").convert("RGBA")
    avatar_img = avatar_img.resize((200, 200))


    # وضع صورة العضو على الخلفية
    img.paste(
        avatar_img,
        (50, 50),
        avatar_img
    )


    # حفظ الصورة النهائية
    img.save("welcome_final.png")


    # إرسال الترحيب
    channel = bot.get_channel(
        int(os.getenv("CHANNEL_ID"))
    )


    await channel.send(
        content=f"🎉 أهلاً بك {member.mention}!\n👥 أنت العضو رقم {member.guild.member_count}",
        file=discord.File("welcome_final.png")
    )


# تشغيل البوت
bot.run(os.getenv("TOKEN"))
