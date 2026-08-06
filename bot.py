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

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت بنجاح: {bot.user}")

@bot.event
async def on_member_join(member):

    # 1. فتح صورة الخلفية بدقة (1920x1080)
    try:
        img = Image.open("welcome.png").convert("RGBA")
    except FileNotFoundError:
        print("خطأ: لم يتم العثور على ملف 'welcome.png'")
        return

    draw = ImageDraw.Draw(img)

    # ----------------------------------------------------
    # 2. إعداد وصنع صورة العضو الدائرية (Avatar)
    # ----------------------------------------------------
    avatar_bytes = await member.display_avatar.read()
    avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

    # المقاسات المضبوطة لدقة 1920x1080
    avatar_size = 590
    avatar_x = 270
    avatar_y = 200

    # تغيير حجم صورة العضو
    avatar_img = avatar_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # إنشاء قناع دائري
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    # قص الصورة بشكل دائري
    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask)

    # لصق الصورة في منتصف الإطار الدائري
    img.paste(avatar_circle, (avatar_x, avatar_y), avatar_circle)

    # ----------------------------------------------------
    # 3. إعداد وكتابة اسم العضو في الشريط السفلي
    # ----------------------------------------------------
    text = member.name
    font_size = 55  # حجم خط متناسق ومناسب لدقة 1080p

    # تحميل الخط
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()

    # تصغير الخط تلقائياً إذا كان الاسم طويلاً
    max_text_width = 750
    while font_size > 20:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width:
            break
        font_size -= 2
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            break

    # توسيط النص أفقياً وعمودياً داخل الشريط السفلي
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    text_x = 80 + (750 - text_width) // 2
    text_y = 940  # الإحداثي العمودي لتنزيل الاسم داخل الشريط السفلي الفارغ

    # رسم ظل غامق خلف النص
    draw.text((text_x + 3, text_y + 3), text, font=font, fill=(10, 10, 25, 220))

    # رسم الاسم باللون الأبيض الناصع
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
