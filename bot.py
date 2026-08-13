import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import io


# ==============================
# إعداد الصلاحيات
# ==============================

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==============================
# عند تشغيل البوت
# ==============================

@bot.event
async def on_ready():
    print(f"🚀 تم تشغيل البوت: {bot.user}")


# ==============================
# عند دخول عضو جديد
# ==============================

@bot.event
async def on_member_join(member):

    print(f"✅ تم اكتشاف دخول عضو جديد: {member} | ID: {member.id}")

    # ==============================
    # جلب قناة الترحيب
    # ==============================

    channel_id = os.getenv("CHANNEL_ID")

    if not channel_id:
        print("❌ لم يتم العثور على CHANNEL_ID في متغيرات البيئة")
        return

    try:
        channel = bot.get_channel(int(channel_id))
    except ValueError:
        print("❌ CHANNEL_ID ليس رقمًا صحيحًا")
        return

    if not channel:
        print(f"❌ لم يتم العثور على القناة برقم: {channel_id}")
        return

    print(f"✅ تم العثور على قناة الترحيب: {channel.name}")

    # ==============================
    # نص الترحيب
    # ==============================

    welcome_text = (
        f"🎉 **مرحبًا بك {member.mention}!**\n\n"
        f"👥 أنت العضو رقم **{member.guild.member_count}**.\n\n"
        f"📜 يرجى قراءة القوانين: <#1500088241481842740>\n"
        f"🗺️ اطلع على خريطة السيرفر: <#1534225181210574990>\n\n"
        f"نتمنى لك وقتًا ممتعًا! 💙"
    )

    # ==============================
    # إنشاء صورة الترحيب
    # ==============================

    try:

        if not os.path.exists("welcome.png"):
            raise FileNotFoundError(
                "❌ ملف welcome.png غير موجود"
            )

        print("✅ تم العثور على welcome.png")

        img = Image.open("welcome.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        # ==============================
        # تحميل صورة العضو
        # ==============================

        avatar_bytes = await member.display_avatar.replace(
            size=512
        ).read()

        avatar_img = Image.open(
            io.BytesIO(avatar_bytes)
        ).convert("RGBA")

        print("✅ تم تحميل صورة العضو")

        # ==============================
        # حجم ومكان صورة العضو
        # ==============================

        avatar_size = 572

        avatar_x = 247
        avatar_y = 119

        avatar_img = avatar_img.resize(
            (avatar_size, avatar_size),
            Image.Resampling.LANCZOS
        )

        # ==============================
        # إنشاء القناع الدائري
        # ==============================

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

        # ==============================
        # جعل صورة العضو دائرية
        # ==============================

        avatar_circle = Image.new(
            "RGBA",
            (avatar_size, avatar_size),
            (0, 0, 0, 0)
        )

        avatar_circle.paste(
            avatar_img,
            (0, 0),
            mask
        )

        img.paste(
            avatar_circle,
            (avatar_x, avatar_y),
            avatar_circle
        )

        print("✅ تم وضع صورة العضو في التصميم")

        # ==============================
        # اسم العضو
        # ==============================

        text = member.name
        font_size = 60

        try:
            font = ImageFont.truetype(
                "arial.ttf",
                font_size
            )

        except:

            try:
                font = ImageFont.truetype(
                    "DejaVuSans-Bold.ttf",
                    font_size
                )

            except:

                font = ImageFont.load_default()

        # ==============================
        # حساب حجم النص
        # ==============================

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = bbox[2] - bbox[0]

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import io

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🚀 تم تشغيل البوت وضبط إحداثيات النص وحجمه: {bot.user}")

@bot.event
async def on_member_join(member):

    # 1. فتح صورة الخلفية (1920x1080)
    try:
        img = Image.open("welcome.png").convert("RGBA")
    except FileNotFoundError:
        print("❌ خطأ: لم يتم العثور على ملف 'welcome.png'")
        return

    draw = ImageDraw.Draw(img)

    # ----------------------------------------------------
    # 2. صورة العضو (Avatar) - المكان المضبوط تمامًا
    # ----------------------------------------------------
    avatar_bytes = await member.display_avatar.read()
    avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

    avatar_size = 572
    avatar_x = 247
    avatar_y = 119

    avatar_img = avatar_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask)

    img.paste(avatar_circle, (avatar_x, avatar_y), avatar_circle)

    # ----------------------------------------------------
    # 3. اسم العضو - مع اعتماد جلب حجم الخط من الكود المفضل
    # ----------------------------------------------------
    text = member.name
    font_size = 60  # حجم الخط المطلوب (60px)

    # جلب الخط بحجم 60 مباشرة بنفس منطق الكود الخاص بك
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            # استخدام حجم الخط المباشر الممرر لـ load_default
            font = ImageFont.load_default(size=font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    # تحريك موقع البدء الأساسي 90 بكسل لليمين
    base_x = 90 + 90  # 180
    text_x = base_x + (700 - text_width) // 2
    text_y = 955     # 945 + 10 (إنزال 10 بكسل)

    # رسم الظل والنص
    draw.text((text_x + 4, text_y + 4), text, font=font, fill=(10, 10, 25, 240))
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # ----------------------------------------------------
    # 4. إرسال الصورة
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

bot.run(os.getenv("TOKEN"))
