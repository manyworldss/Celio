from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.http import HttpResponse
import re

# Pre-cached responses for the demo version
DEMO_RESPONSES = {
    "restaurant|dining|eat|restaurant|waiter|menu": 
        "When dining at restaurants with celiac disease, always:\n\n"
        "1. Call ahead to check if they can accommodate gluten-free needs\n"
        "2. Clearly inform your server about your celiac disease (not just a preference)\n"
        "3. Ask about dedicated preparation areas and cross-contamination protocols\n"
        "4. Consider dining during off-peak hours when kitchen staff has more time to be careful\n"
        "5. Use apps like Find Me Gluten Free to locate celiac-friendly restaurants\n\n"
        "Remember that even 'gluten-free menu' items can be contaminated if proper protocols aren't followed.",
    
    "travel|trip|vacation|abroad|country|flight|plane|hotel": 
        "When traveling with celiac disease:\n\n"
        "1. Research gluten-free options at your destination before you go\n"
        "2. Pack emergency snacks and gluten-free essentials\n"
        "3. Consider booking accommodations with kitchen access to prepare safe meals\n"
        "4. Download translation cards explaining celiac disease in the local language\n"
        "5. Join online celiac groups for destination-specific advice\n"
        "6. Bring a doctor's note explaining your condition for customs/security\n\n"
        "The Celio app's travel guides provide country-specific information about celiac awareness and safe dining options in many destinations.",
    
    "symptom|reaction|sick|pain|bloat|diarrhea|headache|rash|fatigue": 
        "Common symptoms of celiac disease and gluten exposure include:\n\n"
        "1. Digestive issues: bloating, diarrhea, constipation, abdominal pain\n"
        "2. Fatigue and weakness\n"
        "3. Headaches or brain fog\n"
        "4. Joint or bone pain\n"
        "5. Skin rashes (dermatitis herpetiformis)\n"
        "6. Anemia or nutritional deficiencies\n\n"
        "If you've been exposed to gluten, focus on staying hydrated, resting, and following your doctor's recommendations. Symptoms typically resolve within a few days to weeks.",
    
    "food|ingredient|safe|avoid|eat|label|product|grocery": 
        "Foods to always avoid with celiac disease:\n\n"
        "1. Wheat (including durum, semolina, spelt, kamut, einkorn, farro)\n"
        "2. Rye and barley\n"
        "3. Most oats (unless certified gluten-free)\n"
        "4. Malt and malt flavoring\n"
        "5. Many processed foods with hidden gluten\n\n"
        "Safe foods include:\n"
        "- Fresh fruits and vegetables\n"
        "- Unprocessed meats, fish, and poultry\n"
        "- Most dairy products\n"
        "- Beans, legumes, and nuts\n"
        "- Gluten-free grains like rice, corn, quinoa, millet, and certified GF oats\n\n"
        "Always carefully read product labels and look for certified gluten-free products.",
    
    "family|gene|genetic|hereditary|parent|child|test|diagnose|diagnosis": 
        "Celiac disease has a genetic component:\n\n"
        "1. It runs in families - first-degree relatives have a 1 in 10 risk\n"
        "2. Celiac disease requires the presence of HLA-DQ2 or HLA-DQ8 genes\n"
        "3. Having these genes doesn't guarantee developing celiac (40% of the population has them)\n"
        "4. Environmental factors like infections, stress, or pregnancy can trigger onset\n\n"
        "Diagnosis typically involves:\n"
        "- Blood tests for specific antibodies\n"
        "- Small intestine biopsy\n"
        "- Genetic testing to rule out celiac disease\n\n"
        "If you have a family history, consider getting tested even without symptoms, as early detection prevents complications.",
    
    "cross.?contamination|kitchen|prepare|cook|utensil|toaster|cutting": 
        "Preventing cross-contamination at home:\n\n"
        "1. Maintain separate cooking utensils, cutting boards, and toasters\n"
        "2. Use different containers for condiments to prevent crumb transfer\n"
        "3. Clean surfaces thoroughly before preparing gluten-free foods\n"
        "4. Consider having designated gluten-free preparation areas\n"
        "5. Store gluten-free products on upper shelves to prevent crumbs falling from above\n"
        "6. Label gluten-free items clearly\n\n"
        "Even tiny amounts of gluten from cross-contamination can cause reactions in people with celiac disease.",
    
    "hello|hi|hey|greetings|start|intro|welcome":
        "Hello! I'm Sage, your personal gluten and celiac disease assistant. I can help with information about:\n\n"
        "- Safely dining out with celiac disease\n"
        "- Traveling with dietary restrictions\n"
        "- Understanding symptoms and managing accidental exposure\n"
        "- Safe and unsafe ingredients\n"
        "- Cross-contamination prevention\n\n"
        "What would you like to know about today? This is a demo version with pre-made responses, but I'm still learning to be more helpful!",
        
    "default":
        "Thank you for your question. In this demo version, I have a limited set of pre-made responses about celiac disease topics like:\n\n"
        "- Restaurant dining strategies\n"
        "- Travel tips for celiacs\n"
        "- Symptom management\n" 
        "- Safe and unsafe foods\n"
        "- Genetic/family information\n"
        "- Cross-contamination prevention\n\n"
        "Try asking about one of these topics, or check back when the premium version launches with full Claude AI integration for more personalized assistance!"
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
