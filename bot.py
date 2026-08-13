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
    print(f"🚀 تم تشغيل البوت: {bot.user}")

@bot.event
async def on_member_join(member):
    # 1. جلب القناة أولاً
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        print("❌ لم يتم العثور على CHANNEL_ID في متغيرات البيئة")
        return

    channel = bot.get_channel(int(channel_id))
    if not channel:
        print(f"❌ لم يتم العثور على القناة برقم: {channel_id}")
        return

    # نص الترحيب
    welcome_text = (
        f"🎉 **مرحبًا بك {member.mention}!**\n\n"
        f"👥 أنت العضو رقم **{member.guild.member_count}**.\n\n"
        f"📜 يرجى قراءة القوانين: <#1500088241481842740>\n"
        f"🗺️ اطلع على خريطة السيرفر: <#1534225181210574990>\n\n"
        f"نتمنى لك وقتًا ممتعًا! 💙"
    )

    # 2. محاولة إنشاء الصورة
    try:
        if not os.path.exists("welcome.png"):
            raise FileNotFoundError("ملف welcome.png غير موجود")

        img = Image.open("welcome.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        # صورة العضو (Avatar)
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

        # اسم العضو (بدون تصفية معقدة)
        text = member.name
        font_size = 60

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # حساب الموقع ورسم النص
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
        except:
            text_width = 300 # قيمة افتراضية في حال فشل حساب الأبعاد

        base_x = 180
        text_x = base_x + (700 - text_width) // 2
        text_y = 955

        draw.text((text_x + 4, text_y + 4), text, font=font, fill=(10, 10, 25, 240))
        draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

        # حفظ وإرسال
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        await channel.send(content=welcome_text, file=discord.File(buffer, filename="welcome_card.png"))

    except Exception as e:
        print(f"⚠️ خطأ أثناء تجهيز الصورة: {e}")
        # إرسال الرسالة النصية فوراً عند حدوث أي مشكلة في الصورة
        await channel.send(content=welcome_text)

bot.run(os.getenv("TOKEN"))
