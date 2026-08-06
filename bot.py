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
    print(f"تم تشغيل البوت بنجاح: {bot.user}")

# عند دخول عضو جديد
@bot.event
async def on_member_join(member):

    # 1. فتح صورة الخلفية
    img = Image.open("welcome.png").convert("RGBA")

    # ----------------------------------------------------
    # 2. تجهيز وتأطير صورة العضو (Avatar)
    # ----------------------------------------------------
    avatar_bytes = await member.display_avatar.read()
    avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

    # الحجم الدقيق للدائرة البيضاء
    avatar_size = 350
    avatar_img = avatar_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # إنشاء قناع دائري (Mask)
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    # جعل الصورة دائرية
    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask)

    # المكان المناسب بالبيكسل داخل الدائرة البيضاء
    avatar_x = 94
    avatar_y = 51

    # وضع الصورة على خلفية الترحيب
    img.paste(avatar_circle, (avatar_x, avatar_y), avatar_circle)

    # ----------------------------------------------------
    # 3. إعداد وكتابة اسم العضو في الشريط الأزرق السفلي
    # ----------------------------------------------------
    draw = ImageDraw.Draw(img)
    text = member.name
    font_size = 32

    # تحميل الخط
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # تصغير الخط تلقائياً إذا كان الاسم طويلاً ليتناسب مع الشريط
    max_text_width = 380
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width or font_size <= 14:
            break
        font_size -= 2
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            break

    # حساب المكان المناسب ليكون النص موسطاً داخل الشريط الأزرق
    text_x = 60 + (410 - text_width) // 2
    text_y = 498

    # رسم ظل خفيف لزيادة وضوح النص
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(20, 20, 40, 180))

    # رسم اسم العضو بلون أبيض
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # ----------------------------------------------------
    # 4. إرسال الصورة في القناة
    # ----------------------------------------------------
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    channel_id = os.getenv("CHANNEL_ID")
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send(
                content=(
                    f"🎉 **مرحبًا بك {member.mention}!**\n\n"
                    f"👥 أنت العضو رقم **{member.guild.member_count}**.\n\n"
                    f"📜 يرجى قراءة القوانين: <#1500088241481842740>\n"
                    f"🗺️ اطلع على خريطة السيرفر: <#1534225181210574990>\n\n"
                    f"نتمنى لك وقتًا ممتعًا! 💙"
                ),
                file=discord.File(buffer, filename="welcome_card.png")
            )

# تشغيل البوت
bot.run(os.getenv("TOKEN"))
