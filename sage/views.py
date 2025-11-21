from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.http import HttpResponse
import re

# Pre-cached responses for the demo version
DEMO_RESPONSES = {
    # Travel Guide Cards - Italy
    "italy|italian|rome|milan|venice|florence|naples": 
        """<div class="travel-card max-w-md my-5">
            <div class="relative h-40" style="background: linear-gradient(135deg, #059669 0%, #10b981 50%, #dc2626 100%);">
                <div class="absolute inset-0 bg-black/40"></div>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center z-10">
                    <div class="px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30 mb-3">
                        <span class="text-xs font-bold text-white tracking-widest">IT</span>
                    </div>
                    <h3 class="text-4xl font-bold text-white tracking-tight">ITALY</h3>
                </div>
            </div>
            <div class="p-6 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-white/10">
                    <span class="text-xs font-bold uppercase tracking-wider text-white/40">Celiac Awareness</span>
                    <div class="flex gap-1.5">
                        <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-400"></div>
                    </div>
                </div>
                
                <p class="text-white/90 text-sm leading-relaxed"><strong class="text-white">Paradise for celiacs!</strong> Italy has exceptional awareness, government-subsidized GF food, and strict labeling laws. Look for the AIC certification logo.</p>
                
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Must Try</div>
                        <div class="text-sm font-medium text-white">GF Pizza & Pasta</div>
                    </div>
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Language</div>
                        <div class="text-sm font-medium text-white">Italian</div>
                    </div>
                </div>
                
                <div class="bg-violet-500/10 border border-violet-500/30 rounded-lg p-4">
                    <div class="text-xs text-violet-300 uppercase mb-2 font-bold">Useful Phrase</div>
                    <div class="text-sm font-semibold text-white italic">"Sono celiaco/a"</div>
                    <div class="text-xs text-white/50 mt-1">(I am celiac)</div>
                </div>
                
                <div class="text-center py-3 bg-white/5 rounded-lg border border-white/5">
                    <span class="text-xs text-white/30">Full detailed guides coming soon</span>
                </div>
            </div>
        </div>""",
    
    # Travel Guide Cards - France
    "france|french|paris|lyon|marseille|nice": 
        """<div class="travel-card max-w-md my-5">
            <div class="relative h-40" style="background: linear-gradient(135deg, #1e3a8a 0%, #ffffff 50%, #dc2626 100%);">
                <div class="absolute inset-0 bg-black/40"></div>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center z-10">
                    <div class="px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30 mb-3">
                        <span class="text-xs font-bold text-white tracking-widest">FR</span>
                    </div>
                    <h3 class="text-4xl font-bold text-white tracking-tight">FRANCE</h3>
                </div>
            </div>
            <div class="p-6 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-white/10">
                    <span class="text-xs font-bold uppercase tracking-wider text-white/40">Celiac Awareness</span>
                    <div class="flex gap-1.5">
                        <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                        <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                        <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
                        <div class="w-3 h-3 rounded-full bg-gray-600"></div>
                        <div class="w-3 h-3 rounded-full bg-gray-600"></div>
                    </div>
                </div>
                
                <p class="text-white/90 text-sm leading-relaxed"><strong class="text-white">Growing awareness!</strong> The AFDIAG association provides helpful resources. Look for "sans gluten" options, but always communicate your needs clearly.</p>
                
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Must Try</div>
                        <div class="text-sm font-medium text-white">GF Crêpes</div>
                    </div>
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Language</div>
                        <div class="text-sm font-medium text-white">French</div>
                    </div>
                </div>
                
                <div class="bg-violet-500/10 border border-violet-500/30 rounded-lg p-4">
                    <div class="text-xs text-violet-300 uppercase mb-2 font-bold">Useful Phrase</div>
                    <div class="text-sm font-semibold text-white italic">"Je suis cœliaque"</div>
                    <div class="text-xs text-white/50 mt-1">(I am celiac)</div>
                </div>
                
                <div class="bg-orange-500/10 border border-orange-500/30 rounded-lg p-3">
                    <span class="block text-xs text-orange-200 font-medium">Tip: Be cautious with sauces and soups!</span>
                </div>
                
                <div class="text-center py-3 bg-white/5 rounded-lg border border-white/5">
                    <span class="text-xs text-white/30">Full detailed guides coming soon</span>
                </div>
            </div>
        </div>""",
    
    # Travel Guide Cards - Japan
    "japan|japanese|tokyo|kyoto|osaka|hiroshima": 
        """<div class="travel-card max-w-md my-5">
            <div class="relative h-40" style="background: linear-gradient(180deg, #BC002D 0%, #FFFFFF 50%, #FFFFFF 100%);">
                <div class="absolute inset-0 bg-black/50"></div>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center z-10">
                    <div class="px-4 py-1.5 bg-white/20 backdrop-blur-sm rounded-lg border border-white/30 mb-3">
                        <span class="text-xs font-bold text-white tracking-widest">JP</span>
                    </div>
                    <h3 class="text-4xl font-bold text-white tracking-tight">JAPAN</h3>
                </div>
            </div>
            <div class="p-6 space-y-4">
                <div class="flex items-center justify-between pb-3 border-b border-white/10">
                    <span class="text-xs font-bold uppercase tracking-wider text-white/40">Celiac Awareness</span>
                    <div class="flex gap-1.5">
                        <div class="w-3 h-3 rounded-full bg-orange-400"></div>
                        <div class="w-3 h-3 rounded-full bg-orange-400"></div>
                        <div class="w-3 h-3 rounded-full bg-gray-600"></div>
                        <div class="w-3 h-3 rounded-full bg-gray-600"></div>
                        <div class="w-3 h-3 rounded-full bg-gray-600"></div>
                    </div>
                </div>
                
                <p class="text-white/90 text-sm leading-relaxed"><strong class="text-white">Challenging but doable!</strong> Lower celiac awareness. Soy sauce contains wheat and is in many dishes. Language barriers exist, but preparation helps!</p>
                
                <div class="grid grid-cols-2 gap-3">
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Safe Option</div>
                        <div class="text-sm font-medium text-white">Sashimi & Rice</div>
                    </div>
                    <div class="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-violet-500/10 hover:border-violet-500/30 transition-all">
                        <div class="text-xs text-white/40 uppercase mb-1 font-semibold">Language</div>
                        <div class="text-sm font-medium text-white">Japanese</div>
                    </div>
                </div>
                
                <div class="bg-violet-500/10 border border-violet-500/30 rounded-lg p-4">
                    <div class="text-xs text-violet-300 uppercase mb-2 font-bold">Useful Phrase</div>
                    <div class="text-sm font-semibold text-white mb-1">私はセリアック病です</div>
                    <div class="text-xs text-white/50 italic">(Watashi wa seriakku byō desu)</div>
                    <div class="text-xs text-white/40 mt-1">"I have celiac disease"</div>
                </div>
                
                <div class="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                    <span class="block text-xs text-red-200 font-medium">Avoid: Ramen, tempura, soy sauce!</span>
                </div>
                
                <div class="text-center py-3 bg-white/5 rounded-lg border border-white/5">
                    <span class="text-xs text-white/30">Full detailed guides coming soon</span>
                </div>
            </div>
        </div>""",
    
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
        messages = conversation.messages.all().order_by('created_at')
        current_conversation = conversation
    
    # Handle new message submission
    if request.method == 'POST' and 'message' in request.POST:
        user_message = request.POST.get('message').strip()
        
        if user_message:
            # Generate response using demo cached responses based on keywords
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
                messages = request.session['demo_messages']
                
                # If HTMX request, return just the messages
                if request.headers.get('HX-Request'):
                    return render(request, 'sage/partials/messages.html', {
                        'messages': messages
                    })
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
                
                # If HTMX request, return just the messages
                if request.headers.get('HX-Request'):
                    return render(request, 'sage/partials/messages.html', {
                        'messages': current_conversation.messages.all().order_by('created_at')
                    })
    
    return render(request, 'sage/assistant.html', {
        'conversations': conversations,
        'current_conversation': current_conversation if request.user.is_authenticated else None,
        'messages': messages,
    })

# Function to match user query to pre-made responses
def get_demo_response(query):
    # Convert query to lowercase for easier matching
    query = query.lower()
    
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
