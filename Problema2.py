
import string, random, copy
from time import sleep
score = 0

#Cria tabela com elementos aleatorios
def criar_tabuleiro(linha,coluna):
    #Coleta as letras do alfabeto da letra 'A' até a letra de acordo com o número de coluna
    alfabeto = string.ascii_uppercase[0:coluna] 
    #pega o valor de alfabeto e fatia em uma lista
    letras = [l for l in alfabeto]*5
    matriz = []
    for i in range(0,linha):
        # embaralha a lista
        random.shuffle(letras) 
        # faz um cópia da lista embaralhada
        lista = letras[0:coluna] 
        # adciona a lista embaralhada
        matriz.append(lista) 
    return matriz

#faz uma troca de posição com a string adjacente do lado esquerdo
def mover_esquerda(x,y,matriz):
    posicao = matriz[x][y]
    matriz[x][y] = matriz[x][y-1]
    matriz[x][y-1] = posicao
    return matriz

#faz uma troca de posição com a gema adjacente do lado direito
def mover_direita(x,y,matriz):
    posicao = matriz[x][y]
    matriz[x][y] = matriz[x][y+1]
    matriz[x][y+1] = posicao
    return matriz

#faz uma troca de posição com a gema adjacente superior
def mover_cima(x,y,matriz):
    posicao = matriz[x][y]
    matriz[x][y] = matriz[x-1][y]
    matriz[x-1][y] = posicao
    return matriz

#faz uma troca de posição coma a gema adjacente inferior
def mover_baixo(x,y,matriz):
    posicao = matriz[x][y]
    matriz[x][y] = matriz[x+1][y]
    matriz[x+1][y] = posicao
    return matriz

#imprime a matriz formatada
def vizualizar_tabuleiro(matriz, time = 1):
    print('¨'*31)
    print(f'|Score: [{score}]|')
    for x in range(0,len(matriz)):
        if x == 0:
            for i in range(0,len(matriz[0])+1):
                if i == 0:
                    print('   ',end='')
                else:
                    if i != (len(matriz[0])+1) - 1:
                        print(i-1,end='  ')
                    else:
                        print(i-1)
            for i in range(0,len(matriz[0])):
                if i == 0:
                    print('   ',end='')
                else:
                    if i != len((matriz[0]))-1:
                        print('___',end='')
                    else:
                        print('____')

        for y in range(0,len(matriz[0])):

            if y != len((matriz[0]))-1:
                if y == 0:
                    print(f'{x} |',end='')
                print(f'{matriz[x][y]}',end='  ')

            else:
                print(matriz[x][y])
    print('¨'*31)
    print()
    sleep(time)
    return

#Elimina sequencia de string iguais, horizontal e vertical.
def deleta_sequencia(matriz):
    #Faz uma copia da matriz
    copia_matriz = copy.deepcopy(matriz)
    verifica = copy.deepcopy(matriz)
    for x in range(len(matriz)):
        for y in range(len(matriz[0])-1):
            if matriz[x][y] != " ":
                gema = matriz[x][y]
                quantidade = verifica[x].count(gema)
                
                if quantidade >= 3:
                    #remove a string e insere o " " em sua posição
                    for i in range(0,quantidade):
                        matriz[x][y] = " "
                        verifica[x][y] = " "
                        y +=1
                        #verifica se a próxima string é diferente
                        try:
                            if matriz[x][y] != gema:
                                break
                        except IndexError:
                            break

                #Caso tenha alterado apenas dois elementos, retorna ao valor anterior
                if verifica[x].count(" ") < 3:
                    for i in range(2):
                        if " " in verifica[x]:
                            p = verifica[x].index(" ")
                            verifica[x].remove(" ")
                            verifica[x].insert(p, gema)
                            matriz[x][p] = gema
                verifica = copy.deepcopy(copia_matriz)

    #Faz uma matriz só com colunas
    colum = []
    for y in range(len(copia_matriz[0])):
        colum_temp = []
        for x in range(len(copia_matriz)):
            colum_temp.append(copia_matriz[x][y])
        colum.append(colum_temp)
    copia_colum = copy.deepcopy(colum)

    #Mesmo processo feito com as sequncias horizontal, só que agora com as sequencias verticais
    for x in range(len(colum)):
        for y in range(len(colum[0])-1):
            if matriz[y][x] != " ":
                gema = colum[x][y]
                quantidade = colum[x].count(gema)
                if quantidade >= 3:
                    
                    for i in range(0,quantidade):
                        #Usa a matriz colum como referência, e muda 
                        if matriz[y][x] != " ":
                            colum[x][y] = " "
                            matriz[y][x] = " "
                            y += 1
                        
                        try:
                            if colum[x][y] != gema:
                                break
                        except IndexError:
                            break

                    if colum[x].count(" ") < 3:
                        for i in range(2):
                                if " " in colum[x]:
                                    posicao = colum[x].index(" ")
                                    colum[x].remove(" ")
                                    colum[x].insert(posicao, gema)
                                    matriz[posicao][x] = gema
                    colum = copy.deepcopy(copia_colum)
    return matriz

#retorna uma jogada para o usuario, caso seja possivel.
def dica_jogada(matriz):
    copia = copy.deepcopy(matriz)

    for linha in range(0,len(matriz)):
        for coluna in range(0,len(matriz[0])):
            #condição verifica se é a ultima coluna
            if coluna ==  (len(matriz[0])-1) and linha != (len(matriz)-1):
                #faz a permutação com a string inferior
                mover_baixo(linha, coluna, copia)
                deleta_sequencia(copia)
                
                #verifica se tem o " " na matriz.
                for l in copia:
                    if " " in l:
                        #Retorna a string para a posição inicial
                        mover_baixo(linha, coluna, copia)
                        #Caso encontre vai retornar a posição da string que fez a permutação e o sentido.
                        return (
                            f'Mova a gema da posição {linha,coluna} para [S]| Baixo'
                        )

                    mover_baixo(linha, coluna, copia)

            #Entra na condição caso seja a última linha
            elif linha == (len(matriz)-1):
                if coluna != (len(matriz[0])-1):
                    #Faz a permutação com a string adjacente do lado esquerdo
                    mover_direita(linha, coluna, copia)
                    #retorna a matriz com " ", caso tenha feito ponto.
                    deleta_sequencia(copia)
                    for l in copia:
                        if " " in l:
                            mover_direita(linha, coluna, copia)
                            return (
                                f'Mova a gema da posição {linha,coluna} para [D]|Direita!'
                                )

                    mover_direita(linha, coluna, copia)

            #Entra na condição se a posição não pertencer a última coluna, e nem a última linha.
            else:
                mover_direita(linha, coluna, copia)
                deleta_sequencia(copia)
                for l in copia:
                    if " " in l:
                        mover_direita(linha, coluna, copia)
                        return (
                            f'Mova a gema da posição {linha,coluna} para [D]|Direita!'
                            )
                #Reseta a aposição da gema
                mover_direita(linha, coluna, copia)
                mover_baixo(linha, coluna, copia)

                deleta_sequencia(copia)
                for l in copia:
                    if " " in l:
                        mover_baixo(linha, coluna, copia)
                        return (
                            f'Mova a gema da posição {linha,coluna} para [S]|Baixo!'
                            )
                mover_baixo(linha, coluna, copia)

#Gera uma letra aletoria
def gera_letra_aleatoria(linha,coluna):
    alfabeto = string.ascii_uppercase[0:coluna]
    letras = [l for l in alfabeto]*5
    #Embaralha a lista
    random.shuffle(letras)
    #Pega a primeiro elemento de letras
    uma_letra = letras[0]
    return uma_letra

#desloca_gema as gemas para baixo, preenchendo o espaço vazio
def desloca_gema(matriz):
    for linha in range(0, len(matriz)):
        for coluna in range(0,len(matriz[0])):
            cont = 1
            linha2 = linha
            while True:
                if linha == 0:
                    linha += 1
                #Entra na condição se o elento verficado for igual a " "
                if matriz[linha][coluna] == " ":
                    #Entra  na condição se o elemento superior for diferente de " " e não for a primeira linha
                    if matriz[linha2-cont][coluna] != " " and linha != 0:
                        #Caso cumpra os requisitos faz a permutação
                        mover_cima(linha, coluna, matriz)
                        linha -= 1
                        cont += 1
                        if linha == 1:
                            mover_cima(linha, coluna, matriz)
                            linha = cont

                    else:
                        if linha2 == (len(matriz)-1):
                            linha = linha2
                        break
                else:
                    break
    #Gera strings aleatorias quando os espaços "em brancos" estiverem no limite superior.
    for linha in range(0, len(matriz)):
        for coluna in range(0,len(matriz[0])):
            if matriz[linha][coluna] == " ":
                #Gera string aleatoria em espaços vazios
                matriz[linha][coluna] = gera_letra_aleatoria(len(matriz), len(matriz[0]))
    return matriz

#Verifica se existe elementos eliminados na matriz
def conta_pontos(matriz):
    cont = 0
    for linha in matriz:
        for gema in linha:
            if gema == " ":
                #Caso encontre espaço vazio retorna cont incrementa 1
                cont += 1
    if cont == 0:
        return False
    else:
        return cont


    


if __name__ == '__main__':

    print('^'*72)
    print(f"{'BEM VINDO AO JOGO GEMAS':^72}")
    print('^'*72)

    print('='*72)
    print(f"{'|REGRAS DO GAME|':^72}\n")
    print('[1°] O tabuleiro deve ser no mínimo 3x3 e no máximo 10x10\n'
            '[2°] O jogador só pode fazer permutação com gemas adjacentes\n'
            '[3°] As coordenadas indicadas devem está dentro do tabuleiro\n'
            '[4°] O minimo de cadeia de gemas que podem gerar pontos, são três gemas!')
    print('='*72)

    while True:
        print('='*31)
        print('Crie o tabuleiro!')
        sleep(0.5)
        linha = input('Informe a quantidade de linha: \n''->')
        #Verifica se o valor informado é um número
        if not linha.isnumeric():
            print('Só aceitamos números, digite novamente ;)\n')
            continue

        else:
            linha = int(linha)
            #Verifica se linha está entre 3 e 10
            if linha > 10 or linha < 3:
                print('Tamanho de linha invalido!')
                continue
            else:
                break

    while True:
        coluna = input('Informe a quantidade de coluna: \n''->')
        if not coluna.isnumeric():
            print('Só aceitamos números, digite novamente ;)\n')
            continue

        else:
            coluna = int(coluna)
            if linha > 10 or linha < 3:
                print('Tamanho de coluna invalido!')
                continue
            else:
                print('='*31)
                break

    
    #Gera um tabuleiro com possibilidade de jogada e sem sequências de gemas
    print('Criando Tabuleiro, Aguarde...\n')
    while True:
        tabuleiro = criar_tabuleiro(linha, coluna)
        #Deleta sequencia caso exista
        deleta_sequencia(tabuleiro)
        c = conta_pontos(tabuleiro)
        if c == False:
            #Verifica se existe possiblidade de jogada
            if dica_jogada(tabuleiro) == None:
                continue

            else: 
                break
        else:
            continue

    vizualizar_tabuleiro(tabuleiro)        

    cont = 0
    while True:
        while True:
            print('='*31)
            print(f"{f'|Score: [{score}]|':>30}")
            play = input('[H] Pedir dica\n[Q] Encerrar jogo\n[V] Mostrar tabuleiro\n[ENTER] Jogar\n->').upper()

            if play  == 'H':
                if score > 0:
                    score -= 1
                    print()
                    print(f'|Score: [{score}]|')
                    print(dica_jogada(tabuleiro))
                    vizualizar_tabuleiro(tabuleiro)

                else:
                    print('Pontos insuficientes!')
                    vizualizar_tabuleiro(tabuleiro)
                    print('='*31)
                    break

            elif play == 'V':
                vizualizar_tabuleiro(tabuleiro)

            elif play == '':
                print('='*31)

                while True:
                    linha_tabuleiro = input('Indique o número da Linha: ')

                    if not linha_tabuleiro.isnumeric():
                        print('Só aceitamos números, digite novamente ;)\n')
                        vizualizar_tabuleiro(tabuleiro)
                        continue

                    else:
                        linha_tabuleiro = int(linha_tabuleiro)

                        if linha_tabuleiro > len(tabuleiro)-1 or linha_tabuleiro < 0:
                            print('Posição Inváliva\n')
                            vizualizar_tabuleiro(tabuleiro)
                            continue

                        else:
                            break
                while True:
                    coluna_tabuleiro = input('Indique o número da Coluna: ')
                    if not coluna_tabuleiro.isnumeric():
                        print('Só aceitamos números, digite novamente ;)\n')
                        vizualizar_tabuleiro(tabuleiro)
                        continue

                    else:
                        coluna_tabuleiro = int(coluna_tabuleiro)
                        if coluna_tabuleiro > len(tabuleiro[0])-1 or coluna_tabuleiro < 0:
                            print('Posição Inváliva\n')
                            vizualizar_tabuleiro(tabuleiro)
                            continue

                        else:
                            break
                print()
                while True: 
                    try:
                        while True:
                            direcao = input('Informe a direção:\n'
                                        '[W] Cima\n'
                                        '[S] Baixo \n'
                                        '[A] Esquerda \n'
                                        '[D] Direita\n'
                                        '->').upper()

                            if direcao not in 'WASD' or len(direcao) > 1:
                                print('direcao Inválida!')
                                vizualizar_tabuleiro(tabuleiro)
                                continue
                            else:
                                break
                        #Faz uma cópia da matriz antes da jogada
                        copia_tabuleiro = copy.deepcopy(tabuleiro)
                        #Entra na condição de acordo com a direcao
                        if direcao == 'W':
                            tabuleiro = mover_cima(linha_tabuleiro, coluna_tabuleiro, tabuleiro)
                        elif direcao == 'D':
                            tabuleiro = mover_direita(linha_tabuleiro, coluna_tabuleiro, tabuleiro)
                        elif direcao == 'A':
                            tabuleiro = mover_esquerda(linha_tabuleiro, coluna_tabuleiro, tabuleiro)
                        elif direcao == 'S':
                            tabuleiro = mover_baixo(linha_tabuleiro, coluna_tabuleiro, tabuleiro)

                        vizualizar_tabuleiro(tabuleiro)
                        deleta_sequencia(tabuleiro)
                        if conta_pontos(tabuleiro) == False:
                            tabuleiro = copia_tabuleiro
                            vizualizar_tabuleiro(tabuleiro)
                            break
                        else:
                            vizualizar_tabuleiro(tabuleiro)
                            break
                    except IndexError:
                        print('Jogada Inváliada!\n')
                        vizualizar_tabuleiro(tabuleiro)
                        continue
                while True:
                    #Verifica se existe eliminiações no tabuleiro
                    if conta_pontos(tabuleiro) == False:
                        break

                    elif conta_pontos(tabuleiro):
                        #soma a quantidade de pontos no tabuleiro e guarda no score
                        score += conta_pontos(tabuleiro) 
                        #Desloca o tabuleiro
                        desloca_gema(tabuleiro)
                        #Mostra o tabuleiro
                        vizualizar_tabuleiro(tabuleiro)
                        #Elimina sequencia caso exista
                        deleta_sequencia(tabuleiro)
                        #Se existe sequencia entra na condição
                        if conta_pontos(tabuleiro):
                            score += conta_pontos(tabuleiro)
                            #Mostra a matriz
                            vizualizar_tabuleiro(tabuleiro)
                            #Desloca
                            desloca_gema(tabuleiro)
                            vizualizar_tabuleiro(tabuleiro)
                            #Elimina caso exista
                            deleta_sequencia(tabuleiro)
                            #Mostra novamente
                            if conta_pontos(tabuleiro):
                                vizualizar_tabuleiro(tabuleiro)
                            #Continua o laço
                            continue
            #caso não exista jogada posiveis
            if dica_jogada(tabuleiro) == None:
                break

            #Se o valor informado não for o esperado    
            if play not in 'QHV':
                print('Entrada inválida!')
                print('='*31)
                vizualizar_tabuleiro(tabuleiro)
                break

            elif play == 'Q':
                break
        #Para parar o laço principal se não tiver jogadas possiveis ou o jogador pedir pra parar        
        if play == 'Q' or dica_jogada(tabuleiro) == None:
            print('='*31)
            print('Fim de Jogo!')
            print(f'[Score: |{score}|]')
            print('='*31)
            break
