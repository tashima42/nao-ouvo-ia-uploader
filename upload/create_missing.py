import os
import json
import re
import sys
import unicodedata

missing_episodes = [
    "AVISO CCXP 2017 Fini",
    "Abecedário do Não Ouvo",
    "Cyber Teoria Não Ouvo #018 - Cyber Food",
    "Cyber Teoria Não Ouvo #020 - Transportes",
    "Cyber Teoria Não Ouvo #25 - O problema da terceira idade oriental",
    "FÉRIAS!",
    "Hoje é o dia da MALDADE na Internet",
    "Não Ouvo #152 -  Serviço de Atendimento ao Não Ouvinte (ft. Não Ouvintes)",
    "Não Ouvo #154 - Humor 100 Limites (ft. Magalzão e Lucas Inutilismo)",
    "Não Ouvo #156 - POR FAVOR ME ENTRETENHA (ft. Matheus Canella e Lucas Inutilismo)",
    "Não Ouvo #158 - Filmes TOP (ft. Magalzão Show, Matheus Canella e Lucas Inutilismo)",
    "Não Ouvo #160 - Cuck Social (ft. Lierson e Lucas Inutilismo)",
    "Não Ouvo #162 - Papai e Mamãe (ft. Affonso Solano e Didi Braguinha)",
    "Não Ouvo #164 - Minha Vida Gamer (ft. Magalzão, Totoro e Eternal)",
    "Não Ouvo #166 - Será se é live action? (ft. Daniel Bayer, Magalzão e Ivo Neuman)",
    "Não Ouvo #168 - O SAL É O LIMITE!! (ft. Lierson)",
    "Não Ouvo #170 - AQUELA História de Ano Novo",
    "Não Ouvo #172 - O Nome Dela é Jennifer (ft. Ivo Neuman)",
    "Não Ouvo #175 - Show do Gringão",
    "Não Ouvo #178 - Ressacona do Carnaval",
    "Não Ouvo #180 - O BONDE: OS AVENGERS BRASILEIROS",
    "Não Ouvo #187 - Meu vício, minhas regras!",
    "Não Ouvo #188 - Podcast Sério (ft. Guga Mafra)",
    "Não Ouvo #189 - O Que Só Ele Escuta (ft. Daniel Bayer)",
    "Não Ouvo #190 - Que Delícia de Infância! #FiniCast",
    "Não Ouvo #191 - Anime é lindo!!!",
    "Não Ouvo #192 - Super humanos (ft. Didi Braguinha e Daniel Bayer)",
    "Não Ouvo #193 - Que rodeio!",
    "Não Ouvo #194 - Acabou-se tudo",
    "Não Ouvo #195 - Meu querido discador",
    "Não Ouvo #196 - Mais alergia, meu povo!!!",
    "Não Ouvo #197 - Academia dos Infernos",
    "Não Ouvo #198 - Invasão na Área 51",
    "Não Ouvo #199 - O Que Eu Não Deveria Ter Visto no Japão",
    "Não Ouvo #200 - Caminhão a Milhão",
    "Não Ouvo #201 - Estão me Boicotando!",
    "Não Ouvo #202 - Zap da Morte",
    "Não Ouvo #203 - O Futuro já Chegou!!!",
    "Não Ouvo #204 - Histórias Obscuras do Meu Pai",
    "Não Ouvo #205 - Halloween da Malha Fina",
    "Não Ouvo #206 - VOCÊ SÓ TEM UMA CHANCE!!!",
    "Não Ouvo #207 - Bagunça com Hambúrguer",
    "Não Ouvo #208 - Minha TV dos Anos 90 (ft. Guga Mafra)",
    "Não Ouvo #209 - Big Youtubers Brasil",
    "Não Ouvo #210 - Sou Burro Fora do Brasil",
    "Não Ouvo #211 - Fim de Ano Com Meu Pai",
    "Não Ouvo #212 - A Famosa História de Réveillon",
    "Não Ouvo #213 - Sonho de Uma Noite de Verão",
    "Não Ouvo #214 - Coronavírus",
    "Não Ouvo Extra - Festival da Frase Solta",
    "Não Ouvo RPJ: O D1G1T4L 1NFLU3NC3R #1",
    "Não Ouvo RPJ: O D1G1T4L 1NFLU3NC3R #2",
    "O FIM DO NãO OUVO ATÉ O PRÓXIMO",
    "Plantão Não Ouvo #001 - Câncer, Cinzas e Maconha",
    "Plantão Não Ouvo #002 - Motorista do Trump, Tubarão e Barata na Cabeça",
    "Plantão Não Ouvo #003 - Bêbados, Crianças e Maconheiros",
    "Plantão Não Ouvo #004 - Miojo, Catuaba e Pônei sem cinto",
    "Plantão Não Ouvo #005 - Jacaré, Chocolate e Apanhando da Esposa",
    "Plantão Não Ouvo #006 - Escola, Presépio, Gato assassino e Granada sem pino",
    "Plantão Não Ouvo #007 - Churrasco, Tequila e Youtuber Burro",
    "Plantão Não Ouvo #008 - Terreno na Lua, Cachorro no Busão e Resgate em Bitcoin",
    "Plantão Não Ouvo #009 - Briga infinita, uniformes gigantes e bêbado fujão",
    "Plantão Não Ouvo #010 - Resgate de linguiça, cocaína salgada e tudo no improviso",
    "Plantão Não Ouvo #011 - Motorista sem braço, Curriculum de bandido e Churrasco no cemitério",
    "Plantão Não Ouvo #012 - Sequestro por café, Ronaldinhocoin e Lamborgurno",
    "Plantão Não Ouvo #013 - RIP Naruto, Chaleirada na cabeça e chulé",
    "Plantão Não Ouvo #014 - Orgia de 300, Ânus do Thanos e Peru do Galvão",
    "Plantão Não Ouvo #15 - Manda Salve, Pabllo Neymar e Risca carro",
    "Recadinho Especial de Ano Novo",
    "Saindo no Soco #003 - Ana Maria Braga VS Palmirinha",
    "TEASER - Especial RPJ AO VIVO - 30/10/2017",
    "Teaser ESPECIAL RPJ SEGURA A MãE 2 (22/12/2016)",
]


def create_slug(text):
    normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    cleaned = re.sub(r'[^a-zA-Z0-9]+', '-', normalized)
    slug = cleaned.strip('-').lower()
    return slug

missing = []

for e in missing_episodes:
    missing.append(create_slug(e))


if len(sys.argv) != 2:
    print("missing path")
    exit(1)

path = sys.argv[1]

if os.stat(path).st_size == 0:
    print("Error: JSON file is empty.")
    exit(1)

with open(path, "r", encoding="utf-8") as f:
    eps = json.load(f)
    print(eps)
    eps['missing'] = missing

with open(path, "w", encoding="utf-8") as f:
    json.dump(eps, f, indent=4, ensure_ascii=False)
