import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import io

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

    # فتح الخلفية
    img = Image.open("welcome.png").convert("RGBA")
    draw = ImageDraw.Draw(img)


    # الخط
    try:
        font = ImageFont.truetype(
            "DejaVuSans.ttf",
            110
        )
    except:
        font = ImageFont.load_default()


    # اسم العضو فقط
    text = member.name


    # حساب مكان الاسم
    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]

    text_x = (img.width - text_width) // 2
    text_y = 780


    # ظل الاسم
    draw.text(
        (text_x + 5, text_y + 5),
        text,
        font=font,
        fill=(40, 40, 80)
    )


    # الاسم
    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=(255, 255, 255)
    )


    # تحميل صورة العضو
    avatar_bytes = await member.display_avatar.read()

    avatar_img = Image.open(
        io.BytesIO(avatar_bytes)
    ).convert("RGBA")


    # حجم الصورة
    avatar_size = 430

    avatar_img = avatar_img.resize(
        (avatar_size, avatar_size)
    )


    # إنشاء قناع دائري
    mask = Image.new(
        "L",
        (avatar_size, avatar_size),
        0
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse(
        (0, 0, avatar_size, avatar_size),
        fill=255
    )


    # جعل الصورة دائرية
    avatar_circle = Image.new(
        "RGBA",
        (avatar_size, avatar_size),
        (0,0,0,0)
    )

    avatar_circle.paste(
        avatar_img,
        (0,0),
        mask
    )


    # مكان الصورة داخل الدائرة
    avatar_x = 180
    avatar_y = 80


    img.paste(
        avatar_circle,
        (avatar_x, avatar_y),
        avatar_circle
    )


    # حفظ الصورة
    img.save("welcome_final.png")


    # قناة الترحيب
    channel = bot.get_channel(
        int(os.getenv("CHANNEL_ID"))
    )


    await channel.send(
        content=(
            f"🎉 **مرحبًا بك {member.mention}!**\n\n"
            f"👥 أنت العضو رقم **{member.guild.member_count}**.\n\n"
            f"📜 يرجى قراءة القوانين: <#1500088241481842740>\n"
            f"🗺️ اطلع على خريطة السيرفر: <#1534225181210574990>\n\n"
            f"نتمنى لك وقتًا ممتعًا! 💙"
        ),
        file=discord.File(
            "welcome_final.png"
        )
    )


# تشغيل البوت
bot.run(os.getenv("TOKEN"))
