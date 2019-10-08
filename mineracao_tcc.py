import csv
from unicodedata import normalize

import nltk


###################################Pré Processamento ###############################################################

# passo1 remoção de acentos, pontuação e definição de letras minusculas

def formatting_string(txt):
    text = txt.lower()
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


with open('basetreinamento.csv') as file:
    basetreinamento = list(csv.reader(file))
    # print(f'Antes --> {file_r}')
    for base in basetreinamento:
        for b in base:
            base[base.index(b)] = formatting_string(b)

            with open('baseteste.csv') as file:
                baseteste = list(csv.reader(file))
    # print(f'Antes --> {file_r}')
    for base in baseteste:
        for b in base:
            base[base.index(b)] = formatting_string(b)

# print(f'Depois --> {file_r}')

# passo 2 Definição das stopword de forma manual

stopwords = ['a', 'agora', 'algum', 'alguma', 'aquele', 'aqueles', 'de', 'deu', 'do', 'e', 'estou', 'esta', 'esta',
             'ir', 'meu', 'muito', 'mesmo', 'no', 'nossa', 'o', 'outro', 'para', 'que', 'sem', 'talvez', 'tem', 'tendo',
             'tenha', 'teve', 'tive', 'todo', 'um', 'uma', 'umas', 'uns', 'vou', 'pelo', 'com', 'de', 'a', 'o', 'que',
             'e', 'do', 'da', 'em', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as',
             'dos',
             'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também',
             'só',
             'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus', 'quem', 'nas',
             'me',
             'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas',
             'qual', 'nós', 'lhe',
             'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas',
             'teu',
             'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas',
             'aquele',
             'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve',
             'estivemos',
             'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam',
             'estivesse',
             'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve',
             'houvemos',
             'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem',
             'houver', 'houvermos',
             'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou',
             'somos', 'são', 'era',
             'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse',
             'fôssemos',
             'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam',
             'tenho', 'tem', 'temos',
             'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha',
             'tenhamos', 'tenham', 'tivesse',
             'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria',
             'teríamos', 'teriam', 'vou', 'tão']


# função não utilizada, pois as stopwords já serão removidas junto com a função de Stemmer
def removestopwords(file):
    # print('antes', file, '\n\n')

    nfile = []
    nword = []
    for idxl, line in enumerate(file):
        nfile.append([])
        for word in line:
            for caract in word.split():
                if caract in stopwords:
                    pass
                else:
                    nword.append(caract)

            nfile[idxl].append(' '.join(nword))
            nword = []
    return nfile


# print(removestopwords(file_r))

# passo 3 remover os radicais das palavras que não pertencem a lista de stopwords

stopwordsnltk = nltk.corpus.stopwords.words('portuguese')


def aplicastemmer(texto):
    stemmer = nltk.stem.RSLPStemmer()
    frasessstemming = []
    for (palavras, emocao) in texto:
        comstemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopwords]
        frasessstemming.append((comstemming, emocao))
    return frasessstemming


# removendo as stopword e mantendo somente o radical de cada palavra
# remocao = aplicastemmer(file_r)

frasescomstemmingtreinamento = aplicastemmer(basetreinamento)
frasescomstemmingteste = aplicastemmer(baseteste)
# print(remocao)
print(frasescomstemmingtreinamento)
print(frasescomstemmingteste)


# passo 4 Retornar todas as palavras que existem na base de dados
def buscapalavras(frases):
    todaspalavras = []
    for (palavras, emocao) in frases:
        todaspalavras.extend(palavras)
    return todaspalavras


palavrastreinamento = buscapalavras(frasescomstemmingtreinamento)
palavrasteste = buscapalavras(frasescomstemmingteste)
# print(palavras)
print(palavrastreinamento)
print(palavrasteste)


# passo 5 Frequencia que as palabras aparecem no texto
# definindo peso
def buscafrequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras


# frequencia = buscafrequencia(palavras)
frequenciatreinamento = buscafrequencia(palavrastreinamento)
frequenciateste = buscafrequencia(palavrasteste)

# common primeiras 50 palavras
# print(frequencia.most_common(50))
print(frequenciatreinamento.most_common(50))
print(frequenciateste.most_common(50))


# Passo 6 buscar palavras unicas
def buscapalavrasunicas(frequencia):
    freq = frequencia.keys()
    return freq


# palavrasunicas = buscapalavrasunicas(frequencia)
# print(palavrasunicas)

palavrasunicastreinamento = buscapalavrasunicas(frequenciatreinamento)
print(palavrasunicastreinamento)

palavrasunicasteste = buscapalavrasunicas(frequenciateste)
print(palavrasunicasteste)


# passo 7 função que recebe uma frase, e retorna as palavras que ela tem e quais não tem

def extratorpalavras(documento):
    # set: associar
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavrasunicastreinamento:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


# passar frases sem stopword e sem radical
caracteristicasfrase = extratorpalavras(['am', 'nov', 'dia'])
print(caracteristicasfrase)

# passo 8 passando a base completa para extração de cada uma das frases
# esta base pré processada, que será avaliada pelo algoritmo
basecompletatreinamento = nltk.classify.apply_features(extratorpalavras, frasescomstemmingtreinamento)
# print(basecompleta[15]) se eu quiser passo 15 para pegar a decima quinta  frases
print(basecompletatreinamento[15])
basecompletateste = nltk.classify.apply_features(extratorpalavras, frasescomstemmingteste)
# print(basecompleta[15]) se eu quiser passo 15 para pegar a decima quinta  frases
print(basecompletateste[15])

###################################Aplicação do algoritmo###############################################################


# construindo a tabela de probabilidade
# train = treinamento
classificador = nltk.NaiveBayesClassifier.train(basecompletatreinamento)
# mostra quais são as classes
print(classificador.labels())
# print(classificador.show_most_informative_features(20))

print(nltk.classify.accuracy(classificador, basecompletateste))

erros = []
for (frase, classe) in basecompletateste:
    print(frase)
    print(classe)
    resultado = classificador.classify(frase)
    if resultado != classe:
        erros.append((classe, resultado, frase))
for (classe, resultado, frase) in erros:
    print(classe, resultado, frase)

#matriz de erro
from nltk.metrics import ConfusionMatrix
esperado = []
previsto = []
for (frase, classe) in basecompletateste:
    resultado = classificador.classify(frase)
    previsto.append(resultado)
    esperado.append(classe)

#esperado = 'alegria alegria alegria alegria medo medo surpresa surpresa'.split()
#previsto = 'alegria alegria medo surpresa medo medo medo surpresa'.split()
matriz = ConfusionMatrix(esperado, previsto)
print(matriz)

#-------------------------------------------------------------------teste ------------------------------------------------------------------------------

with open('basenova.csv') as file:
    basenova = list(csv.reader(file))
# print(f'Antes --> {file_r}')
for base in basenova:
    for b in base:
        base[base.index(b)] = formatting_string(b)



testestemming = []
stemmer = nltk.stem.RSLPStemmer()
for (palavras) in basenova:
    comstem = [p for p in palavras]
    # radicais mais informativos
    testestemming.append(str(stemmer.stem(comstem[0])))
print(testestemming)

novo = extratorpalavras(testestemming)
print(novo)

print(classificador.classify(novo))

# distribuição da probabilidade em ser satisfatório e insatisfatório
distribuicao = classificador.prob_classify(novo)
for classe in distribuicao.samples():
    print("%s: %f" % (classe, distribuicao.prob(classe)))

