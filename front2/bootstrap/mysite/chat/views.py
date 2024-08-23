from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MessageForm
from .models import Message
from django.shortcuts import render, get_object_or_404
from .models import User, Message

def conversation_view(request, username):
    user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(user=user).order_by('timestamp')
    context = {'user': user, 'messages': messages}
    return render(request, 'conversation.html', context)


def index(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user  # Atribui o usuário logado à mensagem
            message.save()
            return redirect('index')  # Redireciona para a página inicial após o envio
    else:
        form = MessageForm()

    messages = Message.objects.all()  # Obtém todas as mensagens

    return render(request, 'chat/index.html', {'form': form, 'messages': messages})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user  # Atribui o usuário logado à mensagem
            message.save()
            return JsonResponse({'message': message.text})
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)

