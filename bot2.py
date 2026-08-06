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
        font = ImageFont.truetype("DejaVuSans.ttf", 90)
    except:
        font = ImageFont.load_default()


    # اسم العضو
    text = f"Welcome {member.name}"


    # حساب مكان النص
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    text_x = (img.width - text_width) // 2
    text_y = 640


    # كتابة الاسم
    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=(255, 255, 255)
    )


    # تحميل صورة العضو
    avatar = member.display_avatar
    avatar_bytes = await avatar.read()

    with open("avatar.png", "wb") as f:
        f.write(avatar_bytes)


    avatar_size = 340

    avatar_img = Image.open("avatar.png").convert("RGBA")
    avatar_img = avatar_img.resize((avatar_size, avatar_size))


    # إنشاء قناع دائري
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse(
        (0, 0, avatar_size, avatar_size),
        fill=255
    )


    # جعل الصورة دائرية
    avatar_circle = Image.new(
        "RGBA",
        (avatar_size, avatar_size)
    )

    avatar_circle.paste(
        avatar_img,
        (0, 0),
        mask
    )


    # وضع الصورة في المنتصف
    avatar_x = (img.width - avatar_size) // 2
    avatar_y = 220


    img.paste(
        avatar_circle,
        (avatar_x, avatar_y),
        avatar_circle
    )


    # حفظ الصورة النهائية
    img.save("welcome_final.png")


    # إرسال الترحيب
channel = bot.get_channel(
    int(os.getenv("CHANNEL_ID"))
)

rules = f"<#{os.getenv('RULES_CHANNEL_ID')}>"
guide = f"<#{os.getenv('GUIDE_CHANNEL_ID')}>"

await channel.send(
    content=(
        f"🎉 **مرحبًا بك {member.mention}!**\n\n"
        f"👥 أنت العضو رقم **{member.guild.member_count}**.\n\n"
        f"📜 يرجى قراءة القوانين: <#1500088241481842740>\n"
        f"🗺️ اطلع على خريطة السيرفر: <#1534225181210574990>\n\n"
        f"نتمنى لك وقتًا ممتعًا! 💙"
    ),
    file=discord.File("welcome_final.png")
)


# تشغيل البوت
bot.run(os.getenv("TOKEN"))