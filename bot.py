import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import io

# إعداد الصلاحيات (Intents)
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# عند تشغيل البوت بنجاح
@bot.event
async def on_ready():
    print(f"تم تشغيل البوت بنجاح: {bot.user}")

# عند دخول عضو جديد
@bot.event
async def on_member_join(member):

    # 1. فتح صورة الخلفية الخاصة بك
    # تأكد من أن ملف 'welcome.png' موجود في نفس مجلد ملف الكود
    try:
        img = Image.open("welcome.png").convert("RGBA")
    except FileNotFoundError:
        print("خطأ: لم يتم العثور على ملف 'welcome.png'. تأكد من وجوده في نفس المجلد.")
        return

    # ----------------------------------------------------
    # 2. إعداد وتأطير صورة العضو (Avatar)
    # ----------------------------------------------------
    avatar_bytes = await member.display_avatar.read()
    avatar_img = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")

    # القطر الدقيق للدائرة البيضاء في التصميم
    avatar_size = 280
    avatar_img = avatar_img.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

    # إنشاء قناع دائري (Mask)
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

    # جعل الصورة الشخصية دائرية
    avatar_circle = Image.new("RGBA", (avatar_size, avatar_size), (0, 0, 0, 0))
    avatar_circle.paste(avatar_img, (0, 0), mask)

    # الإحداثيات المصححة لمركز الدائرة البيضاء في الخلفية
    # المركز الفعلي للدائرة في التصميم هو (290, 210) تقريبًا.
    avatar_x = 150
    avatar_y = 70

    # وضع الصورة الشخصية على خلفية الترحيب في المكان الصحيح
    img.paste(avatar_circle, (avatar_x, avatar_y), avatar_circle)

    # ----------------------------------------------------
    # 3. إعداد وكتابة اسم العضو في الشريط الأزرق السفلي
    # ----------------------------------------------------
    draw = ImageDraw.Draw(img)
    text = member.name
    font_size = 32 # حجم خط مناسب لارتفاع الشريط

    # تحميل الخط
    # تأكد من وجود ملف خط مناسب مثل 'DejaVuSans-Bold.ttf' أو غيّر الاسم لخط موجود في نظامك
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", font_size)
        except:
            print("تحذير: لم يتم العثور على خط، سيتم استخدام الخط الافتراضي.")
            font = ImageFont.load_default()

    # تصغير حجم الخط تلقائيًا إذا كان اسم العضو طويلاً
    max_text_width = 380
    while True:
        # draw.textbbox((0, 0), text, font=font) يعيد (x0, y0, x1, y1)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width or font_size <= 14:
            break
        font_size -= 2
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except:
            break

    # حساب موقع النص ليكون موسطاً أفقيًا وعموديًا داخل الشريط الأزرق السفلي
    text_x = 60 + (410 - text_width) // 2
    text_y = 495 # الارتفاع المناسب لمنتصف الشريط

    # رسم ظل خفيف لزيادة وضوح النص
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(20, 20, 40, 180))

    # رسم اسم العضو بلون أبيض
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))

    # ----------------------------------------------------
    # 4. إرسال الصورة في قناة الترحيب
    # ----------------------------------------------------
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # احصل على ID قناة الترحيب من متغيرات البيئة
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
        else:
            print(f"خطأ: لم يتم العثور على قناة الترحيب ذات الـ ID: {channel_id}")
    else:
        print("خطأ: لم يتم تعيين متغير البيئة 'CHANNEL_ID'.")

# تشغيل البوت
# تأكد من تعيين متغير البيئة 'TOKEN' برمز توكن البوت الخاص بك
token = os.getenv("TOKEN")
if token:
    bot.run(token)
else:
    print("خطأ: لم يتم تعيين متغير البيئة 'TOKEN'.")
