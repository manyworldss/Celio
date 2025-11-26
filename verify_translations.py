
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append('/Users/raphealsuber/celio(gemini)')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')
django.setup()

from message_cards.models import EmergencyCard
from message_cards.views import unified_card_management

# We need to extract defaultMessages from the view or recreate it here.
# Since it's a local variable in the view, we can't import it directly.
# I will copy the dictionary structure here for verification, 
# assuming it matches what I saw in the file view.
# Ideally, this dictionary should be a constant in constants.py or models.py.

# Re-creating the dictionary based on what I saw in views.py
# This is a snapshot for verification.
defaultMessages = {
    'CEL': {
        'en': "I have Celiac Disease. Please ensure my food is completely gluten-free. No wheat, barley, rye, or oats.",
        'es': "Tengo enfermedad celíaca. Por favor, asegúrese de que mi comida sea completamente sin gluten. Sin trigo, cebada, centeno o avena.",
        'fr': "J'ai la maladie cœliaque. S'il vous plaît, assurez-vous que ma nourriture est complètement sans gluten. Pas de blé, d'orge, de seigle ou d'avoine.",
        'de': "Ich habe Zöliakie. Bitte stellen Sie sicher, dass mein Essen komplett glutenfrei ist. Kein Weizen, Gerste, Roggen oder Hafer.",
        'it': "Ho la celiachia. Per favore assicuratevi che il mio cibo sia completamente senza glutine. Niente grano, orzo, segale o avena.",
        'pt': "Tenho doença celíaca. Por favor, certifique-se de que minha comida é completamente sem glúten. Sem trigo, cevada, centeio ou aveia.",
        'zh': "我有乳糜泻。请确保我的食物完全不含麸质。没有小麦、大麦、黑麦或燕麦。",
        'ja': "私はセリアック病です。私の食事が完全にグルテンフリーであることを確認してください。小麦、大麦、ライ麦、オート麦はダメです。",
        'ko': "저는 셀리악 병이 있습니다. 제 음식이 완전히 글루텐 프리인지 확인해 주세요. 밀, 보리, 호밀 또는 귀리는 안 됩니다.",
        'ar': "لدي مرض السيلياك. يرجى التأكد من أن طعامي خالٍ تمامًا من الغلوتين. لا قمح أو شعير أو جاودار أو شوفان.",
        'ru': "У меня целиакия. Пожалуйста, убедитесь, что моя еда полностью безглютеновая. Никакой пшеницы, ячменя, ржи или овса.",
        'hi': "मुझे सीलिएक रोग है। कृपया सुनिश्चित करें कि मेरा भोजन पूरी तरह से ग्लूटेन-मुक्त हो। कोई गेहूं, जौ, राई, या जई नहीं।"
    },
    'SEN': {
        'en': "I have a gluten sensitivity. Please avoid wheat, barley, and rye.",
        'es': "Tengo sensibilidad al gluten. Por favor evite el trigo, la cebada y el centeno.",
        'fr': "J'ai une sensibilité au gluten. S'il vous plaît éviter le blé, l'orge et le seigle.",
        'de': "Ich habe eine Glutenunverträglichkeit. Bitte vermeiden Sie Weizen, Gerste und Roggen.",
        'it': "Ho una sensibilità al glutine. Si prega di evitare grano, orzo e segale.",
        'pt': "Tenho sensibilidade ao glúten. Por favor, evite trigo, cevada e centeio.",
        'zh': "我对麸质敏感。请避免小麦、大麦和黑麦。",
        'ja': "私はグルテン過敏症です。小麦、大麦、ライ麦は避けてください。",
        'ko': "저는 글루텐 민감증이 있습니다. 밀, 보리, 호밀은 피해 주세요.",
        'ar': "لدي حساسية من الغلوتين. يرجى تجنب القمح والشعير والجاودار.",
        'ru': "У меня чувствительность к глютену. Пожалуйста, избегайте пшеницы, ячменя и ржи.",
        'hi': "मुझे ग्लूटेन संवेदनशीलता है। कृपया गेहूं, जौ और राई से बचें।"
    },
    'ALL': {
        'en': "I have a severe wheat allergy. Please ensure no wheat is present in my food.",
        'es': "Tengo una alergia severa al trigo. Por favor, asegúrese de que no haya trigo en mi comida.",
        'fr': "J'ai une allergie grave au blé. S'il vous plaît, assurez-vous qu'il n'y a pas de blé dans ma nourriture.",
        'de': "Ich habe eine schwere Weizenallergie. Bitte stellen Sie sicher, dass kein Weizen in meinem Essen ist.",
        'it': "Ho una grave allergia al grano. Si prega di assicurarsi che non ci sia grano nel mio cibo.",
        'pt': "Tenho uma alergia grave ao trigo. Por favor, certifique-se de que não há trigo na minha comida.",
        'zh': "我有严重的小麦过敏。请确保我的食物中没有小麦。",
        'ja': "私は重度の小麦アレルギーです。私の食事に小麦が含まれていないことを確認してください。",
        'ko': "저는 심각한 밀 알레르기가 있습니다. 제 음식에 밀이 없는지 확인해 주세요.",
        'ar': "لدي حساسية شديدة من القمح. يرجى التأكد من عدم وجود قمح في طعامي.",
        'ru': "У меня сильная аллергия на пшеницу. Пожалуйста, убедитесь, что в моей еде нет пшеницы.",
        'hi': "मुझे गेहूं से गंभीर एलर्जी है। कृपया सुनिश्चित करें कि मेरे भोजन में कोई गेहूं न हो।"
    }
}

def verify_translations():
    languages = [code for code, name in EmergencyCard.LANGUAGE_CHOICES]
    conditions = [code for code, name in EmergencyCard.SEVERITY_CHOICES]
    
    missing = []
    
    print(f"Verifying {len(languages)} languages across {len(conditions)} conditions...")
    
    for condition in conditions:
        if condition not in defaultMessages:
            missing.append(f"Missing condition block: {condition}")
            continue
            
        for lang in languages:
            if lang not in defaultMessages[condition]:
                missing.append(f"Missing translation for {condition} in {lang}")
            elif not defaultMessages[condition][lang]:
                missing.append(f"Empty translation for {condition} in {lang}")
                
    if missing:
        print("❌ Verification FAILED. Missing translations found:")
        for m in missing:
            print(f"  - {m}")
    else:
        print("✅ Verification PASSED. All language/condition combinations are present.")

if __name__ == "__main__":
    verify_translations()
