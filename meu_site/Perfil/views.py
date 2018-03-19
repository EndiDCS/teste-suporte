from django.shortcuts import render,redirect, get_object_or_404
from .forms import InfoForm,VotoForm
from django.contrib.auth.models import User
from .models import Info,Voto,Profile

# Create your views here.
def adiciona(request):
    #adiciona informação
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return redirect('home')
    else:
        form = InfoForm()
    return render(request, 'adiciona.html', {'form': form})

def mural(request):
    #renderiza o mural sem as informações votadas pelo usuário    
    users = User.objects.exclude(id=request.user.id)
    informations = Info.objects.exclude(user=request.user)
    votes = Voto.objects.filter(user=request.user)
    
    for v in votes:
        informations = informations.exclude(id=v.info.id)
    
    return render(request,'mural.html',{'users':users, 'informations':informations,'votes':votes})


def votos(request,user_id,info_id):
    user = get_object_or_404(User, pk=user_id)
    info = get_object_or_404(Info, pk=info_id)
   
   #Recebe voto 
    if request.method == 'POST':
        if 'True' in request.POST:
            voto = True
        else:
            voto = False
        # Cria e Salva voto    
        v = Voto.create(request.user,info,voto)
        v.save()
        
        #calcula pontuação
        usuarios = User.objects.all()
        votos = Voto.objects.all()
        
        if v.is_true == info.is_true:
            info.acertos = info.acertos + 1
            info.save()
            
            for u in usuarios:
                for v in votos:
                    if (u == v.user and info == v.info):
                        if(info.acertos >= 3):
                            if(info.acertos == 3):
                                u.profile.points = u.profile.points + (1.0/3)
                                u.profile.save()
                            else: 
                                diferenca = info.acertos - 3
                                pontos_a_distribuir = 2**diferenca
                                reducao = 2**(diferenca-1)
                                #verifica se o usuário ja tinha votado antes na informação caso sim apenas adificona diferenca, caso contrario adiciona o valor completo da pontuacao
                                if(u != request.user ):
                                    u.profile.points = u.profile.points + (pontos_a_distribuir / info.acertos) - (reducao/(info.acertos-1))
                                else:
                                    u.profile.points = u.profile.points + (pontos_a_distribuir / info.acertos)
                                u.profile.save()
        else:
            info.erros = info.erros + 1
            info.save()
            for u in usuarios:
                for v in votos:
                    if (u == v.user and info == v.info):
                        if(info.erros >= 3):
                            if(info.erros == 3):
                                u.profile.points = u.profile.points - (1.0/3)
                                u.profile.save()
                            else:    
                                diferenca = info.erros - 3
                                pontos_a_distribuir = 2**diferenca
                                reducao = 2**(diferenca-1)
                                if(u != request.user ):
                                    u.profile.points = u.profile.points - (pontos_a_distribuir / info.erros) + (reducao/(info.erros-1))
                                else:
                                    u.profile.points = u.profile.points - (pontos_a_distribuir / info.erros)
                                u.profile.save()
            
        #verifica se usuário ja votou e esconde informação    
        users = User.objects.exclude(id=request.user.id)
        informations = Info.objects.exclude(user=request.user)
        votes = Voto.objects.filter(user=request.user)
        for v in votes:
            informations = informations.exclude(id=v.info.id)
        #renderiza o mural sem as informações votadas pelo usuário    
        return render(request, 'mural.html',{'users':users, 'informations':informations,'votes':votes} )
    
    # mostar as informações que o usuário ja votou
    return render(request, 'votos.html', )
    
def perfil(request):
    usuarios = User.objects.all()
    perfil = Profile.objects.all()
    votes = Voto.objects.all
    return render(request, 'perfil.html',{'users':usuarios, 'perfil':perfil,'votes':votes} )
    
