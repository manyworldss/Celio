from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.http import HttpResponse

@login_required
def sage_assistant(request):
    # get users conversations or create a default one
    conversation, created = Conversation.objects.get_or_create(user=request.user)

    if not conversation.exists():
        conversation = Conversation.objects.create(
            user=request.user,
            title="Welcome to Sage!"
        )

        # create a welcome message
        Message.objects.create(
            conversation=conversation,
            role=Message.ROLE_ASSISTANT,
            content="Hello! I'm Sage, your personal allergy assistant. How can I help you today?"
        )
    
    else:
        conversation = Conversation.first()

        # Get all messages for the current conversation
        messages = conversation.messages.all()

        # handle new message submission
        if request.method == 'POST' and 'message' in request.POST:
            user_message = request.POST.get('message').strip()

            if user_message:
                # save user message
                Message.objects.create(
                    conversation=conversation,
                    role=Message.ROLE_USER,
                    content=user_message
                )
                
                # generate placeholder response (this will be replaced with actual AI response)
                placeholder_response = {
                    "restaurant": "When dining at restaurants, always inform your server about your celiac disease. Ask about dedicated preparation areas and cross-contamination protocols. Many restaurants now offer gluten-free menus - just make sure they understand the importance of avoiding cross-contamination.",
                    "travel": "When traveling, research gluten-free options at your destination before you go. Consider booking accommodations with kitchen access. Pack emergency snacks, translation cards in the local language, and use apps like Find Me Gluten Free to locate safe restaurants.",
                    "symptoms": "Common symptoms of celiac disease include digestive issues (bloating, diarrhea, constipation), fatigue, headaches, joint pain, and skin rashes. If you accidentally consume gluten, stay hydrated, rest, and follow your doctor's recommendations for recovery.",
                    "foods": "Always avoid wheat, barley, rye, and regular oats (unless certified gluten-free). Safe foods include fresh fruits, vegetables, meat, fish, rice, potatoes, and certified gluten-free products. Always check labels, as gluten can hide in unexpected places like sauces and seasonings."
                }
                
                # simple keyword matching for demo purposes
                response_text = "I'm still learning about celiac disease. This feature will be expanded in the premium version of Celio to provide more personalized response using Claude AI."

                # save assistant response
                Message.objects.create(
                    conversation=conversation,
                    role=Message.ROLE_ASSISTANT,
                    content=response_text
                )
                
                # update conversation timestamp
                conversation.save()

                # if HTMX request, return just the messages
                if request.headers.get('HX-Request'):
                    return render(request, 'sage/partials/message.html', {
                        'messages': conversation.messages.all().order_by('created_at')
                    })
        return render(request, 'sage/sage_assistant.html', {
            'conversation': conversation,
            'current_conversation': conversation,
            'messages': messages,
            })
    
    @login_required
    def new_conversation(request):
        # create new conversation
        Conversation.objects.create(
            user=request.user,
            title="New Conversation"
        )

        # add welcome message
        Message.objects.create(
            conversation=Conversation,
            role=Message.ROLE_ASSISTANT,
            content="Hello! I'm Sage, your personal allergy assistant. How can I help you today?"
        )
        return redirect('sage:sage_assistant')

@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)

    if request.method == 'POST':
        conversation.delete()

    return redirect('sage:sage_assistant')

        
            


# Create your views here.
