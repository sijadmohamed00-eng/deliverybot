import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import unicodedata
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")

DATA = {
    "الاعظمية": [
        {"area": "شارع الضباط", "price": "1", "distance": "1كم"},
        {"area": "الشماسية", "price": "1", "distance": "1-2كم"},
        {"area": "شارع عمر", "price": "1", "distance": "2-3كم"},
        {"area": "ساحة عنتر", "price": "1", "distance": "2-3كم"},
        {"area": "شارع الاخطل", "price": "1", "distance": "2-3كم"},
        {"area": "شارع 20", "price": "1", "distance": "3-4كم"},
        {"area": "شارع سهام", "price": "1", "distance": "2-3كم"},
        {"area": "قصر بلاسم", "price": "1", "distance": "3-4كم"},
        {"area": "شارع المشاتل", "price": "1", "distance": "3-4كم"},
        {"area": "جامع النداء", "price": "1", "distance": "3-4كم"},
        {"area": "الكم", "price": "1", "distance": "2-3كم"},
        {"area": "راغبة غاتون", "price": "1", "distance": "1-2كم"},
        {"area": "شارع أبو حنيفة", "price": "1", "distance": "3-4كم"},
        {"area": "السفينة", "price": "2", "distance": "4-5كم"},
        {"area": "المقبرة الملكية", "price": "2", "distance": "4-5كم"},
        {"area": "مقابر الخيزران", "price": "2", "distance": "4-5كم"},
        {"area": "مقبرة الشهداء", "price": "2", "distance": "4كم"},
        {"area": "مستشفى النعمان", "price": "2", "distance": "4-5كم"},
        {"area": "كورنيش الاعظمية", "price": "2", "distance": "4-5كم"},
        {"area": "المسناية", "price": "2", "distance": "5-6كم"},
        {"area": "جسر الئأمة", "price": "2", "distance": "5-6كم"},
        {"area": "كورنيش الكاظمية", "price": "2", "distance": "6-7كم"},
        {"area": "شارع اكد", "price": "2", "distance": "7-8كم"},
        {"area": "مستشفى أطفال الكاظمية", "price": "2", "distance": "7-8كم"},
        {"area": "فلكة محمد الجواد", "price": "2", "distance": "7-8كم"},
        {"area": "باب المراد", "price": "2", "distance": "7-8كم"},
        {"area": "مجمع العبسلي", "price": "2", "distance": "7-8كم"},
        {"area": "شارع الجواد", "price": "2", "distance": "7-8كم"},
        {"area": "معسكر العدالة", "price": "2", "distance": "8-9كم"},
        {"area": "الوزيرية", "price": "2", "distance": "6-7كم"},
        {"area": "شارع المغرب", "price": "2", "distance": "6-7كم"},
        {"area": "باب المعظم", "price": "2", "distance": "7-8كم"},
        {"area": "مدينة الطب", "price": "2", "distance": "6-7كم"},
        {"area": "صليخ", "price": "2", "distance": "5-6كم"},
        {"area": "القاهرة جهة النداء", "price": "2", "distance": "5-6كم"},
        {"area": "القاهرة الدلفية", "price": "2", "distance": "5-7كم"},
        {"area": "الكريعات", "price": "3", "distance": "7-8كم"},
    ],
    "البنوك": [
        {"area": "طاقه ومجمع الاساتذه", "price": "0", "distance": "1كم"},
        {"area": "نادي العربي", "price": "1", "distance": "2كم"},
        {"area": "طالبية", "price": "1", "distance": "2كم"},
        {"area": "نادي النفط", "price": "1", "distance": "2كم"},
        {"area": "حي اور 600", "price": "1", "distance": "2-3كم"},
        {"area": "صباح الخياط", "price": "1", "distance": "2-3كم"},
        {"area": "علوة زويني", "price": "1", "distance": "2-3كم"},
        {"area": "البنوك بكل مخارجها ومداخلها", "price": "1", "distance": "2-4كم"},
        {"area": "حي سومر", "price": "1", "distance": "3-4كم"},
        {"area": "عمار ابن ياسر", "price": "1", "distance": "2-3كم"},
        {"area": "شارع فلسطين تقاطع الصخرة", "price": "2", "distance": "4كم"},
        {"area": "شارع فلسطين نادي التركماني", "price": "2", "distance": "4-5كم"},
        {"area": "شارع فلسطين مركز شرطة القناة", "price": "2", "distance": "4-5كم"},
        {"area": "م ابن البلدي", "price": "2", "distance": "3-4كم"},
        {"area": "حي اور معمل الرحلات", "price": "2", "distance": "3-4كم"},
        {"area": "حي اور كوفي السلطان", "price": "2", "distance": "3-4كم"},
        {"area": "حي الكوفه", "price": "2", "distance": "4-5كم"},
        {"area": "سبع قصور", "price": "2", "distance": "4-5كم"},
        {"area": "قاهرة من جسر البنوك لغاية جامعة الامام الصادق", "price": "2", "distance": "4-5كم"},
        {"area": "ام الكبر", "price": "2", "distance": "4-5كم"},
        {"area": "جميلة", "price": "2", "distance": "4-5كم"},
        {"area": "مدينه الصدر من الفلاح الى قطاع 79", "price": "2", "distance": "5-7كم"},
        {"area": "كسرة وعطش", "price": "2", "distance": "5-6كم"},
        {"area": "نهايه حي اور", "price": "2", "distance": "4-5كم"},
        {"area": "شيشان حي اور", "price": "2", "distance": "4-5كم"},
        {"area": "اريدو وساحة بيروت", "price": "2", "distance": "6-7كم"},
        {"area": "مستشفى الكندي", "price": "3", "distance": "7-8كم"},
        {"area": "النهضة", "price": "3", "distance": "8-9كم"},
    ],
    "الحرية": [
        {"area": "شارع الدور العريض", "price": "0", "distance": "1كم"},
        {"area": "بيت شاطىء", "price": "0", "distance": "1كم"},
        {"area": "مصور عيسى", "price": "0", "distance": "1كم"},
        {"area": "كباب ابو رضا", "price": "0", "distance": "0كم"},
        {"area": "جامع المشاهده", "price": "1", "distance": "1-2كم"},
        {"area": "دور النواب", "price": "1", "distance": "2-3كم"},
        {"area": "دور الضباط", "price": "1", "distance": "2-3كم"},
        {"area": "شارع 20", "price": "1", "distance": "2-3كم"},
        {"area": "حي السلام", "price": "1", "distance": "3-4كم"},
        {"area": "البستان", "price": "1", "distance": "2-3كم"},
        {"area": "الدباش", "price": "1", "distance": "3-4كم"},
        {"area": "جامع زين العابدين", "price": "1", "distance": "2-3كم"},
        {"area": "شارع المشجر", "price": "1", "distance": "1-2كم"},
        {"area": "الحريه 1 2 3", "price": "1", "distance": "2-4كم"},
        {"area": "الحريه شارع الصحه", "price": "1", "distance": "1-2كم"},
        {"area": "الحريه الجمعيه", "price": "1", "distance": "2-3كم"},
        {"area": "الزراعي بالحريه", "price": "2", "distance": "4-5كم"},
        {"area": "الامام الحسين واخيه العباس", "price": "2", "distance": "3-4كم"},
        {"area": "الكاظميه", "price": "2", "distance": "4-5كم"},
        {"area": "الدولعي", "price": "2", "distance": "4-5كم"},
        {"area": "حي الجامعه", "price": "2", "distance": "4-5كم"},
        {"area": "الوشاش", "price": "2", "distance": "6-7كم"},
        {"area": "المنصور", "price": "2", "distance": "5-6كم"},
        {"area": "الاسكان", "price": "2", "distance": "4-5كم"},
        {"area": "شالجيه", "price": "2", "distance": "5-6كم"},
        {"area": "الطي", "price": "3", "distance": "6-7كم"},
        {"area": "العلاوي", "price": "3", "distance": "6-7كم"},
        {"area": "المنصور البيجية", "price": "3", "distance": "6-7كم"},
    ],
    "الدورة": [
        {"area": "شارع 60", "price": "1", "distance": "1-2كم"},
        {"area": "شارع 120", "price": "1", "distance": "2-3كم"},
        {"area": "شارع الزيتون", "price": "1", "distance": "2-3كم"},
        {"area": "شارع الصحة", "price": "1", "distance": "2-3كم"},
        {"area": "الرواد", "price": "1", "distance": "2-3كم"},
        {"area": "كلية الهادي", "price": "1", "distance": "1-2كم"},
        {"area": "هور رجب", "price": "2", "distance": "5-6كم"},
        {"area": "أبو دشير", "price": "2", "distance": "4-5كم"},
        {"area": "عمارات كفائات الصحة", "price": "2", "distance": "4-5كم"},
        {"area": "حي اسيا وحي الحضر", "price": "2", "distance": "3-4كم"},
        {"area": "الوادي", "price": "2", "distance": "4-5كم"},
        {"area": "الاسكان", "price": "2", "distance": "5كم"},
        {"area": "المعلمين", "price": "2", "distance": "5-6كم"},
        {"area": "حي الشرطة", "price": "2", "distance": "5-6كم"},
        {"area": "حي دجلة", "price": "2", "distance": "5-6كم"},
        {"area": "المعامرة", "price": "2", "distance": "6-7كم"},
        {"area": "الطعمة", "price": "2", "distance": "6-7كم"},
        {"area": "المخابرات وحي زبيرة", "price": "2", "distance": "6-7كم"},
        {"area": "سكانية", "price": "2", "distance": "4-5كم"},
        {"area": "كلية دجلة", "price": "2", "distance": "5-6كم"},
        {"area": "كلية الفارابي", "price": "2", "distance": "6-7كم"},
        {"area": "الجامعة التقنية الوسطى", "price": "2", "distance": "7-8كم"},
        {"area": "شهداء أبو دشير", "price": "2", "distance": "6-7كم"},
        {"area": "بريد الدورة", "price": "2", "distance": "5-6كم"},
        {"area": "حاتم السعدون", "price": "2", "distance": "5-6كم"},
        {"area": "كرارة", "price": "2", "distance": "7-8كم"},
        {"area": "خط النفط", "price": "2", "distance": "10-11كم"},
        {"area": "الاثوريين", "price": "3", "distance": "5-7كم"},
        {"area": "كلية السلام", "price": "3", "distance": "6-7كم"},
        {"area": "السيدية وشهداء السيدية", "price": "3", "distance": "7-8كم"},
        {"area": "العدوانية", "price": "3", "distance": "6-7كم"},
        {"area": "علوة الرشيد", "price": "3", "distance": "8-9كم"},
        {"area": "كويريش", "price": "3", "distance": "8-9كم"},
        {"area": "جمعية خير الله", "price": "3", "distance": "9-10كم"},
        {"area": "جسر الطابقين", "price": "3", "distance": "10-12كم"},
        {"area": "المهدية 1 2 3", "price": "3", "distance": "10-11كم"},
        {"area": "السابعة مدخل الحشد", "price": "3", "distance": "9-10كم"},
        {"area": "جسر المعسكر الثامنة", "price": "3", "distance": "9-10كم"},
        {"area": "شيخ سردي وجسر صدام", "price": "3", "distance": "8-9كم"},
        {"area": "عرب جبور", "price": "3", "distance": "9-11كم"},
        {"area": "البعيثة", "price": "3", "distance": "10-12كم"},
        {"area": "زراعي الشرطة", "price": "3", "distance": "10-11كم"},
        {"area": "زراعي والملا والعبيدي وأبو طيارة", "price": "3", "distance": "9-11كم"},
        {"area": "اعلام البياع", "price": "3", "distance": "10-11كم"},
        {"area": "التراث", "price": "3", "distance": "10-12كم"},
        {"area": "المعالف", "price": "3", "distance": "12-13كم"},
        {"area": "المعدات", "price": "3", "distance": "11-12كم"},
        {"area": "مصفى الدورة", "price": "3", "distance": "10-11كم"},
        {"area": "مجمع الايادي", "price": "3", "distance": "9-10كم"},
        {"area": "دور النفط", "price": "3", "distance": "10-11كم"},
    ],
    "الشعب": [
        {"area": "الصحه", "price": "1", "distance": "1كم"},
        {"area": "وصفي المضمد", "price": "1", "distance": "1كم"},
        {"area": "جامع الحق", "price": "1", "distance": "1كم"},
        {"area": "جامع الارقم", "price": "1", "distance": "2-3كم"},
        {"area": "صلاح الدين", "price": "1", "distance": "2-3كم"},
        {"area": "شارع عدن", "price": "1", "distance": "2-3كم"},
        {"area": "جامع الجهاد", "price": "1", "distance": "2-3كم"},
        {"area": "شارع المحكمه", "price": "1", "distance": "2كم"},
        {"area": "الجزائر", "price": "1", "distance": "2-3كم"},
        {"area": "الفيحاء", "price": "1", "distance": "1-2كم"},
        {"area": "المثلث", "price": "1", "distance": "2كم"},
        {"area": "الديوان", "price": "1", "distance": "2-3كم"},
        {"area": "شارع 25", "price": "1", "distance": "2كم"},
        {"area": "شارع 40", "price": "1", "distance": "2-3كم"},
        {"area": "شارع 15", "price": "1", "distance": "2كم"},
        {"area": "سما بغداد", "price": "1", "distance": "2كم"},
        {"area": "زراعيه شارع 20", "price": "1", "distance": "2كم"},
        {"area": "ساحه علاء نجف", "price": "1", "distance": "1-2كم"},
        {"area": "شارع ابو ماهر", "price": "1", "distance": "2كم"},
        {"area": "حجي عادل", "price": "1", "distance": "1-2كم"},
        {"area": "حي البساتين مقابيل المحكمه", "price": "2", "distance": "2-3كم"},
        {"area": "البساتين شارع احمد الوائلي", "price": "2", "distance": "3-4كم"},
        {"area": "البساتين شارع التكاتك", "price": "2", "distance": "3-4كم"},
        {"area": "البساتين شارع الشخ منهل", "price": "2", "distance": "3-4كم"},
        {"area": "حي المصطفى", "price": "2", "distance": "4كم"},
        {"area": "حي المهندسين", "price": "2", "distance": "4كم"},
        {"area": "جمعيات وجامع المحترك", "price": "2", "distance": "2-3كم"},
        {"area": "شارع ابو هيثم", "price": "2", "distance": "3كم"},
        {"area": "بساتين الضباط", "price": "2", "distance": "3-4كم"},
        {"area": "بساتين حي السلام", "price": "2", "distance": "3-4كم"},
        {"area": "بساتين من جهة القناه", "price": "2", "distance": "4كم"},
        {"area": "بساتين الشقق", "price": "2", "distance": "4كم"},
        {"area": "بساتين اسواق فراوله", "price": "2", "distance": "3-4كم"},
        {"area": "بساتين شارع السبيس", "price": "2", "distance": "3-4كم"},
        {"area": "سيطره الشعب القديمه", "price": "2", "distance": "3-4كم"},
        {"area": "السريدات", "price": "2", "distance": "4كم"},
        {"area": "حي الشهيدين", "price": "2", "distance": "4كم"},
        {"area": "الثعالبه", "price": "2", "distance": "4-5كم"},
        {"area": "بوب الشام", "price": "2", "distance": "5-6كم"},
        {"area": "واحد حزيران", "price": "2", "distance": "5-6كم"},
        {"area": "بوب الشام بعد القوس", "price": "3", "distance": "6-7كم"},
        {"area": "فوج شمال بغداد", "price": "3", "distance": "6-7كم"},
    ],
    "الغدير": [
        {"area": "الغدير", "price": "1", "distance": "1كم"},
        {"area": "تل محمد", "price": "1", "distance": "1-2كم"},
        {"area": "بغداد الجديده الدرويش", "price": "1", "distance": "3-4كم"},
        {"area": "زيونه", "price": "1", "distance": "2-3كم"},
        {"area": "ميسلون", "price": "1", "distance": "1كم"},
        {"area": "شارع الربيعي", "price": "1", "distance": "1-2كم"},
        {"area": "الف دار", "price": "1", "distance": "4-5كم"},
        {"area": "بغداد الجديده شارع المسبح الفين", "price": "2", "distance": "4-5كم"},
        {"area": "الأمين", "price": "2", "distance": "4-5كم"},
        {"area": "البلديات", "price": "2", "distance": "4-5كم"},
        {"area": "الكراده خارج", "price": "2", "distance": "5-6كم"},
        {"area": "الكراده داخل", "price": "2", "distance": "6-7كم"},
        {"area": "النعيريه", "price": "2", "distance": "5-6كم"},
        {"area": "الحبيبيه", "price": "2", "distance": "5-6كم"},
        {"area": "شارع فلسطين حي النيل", "price": "2", "distance": "5-6كم"},
        {"area": "شارع فلسطين حي المهندسين", "price": "2", "distance": "5-6كم"},
        {"area": "كراج الامانه", "price": "2", "distance": "4-5كم"},
        {"area": "مشتل", "price": "2", "distance": "5-6كم"},
        {"area": "فلكه رقم 10", "price": "2", "distance": "4-5كم"},
        {"area": "شارع المطبك", "price": "2", "distance": "6-7كم"},
        {"area": "ملجأ", "price": "2", "distance": "5-6كم"},
        {"area": "شارع السعدون", "price": "2", "distance": "5-6كم"},
        {"area": "ملعب الشعب على جهة وزاره الداخليه", "price": "2", "distance": "5-6كم"},
        {"area": "مدينه قطاع 0 1 2 3", "price": "2", "distance": "6-7كم"},
        {"area": "الاستكشافات", "price": "3", "distance": "6-7كم"},
        {"area": "الجملة العصبيه", "price": "3", "distance": "6-7كم"},
        {"area": "كفاءات العبيدي", "price": "3", "distance": "7-8كم"},
        {"area": "اورفلي", "price": "3", "distance": "7-8كم"},
        {"area": "رستميه", "price": "3", "distance": "6-7كم"},
    ],
    "الغزالية": [
        {"area": "شارع مدير الامن", "price": "1", "distance": "1-2كم"},
        {"area": "شارع الصديق", "price": "1", "distance": "1-2كم"},
        {"area": "مرور الغزالية", "price": "1", "distance": "2كم"},
        {"area": "سوق النفلة", "price": "1", "distance": "2كم"},
        {"area": "شارع أسواق الزاوية", "price": "1", "distance": "1-2كم"},
        {"area": "الهياكل", "price": "2", "distance": "3-4كم"},
        {"area": "ام القرى", "price": "2", "distance": "3-4كم"},
        {"area": "سوق المائدة", "price": "2", "distance": "3-4كم"},
        {"area": "شارع المهاجرين", "price": "2", "distance": "3-4كم"},
        {"area": "شارع المركز", "price": "2", "distance": "3-4كم"},
        {"area": "شارع الضغط", "price": "2", "distance": "4-5كم"},
        {"area": "البكرية", "price": "2", "distance": "3-4كم"},
        {"area": "شارع البصرة", "price": "2", "distance": "4-5كم"},
        {"area": "شارع الزبير", "price": "2", "distance": "4-5كم"},
        {"area": "مجمع المالية", "price": "2", "distance": "4-5كم"},
        {"area": "المجمع السويسري", "price": "2", "distance": "5-6كم"},
        {"area": "مول الغزالية", "price": "2", "distance": "4-5كم"},
        {"area": "شارع البدالة", "price": "2", "distance": "4-5كم"},
        {"area": "الشعلة", "price": "2", "distance": "6-7كم"},
        {"area": "حي الخضراء", "price": "2", "distance": "7-8كم"},
        {"area": "جرف الملح", "price": "2", "distance": "7-8كم"},
        {"area": "الرحمانية", "price": "3", "distance": "4-6كم"},
        {"area": "الصابئات", "price": "3", "distance": "7-8كم"},
        {"area": "السلاميات", "price": "3", "distance": "9-10كم"},
        {"area": "العامرية", "price": "3", "distance": "9-10كم"},
        {"area": "حي الحسين", "price": "3", "distance": "9-10كم"},
    ],
    "حي العامل": [
        {"area": "شارع السكلات والجنابات", "price": "1", "distance": "1كم"},
        {"area": "شارع 30 جامع العشرة المبشر", "price": "1", "distance": "1كم"},
        {"area": "دور النفط", "price": "1", "distance": "1-2كم"},
        {"area": "مركز الصحي", "price": "1", "distance": "1-2كم"},
        {"area": "شارع 7 نيسان وشارع التايرات", "price": "1", "distance": "2-3كم"},
        {"area": "سوق الشعبي وجامع الزهراء", "price": "1", "distance": "1-2كم"},
        {"area": "شارع المصرف وفوج المصرف", "price": "1", "distance": "1-2كم"},
        {"area": "شارع 84 الجمعيات", "price": "1", "distance": "1-2كم"},
        {"area": "سوق المكاصيص", "price": "1", "distance": "2-3كم"},
        {"area": "نادي صلاح الدين", "price": "1", "distance": "2-3كم"},
        {"area": "مدرسة تعز والبريد", "price": "1", "distance": "2-3كم"},
        {"area": "شارع التشييش", "price": "1", "distance": "2-3كم"},
        {"area": "حي صدام وشارع المطار", "price": "1", "distance": "4-5كم"},
        {"area": "المدارس الصفر", "price": "1", "distance": "3-4كم"},
        {"area": "هايبر ماركت البياع", "price": "1", "distance": "3-4كم"},
        {"area": "فلكة حياوي ومؤسسة بنت الهدى", "price": "1", "distance": "2-3كم"},
        {"area": "حي العمداء", "price": "1", "distance": "3-4كم"},
        {"area": "حي الجهاد وحي الأساتذة والملحانية", "price": "2", "distance": "4-5كم"},
        {"area": "حي الحسين وحي العباس", "price": "2", "distance": "5-6كم"},
        {"area": "البياع وشهداء البياع", "price": "2", "distance": "6-7كم"},
        {"area": "حي الرسالة وشارع السياب", "price": "2", "distance": "6-7كم"},
        {"area": "محطة نفايات البياع", "price": "2", "distance": "4-5كم"},
        {"area": "مدرسة سعد ابن المسيب", "price": "2", "distance": "5-6كم"},
        {"area": "شارع 9 نيسان", "price": "2", "distance": "5-6كم"},
        {"area": "شارع المكتفي", "price": "2", "distance": "5-7كم"},
        {"area": "تقاطع البياع", "price": "2", "distance": "6-7كم"},
        {"area": "شارع المعتز", "price": "2", "distance": "6-7كم"},
        {"area": "مجمع المحبة السكني", "price": "2", "distance": "7-8كم"},
        {"area": "مجمع السلام", "price": "2", "distance": "4-5كم"},
        {"area": "اليرموك", "price": "3", "distance": "7-8كم"},
        {"area": "حي التراث", "price": "3", "distance": "7-8كم"},
        {"area": "الشرطة الرابعة", "price": "3", "distance": "8-9كم"},
        {"area": "الشرطة الخامسة", "price": "3", "distance": "8-9كم"},
        {"area": "حي الفرات", "price": "3", "distance": "9-10كم"},
        {"area": "الجادرية", "price": "3", "distance": "9-10كم"},
        {"area": "جامعة بغداد", "price": "3", "distance": "10-11كم"},
        {"area": "جامعة الفراهيدي", "price": "3", "distance": "10-11كم"},
        {"area": "حي الاطباء", "price": "3", "distance": "10-12كم"},
    ],
    "بسمايه": [
        {"area": "كل المنطقة", "price": "1", "distance": "كل المنطقة"},
    ],
}

PRICE_LABELS = {
    "0": "مجاني 🎁",
    "1": "1,000 دينار",
    "2": "2,000 دينار",
    "3": "3,000 دينار",
}

def normalize(text):
    text = re.sub(r'[أإآا]', 'ا', text)
    text = re.sub(r'[ةه]', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

def search_area(query):
    norm_q = normalize(query)
    results = []
    for branch, areas in DATA.items():
        for item in areas:
            if norm_q in normalize(item["area"]):
                results.append({**item, "branch": branch})
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    branches_list = "\n".join([f"• {b}" for b in DATA.keys()])
    await update.message.reply_text(
        "🚚 *مرحبا بك في بوت التوصيل!*\n\n"
        "اكتب اسم المنطقة وراح أعطيك:\n"
        "📍 الفرع الأقرب\n"
        "💰 سعر التوصيل\n"
        "📏 المسافة\n"
        "🗺️ رابط خريطة\n\n"
        f"*الأفرع المتوفرة:*\n{branches_list}\n\n"
        "مثال: اكتب *الكراده* أو *المنصور*",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    results = search_area(query)

    if not results:
        await update.message.reply_text(
            f"❌ ما لكيت نتيجة لـ *{query}*\n\n"
            "جرب كلمة ثانية أو جزء من الاسم\n"
            "مثال: بدل *شارع المنصور* اكتب *المنصور* بس",
            parse_mode="Markdown"
        )
        return

    if len(results) == 1:
        await send_result(update, results[0])
        return

    if len(results) <= 8:
        keyboard = []
        for i, r in enumerate(results):
            keyboard.append([InlineKeyboardButton(
                f"{r['area']} — {r['branch']}",
                callback_data=f"area_{i}_{query}"
            )])
        context.user_data[f"results_{query}"] = results
        await update.message.reply_text(
            f"🔍 لكيت *{len(results)}* نتائج لـ *{query}*، اختار الأقرب:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        text = f"🔍 لكيت *{len(results)}* نتيجة لـ *{query}*:\n\n"
        for r in results[:10]:
            price = PRICE_LABELS.get(r['price'], r['price'])
            text += f"📍 *{r['area']}*\n"
            text += f"   الفرع: {r['branch']} | {price} | {r['distance']}\n\n"
        if len(results) > 10:
            text += f"_...و {len(results)-10} نتيجة أخرى، دق أكثر للبحث_"
        await update.message.reply_text(text, parse_mode="Markdown")

async def send_result(update_or_query, item, is_callback=False):
    price = PRICE_LABELS.get(item['price'], item['price'])
    map_url = f"https://www.google.com/maps/search/{item['area'].replace(' ', '+')}+بغداد+العراق"

    text = (
        f"📍 *{item['area']}*\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏪 *الفرع:* {item['branch']}\n"
        f"💰 *سعر التوصيل:* {price}\n"
        f"📏 *المسافة:* {item['distance']}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🗺️ [افتح على خريطة Google]({map_url})"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗺️ Google Maps", url=map_url)],
        [InlineKeyboardButton("🔍 بحث ثاني", callback_data="new_search")]
    ])

    if is_callback:
        await update_or_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update_or_query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "new_search":
        await query.edit_message_text("اكتب اسم المنطقة الجديدة 👇")
        return

    if query.data.startswith("area_"):
        parts = query.data.split("_", 2)
        idx = int(parts[1])
        search_key = parts[2]
        results = context.user_data.get(f"results_{search_key}", [])
        if idx < len(results):
            await send_result(query, results[idx], is_callback=True)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
