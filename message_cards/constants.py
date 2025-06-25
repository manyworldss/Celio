"""
Constants for the Message Cards app, including predefined messages for different conditions
in multiple languages.
"""

# Predefined messages by condition and language
PREDEFINED_MESSAGES = {
    'CEL': {  # Celiac Disease
        'en': (
            "I have celiac disease, an autoimmune condition that requires me to avoid all gluten. "
            "Even trace amounts of gluten can make me extremely ill. "
            "If needed, please ensure all food and medication is gluten-free."
        ),
        'es': (
            "Tengo enfermedad celíaca, una condición autoinmune que me obliga a evitar todo el gluten. "
            "Incluso cantidades mínimas de gluten pueden enfermarme gravemente. "
            "En caso de emergencia, asegúrese de que todos los alimentos y medicamentos sean sin gluten."
        ),
        'fr': (
            "Je souffre de maladie cœliaque, une maladie auto-immune qui m'oblige à éviter tout gluten. "
            "Même des traces de gluten peuvent me rendre extrêmement malade. "
            "En cas d'urgence, veuillez vous assurer que tous les aliments et médicaments sont sans gluten."
        ),
        'de': (
            "Ich habe Zöliakie, eine Autoimmunerkrankung, die es erfordert, dass ich jegliches Gluten vermeide. "
            "Selbst Spuren von Gluten können mich sehr krank machen. "
            "Im Notfall stellen Sie bitte sicher, dass alle Lebensmittel und Medikamente glutenfrei sind."
        ),
        'it': (
            "Ho la celiachia, una condizione autoimmune che mi costringe a evitare tutto il glutine. "
            "Anche tracce di glutine possono farmi stare molto male. "
            "In caso di emergenza, assicurati che tutti gli alimenti e i farmaci siano senza glutine."
        ),
        'pt': (
            "Tenho doença celíaca, uma condição autoimune que me obriga a evitar todo o glúten. "
            "Mesmo quantidades mínimas de glúten podem me deixar extremamente doente. "
            "Em caso de emergência, certifique-se de que todos os alimentos e medicamentos sejam sem glúten."
        ),
        'ja': (
            "私はセリアック病（自己免疫疾患）を持っており、すべてのグルテンを避ける必要があります。"
            "微量のグルテンでも非常に体調が悪くなることがあります。"
            "緊急時には、すべての食べ物や薬がグルテンフリーであることを確認してください。"
        ),
        'zh': (
            "我患有乳糜泻，这是一种自身免疫性疾病，需要我避免所有麸质。"
            "即使是微量的麸质也会让我极度不适。"
            "在紧急情况下，请确保所有食物和药物都不含麸质。"
        )
    },
    'SEN': {  # Gluten Sensitive
        'en': (
            "I have non-celiac gluten sensitivity. Consuming gluten causes significant discomfort and health issues. "
            "Please ensure my food and medication are gluten-free whenever possible."
        ),
        'es': (
            "Tengo sensibilidad al gluten no celíaca. Consumir gluten me causa malestar significativo y problemas de salud. "
            "Por favor, asegúrese de que mis alimentos y medicamentos sean sin gluten siempre que sea posible."
        ),
        'fr': (
            "J'ai une sensibilité au gluten non cœliaque. La consommation de gluten provoque un inconfort important et des problèmes de santé. "
            "Veuillez vous assurer que mes aliments et médicaments sont sans gluten dans la mesure du possible."
        ),
        'de': (
            "Ich habe eine Nicht-Zöliakie-Glutensensitivität. Der Verzehr von Gluten verursacht erhebliche Beschwerden und gesundheitliche Probleme. "
            "Bitte stellen Sie sicher, dass meine Lebensmittel und Medikamente wann immer möglich glutenfrei sind."
        ),
        'it': (
            "Ho una sensibilità al glutine non celiaca. Consumare glutine mi causa notevole disagio e problemi di salute. "
            "Per favore, assicurati che il mio cibo e i farmaci siano senza glutine quando possibile."
        ),
        'pt': (
            "Tenho sensibilidade ao glúten não celíaca. Consumir glúten causa desconforto significativo e problemas de saúde. "
            "Por favor, certifique-se de que minha comida e medicamentos sejam sem glúten sempre que possível."
        ),
        'ja': (
            "私は非セリアックグルテン過敏症です。グルテンを摂取すると、著しい不快感や健康上の問題が生じます。"
            "可能な限り、食べ物や薬がグルテンフリーであることを確認してください。"
        ),
        'zh': (
            "我有非乳糜泻麸质敏感症。摄入麸质会导致明显的不适和健康问题。"
            "请尽可能确保我的食物和药物不含麸质。"
        )
    },
    'ALL': {  # Wheat/Gluten Allergy
        'en': (
            "I have a wheat/gluten allergy. Exposure can cause a severe allergic reaction that may require medical attention. "
            "Please ensure all my food and medication is completely free of wheat and gluten."
        ),
        'es': (
            "Tengo alergia al trigo/gluten. La exposición puede causar una reacción alérgica grave que puede requerir atención médica de emergencia. "
            "Por favor, asegúrese de que todos mis alimentos y medicamentos estén completamente libres de trigo y gluten."
        ),
        'fr': (
            "J'ai une allergie au blé/gluten. L'exposition peut provoquer une réaction allergique grave nécessitant des soins médicaux d'urgence. "
            "Veuillez vous assurer que tous mes aliments et médicaments sont complètement exempts de blé et de gluten."
        ),
        'de': (
            "Ich habe eine Weizen-/Glutenallergie. Der Kontakt kann eine schwere allergische Reaktion auslösen, die eine notärztliche Behandlung erfordern kann. "
            "Bitte stellen Sie sicher, dass alle meine Lebensmittel und Medikamente vollständig frei von Weizen und Gluten sind."
        ),
        'it': (
            "Ho un'allergia al grano/glutine. L'esposizione può causare una grave reazione allergica che potrebbe richiedere cure mediche di emergenza. "
            "Si prega di assicurarsi che tutti i miei alimenti e farmaci siano completamente privi di grano e glutine."
        ),
        'pt': (
            "Tenho alergia a trigo/glúten. A exposição pode causar uma reação alérgica grave que pode exigir atenção médica de emergência. "
            "Por favor, certifique-se de que todos os meus alimentos e medicamentos sejam completamente livres de trigo e glúten."
        ),
        'ja': (
            "私は小麦/グルテンアレルギーがあります。接触すると、緊急医療が必要な重度のアレルギー反応を引き起こす可能性があります。"
            "すべての食べ物と薬が完全に小麦とグルテンを含まないようにしてください。"
        ),
        'zh': (
            "我对小麦/麸质过敏。接触可能导致严重的过敏反应，可能需要紧急医疗救助。"
            "请确保我所有的食物和药物完全不含小麦和麸质。"
        )
    }
}

# Medical information bullet points by condition for each language
MEDICAL_INFO_BULLETS = {
    'CEL': {  # Celiac Disease
        'en': [
            "Autoimmune disorder triggered by gluten",
            "Must maintain strict gluten-free diet",
            "Damage to small intestine can occur with any exposure",
            "Heightened risk for nutritional deficiencies",
            "Cross-contamination must be avoided"
        ],
        'es': [
            "Trastorno autoinmune desencadenado por el gluten",
            "Debe mantener una dieta estricta sin gluten",
            "Puede ocurrir daño al intestino delgado con cualquier exposición",
            "Mayor riesgo de deficiencias nutricionales",
            "Debe evitarse la contaminación cruzada"
        ],
        'fr': [
            "Maladie auto-immune déclenchée par le gluten",
            "Doit maintenir un régime sans gluten strict",
            "Des lésions de l'intestin grêle peuvent survenir avec toute exposition",
            "Risque accru de carences nutritionnelles",
            "La contamination croisée doit être évitée"
        ],
        'de': [
            "Autoimmunerkrankung, ausgelöst durch Gluten",
            "Strikte glutenfreie Diät muss eingehalten werden",
            "Schäden am Dünndarm können bei jeder Exposition auftreten",
            "Erhöhtes Risiko für Nährstoffmängel",
            "Kreuzkontamination muss vermieden werden"
        ],
        'it': [
            "Disturbo autoimmune innescato dal glutine",
            "Deve mantenere una dieta rigorosamente priva di glutine",
            "Possono verificarsi danni all'intestino tenue con qualsiasi esposizione",
            "Maggiore rischio di carenze nutrizionali",
            "La contaminazione incrociata deve essere evitata"
        ],
        'pt': [
            "Distúrbio autoimune desencadeado pelo glúten",
            "Deve manter dieta estritamente sem glúten",
            "Danos ao intestino delgado podem ocorrer com qualquer exposição",
            "Risco aumentado de deficiências nutricionais",
            "A contaminação cruzada deve ser evitada"
        ],
        'ja': [
            "グルテンによって引き起こされる自己免疫疾患",
            "厳格なグルテンフリー食を維持する必要がある",
            "どのような曝露でも小腸へのダメージが起こりうる",
            "栄養不足のリスクが高まる",
            "交差汚染を避ける必要がある"
        ],
        'zh': [
            "由麸质触发的自身免疫性疾病",
            "必须保持严格的无麸质饮食",
            "任何接触都可能导致小肠损伤",
            "营养不良风险增加",
            "必须避免交叉污染"
        ]
    },
    'SEN': {  # Gluten Sensitive
        'en': [
            "Non-celiac gluten sensitivity",
            "Intestinal and extra-intestinal symptoms",
            "No intestinal damage but significant discomfort",
            "Symptoms improve on gluten-free diet",
            "May have other food sensitivities"
        ],
        'es': [
            "Sensibilidad al gluten no celíaca",
            "Síntomas intestinales y extraintestinales",
            "Sin daño intestinal pero malestar significativo",
            "Los síntomas mejoran con una dieta sin gluten",
            "Puede tener otras sensibilidades alimentarias"
        ],
        'fr': [
            "Sensibilité au gluten non cœliaque",
            "Symptômes intestinaux et extra-intestinaux",
            "Pas de lésions intestinales mais inconfort important",
            "Les symptômes s'améliorent avec un régime sans gluten",
            "Peut présenter d'autres sensibilités alimentaires"
        ],
        'de': [
            "Nicht-Zöliakie-Glutensensitivität",
            "Intestinale und extraintestinale Symptome",
            "Keine Darmschäden, aber erhebliche Beschwerden",
            "Symptome verbessern sich bei glutenfreier Ernährung",
            "Kann andere Nahrungsmittelempfindlichkeiten haben"
        ],
        'it': [
            "Sensibilità al glutine non celiaca",
            "Sintomi intestinali ed extra-intestinali",
            "Nessun danno intestinale ma disagio significativo",
            "I sintomi migliorano con una dieta priva di glutine",
            "Può avere altre sensibilità alimentari"
        ],
        'pt': [
            "Sensibilidade ao glúten não celíaca",
            "Sintomas intestinais e extra-intestinais",
            "Sem danos intestinais, mas desconforto significativo",
            "Os sintomas melhoram com uma dieta sem glúten",
            "Pode ter outras sensibilidades alimentares"
        ],
        'ja': [
            "非セリアックグルテン過敏症",
            "腸内および腸外の症状",
            "腸の損傷はないが著しい不快感",
            "グルテンフリー食で症状が改善",
            "他の食物感受性を持つ可能性がある"
        ],
        'zh': [
            "非乳糜泻麸质敏感症",
            "肠道和肠外症状",
            "无肠道损伤但有明显不适",
            "无麸质饮食可改善症状",
            "可能有其他食物敏感性"
        ]
    },
    'ALL': {  # Wheat/Gluten Allergy
        'en': [
            "Immune response to wheat/gluten proteins",
            "Can cause immediate allergic reactions",
            "May include difficulty breathing or anaphylaxis",
            "Requires complete avoidance of wheat products",
            "Medication may be necessary"
        ],
        'es': [
            "Respuesta inmune a las proteínas del trigo/gluten",
            "Puede causar reacciones alérgicas inmediatas",
            "Puede incluir dificultad para respirar o anafilaxia",
            "Requiere evitar completamente los productos de trigo",
            "Puede ser necesaria medicación de emergencia"
        ],
        'fr': [
            "Réponse immunitaire aux protéines de blé/gluten",
            "Peut provoquer des réactions allergiques immédiates",
            "Peut inclure des difficultés respiratoires ou une anaphylaxie",
            "Nécessite d'éviter complètement les produits à base de blé",
            "Un médicament d'urgence peut être nécessaire"
        ],
        'de': [
            "Immunantwort auf Weizen-/Glutenproteine",
            "Kann sofortige allergische Reaktionen auslösen",
            "Kann Atembeschwerden oder Anaphylaxie umfassen",
            "Erfordert vollständige Vermeidung von Weizenprodukten",
            "Notfallmedikation kann erforderlich sein"
        ],
        'it': [
            "Risposta immunitaria alle proteine del grano/glutine",
            "Può causare reazioni allergiche immediate",
            "Può includere difficoltà respiratorie o anafilassi",
            "Richiede la completa eliminazione dei prodotti a base di grano",
            "Potrebbe essere necessario un farmaco di emergenza"
        ],
        'pt': [
            "Resposta imune às proteínas do trigo/glúten",
            "Pode causar reações alérgicas imediatas",
            "Pode incluir dificuldade para respirar ou anafilaxia",
            "Requer a completa evitação de produtos de trigo",
            "Medicação de emergência pode ser necessária"
        ],
        'ja': [
            "小麦/グルテンタンパク質に対する免疫反応",
            "即時アレルギー反応を引き起こす可能性がある",
            "呼吸困難やアナフィラキシーを含む場合がある",
            "小麦製品の完全な回避が必要",
            "緊急薬が必要な場合がある"
        ],
        'zh': [
            "对小麦/麸质蛋白的免疫反应",
            "可引起即时过敏反应",
            "可能包括呼吸困难或过敏性休克",
            "需要完全避免小麦产品",
            "可能需要紧急药物"
        ]
    }
}
