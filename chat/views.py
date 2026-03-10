"""Chat UI and send-message API. Anonymous users use session; logged-in users use DB."""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from .models import ChatThread, ChatMessage

SESSION_CHAT_KEY = 'chat_messages'
SESSION_CHAT_MAX = 20


def _get_system_prompt(request):
    """Build system prompt from user's profile (custom_instructions, base_style, bio)."""
    parts = [
        "You are a helpful assistant for ExploringU, a career exploration tool for college students. "
        "Help with brainstorming, academic questions, and general questions. Be clear and supportive.",
        "Format your responses for easy reading: start a new line for each distinct topic or point. "
        "Bold every heading or topic by wrapping it in double asterisks, e.g. **Topic name**. "
        "Use this pattern: **Heading** then the content on the next line(s). Keep structure clear.",
    ]
    try:
        profile = request.user.profile
    except Exception:
        profile = None
    if profile:
        if profile.base_style:
            style_map = {
                'friendly': 'Use a friendly, approachable tone.',
                'professional': 'Use a professional, polished tone.',
                'concise': 'Be concise and to the point.',
                'detailed': 'Give detailed, thorough answers.',
            }
            parts.append(style_map.get(profile.base_style, ''))
        if profile.custom_instructions:
            parts.append("User's custom instructions: " + profile.custom_instructions.strip())
        if profile.bio:
            parts.append("About the user: " + profile.bio.strip())
    return "\n".join(p for p in parts if p)


def chat_home_view(request):
    """Chat page: message list and input. Works for anonymous and logged-in users."""
    return render(request, 'chat/chat.html')


@csrf_exempt
@require_POST
def chat_send_view(request):
    """API: POST { content: "user message" } -> { content: "assistant reply" } or { error: "..." }."""
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    content = (body.get('content') or '').strip()
    if not content:
        return JsonResponse({'error': 'Message is required.'}, status=400)

    try:
        system = _get_system_prompt(request)
        from resume.views import _call_gemini

        if request.user.is_authenticated:
            thread, _ = ChatThread.objects.get_or_create(user=request.user)
            ChatMessage.objects.create(thread=thread, role=ChatMessage.ROLE_USER, content=content)
            all_messages = list(thread.messages.order_by('created_at'))
            messages = all_messages[-SESSION_CHAT_MAX:]
            history_lines = []
            for m in messages:
                prefix = "User: " if m.role == ChatMessage.ROLE_USER else "Assistant: "
                history_lines.append(prefix + m.content)
            prompt = system + "\n\n" + "\n\n".join(history_lines) + "\n\nAssistant: "
            text, err = _call_gemini(prompt)
            if err:
                return JsonResponse({'error': err}, status=500)
            if not text:
                return JsonResponse({'error': 'No response from assistant.'}, status=500)
            ChatMessage.objects.create(thread=thread, role=ChatMessage.ROLE_ASSISTANT, content=text)
            return JsonResponse({'content': text})

        # Anonymous: use session for history
        messages = request.session.get(SESSION_CHAT_KEY, [])
        messages.append({'role': ChatMessage.ROLE_USER, 'content': content})
        history_lines = []
        for m in messages[-SESSION_CHAT_MAX:]:
            prefix = "User: " if m['role'] == ChatMessage.ROLE_USER else "Assistant: "
            history_lines.append(prefix + m['content'])
        prompt = system + "\n\n" + "\n\n".join(history_lines) + "\n\nAssistant: "
        text, err = _call_gemini(prompt)
        if err:
            return JsonResponse({'error': err}, status=500)
        if not text:
            return JsonResponse({'error': 'No response from assistant.'}, status=500)
        messages.append({'role': ChatMessage.ROLE_ASSISTANT, 'content': text})
        request.session[SESSION_CHAT_KEY] = messages[-SESSION_CHAT_MAX:]
        request.session.modified = True
        return JsonResponse({'content': text})
    except Exception as e:
        return JsonResponse(
            {'error': str(e) if str(e) else 'An unexpected error occurred.'},
            status=500,
        )


def _saved_summary(saved_list, max_words=5):
    """First user message, truncated to max_words. Default label if empty."""
    for m in saved_list:
        if m.get('role') == 'user' and (m.get('content') or '').strip():
            words = (m.get('content') or '').strip().split()[:max_words]
            return ' '.join(words) if words else 'Previous chat'
    return 'Previous chat'


@require_GET
def chat_messages_view(request):
    """API: GET -> { messages: [], savedMessages: [...], savedSummary: "..." }. On load, previous conversation becomes saved (sidebar); main stays empty."""
    if request.user.is_authenticated:
        thread = ChatThread.objects.filter(user=request.user).first()
        if not thread:
            return JsonResponse({'messages': [], 'savedMessages': [], 'savedSummary': ''})
        saved_list = [
            {'role': m.role, 'content': m.content}
            for m in thread.messages.order_by('created_at')
        ]
        thread.messages.all().delete()
        summary = _saved_summary(saved_list)
        return JsonResponse({'messages': [], 'savedMessages': saved_list, 'savedSummary': summary})
    # Anonymous: move current to saved for sidebar, clear current
    saved_list = list(request.session.get(SESSION_CHAT_KEY, []))
    request.session[SESSION_CHAT_KEY] = []
    request.session.modified = True
    summary = _saved_summary(saved_list)
    return JsonResponse({'messages': [], 'savedMessages': saved_list, 'savedSummary': summary})
