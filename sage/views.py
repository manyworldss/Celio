from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.http import HttpResponse
from django.template.loader import render_to_string
import re

# Travel Guide Data
TRAVEL_DATA = {
    "italy": {
        "name": "Italy",
        "code": "IT",
        "greeting": "Ciao!",
        "image_url": "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
        "awareness_level": 5,
        "language": "Italian",
        "overview": "Italy is a paradise for celiacs! With government-subsidized GF food and strict labeling laws, you'll find safe options almost everywhere. Look for the AIC (Italian Celiac Association) certification logo.",
        "safe_bets": ["Risotto (check broth)", "Polenta", "Grilled meats/fish", "Gelato (cup)"],
        "avoid": ["Breaded items", "Fried foods (shared oil)", "Pasta (unless GF)", "Pizza (unless GF)"],
        "dining_tips": [
            "Look for the 'Senza Glutine' sign",
            "Pharmacies sell high-quality GF bread/pasta",
            "Most gelaterias have GF cones or cups",
            "Always mention 'Sono celiaco' to your waiter"
        ],
        "apps": ["Mangiare Senza Glutine", "AIC Mobile"],
        "phrases": [
            {"english": "I am celiac", "native": "Sono celiaco/a", "pronunciation": "So-no che-lee-ah-ko"},
            {"english": "Is this gluten-free?", "native": "È senza glutine?", "pronunciation": "Eh sen-tsa gloo-tee-neh"},
            {"english": "Does this contain wheat?", "native": "Contiene grano?", "pronunciation": "Con-tyeh-neh grah-no"}
        ]
    },
    "france": {
        "name": "France",
        "code": "FR",
        "greeting": "Bonjour!",
        "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
        "awareness_level": 3,
        "language": "French",
        "overview": "Awareness is growing in France, especially in major cities like Paris. The AFDIAG association provides helpful resources. Always look for 'Sans Gluten' options.",
        "safe_bets": ["Macarons (usually GF)", "Buckwheat Galettes", "Cheese plates", "Omelettes"],
        "avoid": ["Baguettes/Croissants", "Sauces (roux-based)", "Fried foods", "Beer"],
        "dining_tips": [
            "Pharmacies are great for GF snacks",
            "Bio (organic) stores carry many GF brands",
            "Verify if 'sarrasin' (buckwheat) galettes are 100% buckwheat",
            "Confirm sauces are not thickened with flour"
        ],
        "apps": ["Gluten Free Roads", "Find Me Gluten Free"],
        "phrases": [
            {"english": "I am celiac", "native": "Je suis cœliaque", "pronunciation": "Zhuh swee say-lee-ak"},
            {"english": "I cannot eat gluten", "native": "Je ne peux pas manger de gluten", "pronunciation": "Zhuh nuh puh pah mahn-zhay duh gloo-ten"},
            {"english": "Wheat flour", "native": "Farine de blé", "pronunciation": "Fah-reen duh blay"}
        ]
    },
    "japan": {
        "name": "Japan",
        "code": "JP",
        "greeting": "Konnichiwa!",
        "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
        "awareness_level": 2,
        "language": "Japanese",
        "overview": "Japan can be challenging due to soy sauce (wheat) in many dishes. However, awareness is rising. Stick to simple grilled items and always carry a translation card.",
        "safe_bets": ["Sashimi (no soy sauce)", "Mochi (check ingredients)", "Edamame", "Yakitori (salt only)"],
        "avoid": ["Soy sauce (Shoyu)", "Ramen/Udon", "Tempura", "Miso soup (often has wheat)"],
        "dining_tips": [
            "Bring your own GF soy sauce (Tamari)",
            "Convenience stores (Konbini) have safe Onigiri (check labels)",
            "Kaiten-zushi (conveyor belt sushi) can be risky for cross-contamination",
            "Department store basements (Depachika) have high-quality fresh foods"
        ],
        "apps": ["Gluten Free Japan", "Google Translate (Camera)"],
        "phrases": [
            {"english": "I have celiac disease", "native": "私はセリアック病です", "pronunciation": "Watashi wa seriakku byō desu"},
            {"english": "No soy sauce please", "native": "醤油抜きでお願いします", "pronunciation": "Shoyu nuki de onegaishimasu"},
            {"english": "Wheat allergy", "native": "小麦アレルギー", "pronunciation": "Komugi arerugī"}
        ]
    }
}

# Pre-cached responses for the demo version
DEMO_RESPONSES = {
    # General travel query - show all three
    "travel guide|where to travel|travel tips|destination": 
        "I can help you with celiac-friendly travel guides!\n\n"
        "Try asking about specific destinations like:\n"
        "• Italy (excellent celiac awareness!)\n"
        "• France (growing awareness)\n"
        "• Japan (challenging but doable)\n\n"
        "Just say something like 'Tell me about traveling to Italy' or 'Japan travel guide' and I'll show you detailed information!",
    
    "restaurant|dining|eat out|waiter|menu": 
        "**Dining Out Safely with Celiac Disease**\n\n"
        "**Before You Go:**\n"
        "• Call ahead to verify gluten-free options\n"
        "• Use apps like Find Me Gluten-Free\n"
        "• Check restaurant reviews from other celiacs\n\n"
        "**At the Restaurant:**\n"
        "• Specify 'celiac disease' not just 'gluten-free preference'\n"
        "• Ask about cross-contamination protocols\n"
        "• Request dedicated preparation areas\n"
        "• Inquire about separate fryers for allergen-free items\n\n"
        "**Best Times:**\n"
        "• Dine during off-peak hours when staff can focus on your needs\n\n"
        "*Tip*: Even 'gluten-free menu' items can be unsafe if proper protocols aren't followed!",

    "travel|trip|vacation|abroad|country|flight|plane|hotel": 
        "**Traveling with Celiac Disease**\n\n"
        "**Before Your Trip:**\n"
        "• Research GF options at your destination\n"
        "• Download translation cards in local language\n"
        "• Join celiac travel groups for insider tips\n"
        "• Get a doctor's note (helpful for customs)\n\n"
        "**Packing Essentials:**\n"
        "• Emergency snacks (protein bars, crackers)\n"
        "• Portable allergen test kit\n"
        "• Medication for accidental exposure\n\n"
        "**Accommodation Tips:**\n"
        "• Book places with kitchen access\n"
        "• Research nearby GF grocery stores\n\n"
        "*Ask me about specific countries for detailed guides!*",
    
    "symptom|reaction|sick|pain|bloat|diarrhea|headache|rash|fatigue|gluten exposure": 
        "**Gluten Exposure & Symptoms**\n\n"
        "**Common Symptoms Include:**\n"
        "• Digestive: Bloating, diarrhea, constipation, stomach pain\n"
        "• Energy: Extreme fatigue, weakness\n"
        "• Mental: Brain fog, headaches, mood changes\n"
        "• Physical: Joint pain, skin rashes (DH)\n"
        "• Other: Anemia, nutritional deficiencies\n\n"
        "**If You've Been Exposed:**\n"
        "• Stay hydrated (water, electrolytes)\n"
        "• Rest and be gentle with yourself\n"
        "• Stick to simple, safe foods\n"
        "• Follow your doctor's recommendations\n\n"
        "Symptoms typically resolve in a few days to weeks.",
    
    "food|ingredient|safe|avoid|label|product|grocery|what can i eat": 
        "**Safe vs. Unsafe Foods**\n\n"
        "**Always Avoid:**\n"
        "• Wheat (all types: durum, semolina, spelt, kamut)\n"
        "• Rye and barley\n"
        "• Most oats (unless certified GF)\n"
        "• Malt and malt flavoring\n"
        "• Many processed foods with hidden gluten\n\n"
        "**Safe to Eat:**\n"
        "• Fresh fruits and vegetables\n"
        "• Unprocessed meats, fish, poultry\n"
        "• Most dairy products\n"
        "• Beans, legumes, nuts\n"
        "• GF grains: rice, corn, quinoa, millet\n"
        "• Certified gluten-free oats\n\n"
        "**Always** read labels carefully and look for certified GF symbols!",
    
    "cross contamination|kitchen|prepare|cook|utensil|toaster|cutting board": 
        "**Preventing Cross-Contamination**\n\n"
        "**Essential Kitchen Practices:**\n\n"
        "**Separate Equipment:**\n"
        "• Dedicated cutting boards\n"
        "• Separate toaster (or toaster bags)\n"
        "• Individual utensils\n"
        "• Distinct colanders and strainers\n\n"
        "**Storage Tips:**\n"
        "• GF products on UPPER shelves\n"
        "• Dedicated containers for condiments\n"
        "• Clear labeling system\n\n"
        "**Cleaning:**\n"
        "• Thoroughly clean surfaces before GF prep\n"
        "• Use separate sponges/cloths\n\n"
        "Even *tiny* amounts of gluten can trigger reactions!",
    
    "family|gene|genetic|hereditary|parent|child|test|diagnose|diagnosis": 
        "**Celiac Disease & Genetics**\n\n"
        "**Family Connection:**\n"
        "• First-degree relatives: 1 in 10 risk\n"
        "• Requires HLA-DQ2 or HLA-DQ8 genes\n"
        "• 40% of people have these genes (not all develop celiac)\n"
        "• Environmental triggers: infections, stress, pregnancy\n\n"
        "**Diagnosis Process:**\n"
        "1. Blood tests (antibody screening)\n"
        "2. Small intestine biopsy\n"
        "3. Genetic testing (to rule out)\n\n"
        "**Important**: Get tested *before* going gluten-free, even without symptoms!\n\n"
        "Early detection prevents long-term complications.",
    
    "hello|hi|hey|greetings|start|intro|welcome":
        "**Hello! I'm Sage** - Your personal celiac & gluten-free assistant!\n\n"
        "I'm here to help with:\n\n"
        "**Travel Guides** - Italy, France, Japan & more\n"
        "**Dining Out** - Restaurant strategies & safety\n"
        "**Health Info** - Symptoms, diagnosis, management\n"
        "**Food Safety** - What to eat, what to avoid\n"
        "**Cross-Contamination** - Kitchen best practices\n\n"
        "Try asking:\n"
        "• 'Tell me about traveling to Italy'\n"
        "• 'How do I eat safely at restaurants?'\n"
        "• 'What foods should I avoid?'\n\n"
        "*This is a demo with pre-made responses - full AI coming soon!*",
        
    "default":
        "I'm still learning!\n\n"
        "**I can help with:**\n"
        "Travel guides (Italy, France, Japan)\n"
        "Restaurant dining strategies\n"
        "Symptom management\n"
        "Safe vs unsafe foods\n"
        "Genetic/family information\n"
        "Cross-contamination prevention\n\n"
        "Try asking about one of these topics!\n\n"
        "*Premium version with full Claude AI integration coming soon!*"
}

def sage_assistant(request):
    # For demo mode, use session-based messages instead of database
    chat_messages = []
    if not request.user.is_authenticated:
        # Demo mode for unauthenticated users
        if 'demo_messages' not in request.session:
            request.session['demo_messages'] = []
        
        messages = request.session['demo_messages']
        conversations = []  # No conversations in demo mode
        current_conversation = None
    else:
        # Authenticated user logic (existing functionality)
        conversation_id = request.GET.get('conversation')
        
        if conversation_id:
            try:
                conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            except:
                conversation = Conversation.objects.filter(user=request.user).order_by('-updated_at').first()
        else:
            conversation = Conversation.objects.filter(user=request.user).order_by('-updated_at').first()
        
        if not conversation:
            conversation = Conversation.objects.create(
                user=request.user,
                title="Welcome to Sage!"
            )
            
            Message.objects.create(
                conversation=conversation,
                role="assistant",
                content="Hello! I'm Sage, your personal celiac and gluten-free assistant. How can I help you today?"
            )
        
        conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
        chat_messages = conversation.messages.all().order_by('created_at')
        current_conversation = conversation
    
    # Handle new message submission
    if request.method == 'POST':
        # Handle Clear Chat
        if 'clear_chat' in request.POST:
            if not request.user.is_authenticated:
                # Demo mode: clear session messages
                request.session['demo_messages'] = []
                request.session.modified = True
                chat_messages = []
            else:
                # Authenticated mode: clear database messages
                current_conversation.messages.all().delete()
                # Reset title
                current_conversation.title = "New Conversation"
                current_conversation.save()
                
                # Add welcome message back
                Message.objects.create(
                    conversation=current_conversation,
                    role="assistant",
                    content="Hello! I'm Sage, your personal celiac and gluten-free assistant. How can I help you today?"
                )
                chat_messages = current_conversation.messages.all().order_by('created_at')

            # If HTMX request, return just the messages
            if request.headers.get('HX-Request'):
                return render(request, 'sage/partials/messages.html', {
                    'chat_messages': chat_messages
                })
            return redirect('sage:assistant')

        # Handle User Message
        user_message = request.POST.get('message')
        if user_message:
            response_text = get_demo_response(user_message)
            
            if not request.user.is_authenticated:
                # Demo mode: use session storage
                request.session['demo_messages'].append({
                    'role': 'user',
                    'content': user_message
                })
                request.session['demo_messages'].append({
                    'role': 'assistant', 
                    'content': response_text
                })
                request.session.modified = True
                chat_messages = request.session['demo_messages']
            else:
                # Authenticated mode: use database
                Message.objects.create(
                    conversation=current_conversation,
                    role="user",
                    content=user_message
                )
                
                Message.objects.create(
                    conversation=current_conversation,
                    role="assistant",
                    content=response_text
                )
                
                # Update conversation title if it's the first user message
                if current_conversation.title == "Welcome to Sage!" or current_conversation.title == "New Conversation":
                    title = user_message[:30] + "..." if len(user_message) > 30 else user_message
                    current_conversation.title = title
                    current_conversation.save()
                
                chat_messages = current_conversation.messages.all().order_by('created_at')
            
            # If HTMX request, return just the messages
            if request.headers.get('HX-Request'):
                return render(request, 'sage/partials/messages.html', {
                    'chat_messages': chat_messages
                })
    
    return render(request, 'sage/assistant.html', {
        'conversations': conversations,
        'current_conversation': current_conversation if request.user.is_authenticated else None,
        'chat_messages': chat_messages,
    })

# Function to match user query to pre-made responses
def get_demo_response(query):
    # Convert query to lowercase for easier matching
    query = query.lower()
    
    # Check for specific country travel guides first
    if "italy" in query or "italian" in query or "rome" in query:
        return render_to_string('sage/partials/travel_guide_card.html', {'country': TRAVEL_DATA['italy']})
    
    if "france" in query or "french" in query or "paris" in query:
        return render_to_string('sage/partials/travel_guide_card.html', {'country': TRAVEL_DATA['france']})
        
    if "japan" in query or "japanese" in query or "tokyo" in query:
        return render_to_string('sage/partials/travel_guide_card.html', {'country': TRAVEL_DATA['japan']})
    
    # Check each keyword pattern against the query
    for keywords, response in DEMO_RESPONSES.items():
        # Use regex to check if any of the keywords match
        pattern = '\\b(' + keywords + ')\\b'
        if re.search(pattern, query, re.IGNORECASE):
            return response
    
    # If no specific matches, return the default response
    return DEMO_RESPONSES["default"]

def new_conversation(request):
    if not request.user.is_authenticated:
        # Demo mode: clear session messages
        request.session['demo_messages'] = []
        return redirect('sage:assistant')
    
    # Authenticated mode: create new conversation
    conversation = Conversation.objects.create(
        user=request.user,
        title="New Conversation"
    )
    
    Message.objects.create(
        conversation=conversation,
        role="assistant",
        content="Hello! I'm Sage, your personal celiac and gluten-free assistant. How can I help you today?"
    )
    return redirect('sage:assistant')

def delete_conversation(request, conversation_id):
    if not request.user.is_authenticated:
        # Demo mode: redirect back to assistant
        return redirect('sage:assistant')
    
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    if request.method == 'POST':
        conversation.delete()
    
    return redirect('sage:assistant')
