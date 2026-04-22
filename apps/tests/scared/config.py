SCARED_CODE = "scared"
SCARED_NAME = "SCARED - Screen for Child Anxiety Related Emotional Disorders"

CHILD_MAX_AGE = 12

SCARED_FORMS = {
    "child": "Autorrelato",
    "parent": "Pais/Cuidadores",
}

OPCOES_RESPOSTA = {
    0: "Nunca ou raramente verdadeiro",
    1: "Algumas vezes verdadeiro",
    2: "Bastante ou frequentemente verdadeiro",
}

ITENS_PAIS = {
    1: "Quando meu/minha filho(a) fica com medo, ele/ela tem dificuldades para respirar.",
    2: "Meu/minha filho(a) sente dor de cabeça quando está na escola.",
    3: "Meu/minha filho(a) não gosta de estar com pessoas que não conhece bem.",
    4: "Meu/minha filho(a) fica com medo quando dorme fora de casa.",
    5: "Meu/minha filho(a) se preocupa se as outras pessoas gostam dele/dela.",
    6: "Quando meu/minha filho(a) fica com medo, ele/ela se sente como se fosse desmaiar.",
    7: "Meu/minha filho(a) é nervoso(a).",
    8: "Meu/minha filho(a) me segue aonde quer que eu vá.",
    9: "As pessoas me dizem que meu/minha filho(a) parece nervoso(a).",
    10: "Meu/minha filho(a) fica nervoso(a) com pessoas que ele não conhece bem.",
    11: "Meu/minha filho(a) tem dor de barriga na escola.",
    12: "Quando meu/minha filho(a) fica com medo, ele acha que vai enlouquecer.",
    13: "Meu/minha filho(a) tem medo de dormir sozinho(a).",
    14: "Meu/minha filho(a) se preocupa em ser tão bom quanto as outras crianças.",
    15: "Quando meu/minha filho(a) fica com medo, ele/ela tem a impressão de que as coisas não são reais.",
    16: "Meu/minha filho(a) tem pesadelos com coisas ruins acontecendo com os seus pais.",
    17: "Meu/minha filho(a) fica preocupado quando tem que ir à escola.",
    18: "Quando meu/minha filho(a) fica com medo, o seu coração bate rápido.",
    19: "Quando meu/minha filho(a) fica nervoso, ele treme de medo.",
    20: "Meu/minha filho(a) tem pesadelos com alguma coisa ruim acontecendo com ele.",
    21: "Meu/minha filho(a) fica preocupado se as coisas vai dar certo para ele/ela.",
    22: "Quando meu/minha filho(a) fica com medo, ele sua muito.",
    23: "Meu/minha filho(a) é muito preocupado(a).",
    24: "Meu/minha filho(a) fica com muito medo(a) sem nenhum motivo.",
    25: "Meu/minha filho(a) tem medo de ficar sozinho(a) em casa.",
    26: "Meu/minha filho(a) tem dificuldade para falar com pessoas que não conhece bem.",
    27: "Quando meu/minha filho(a) fica com medo, ele se sente sufocado(a).",
    28: "As pessoas me dizem que meu/minha filho(a) se preocupa demais.",
    29: "Meu/minha filho(a) não gosta de ficar longe de sua família.",
    30: "Meu/minha filho(a) tem medo de ter ataques de ansiedade (ou ataques de pânico).",
    31: "Meu/minha filho(a) tem medo de que alguma coisa ruim possa aconteça comigo ou com o pai / a mãe dele/dela.",
    32: "Meu/minha filho(a) fica com vergonha na frente de pessoas que não conhece bem.",
    33: "Meu/minha filho(a) se preocupa muito com o que vai acontecer no futuro.",
    34: "Quando meu/minha filho(a) fica com medo, ele tem vontade de vomitar.",
    35: "Meu/minha filho(a) se preocupa muito em fazer as coisas bem feitas.",
    36: "Meu/minha filho(a) tem medo de ir à escola.",
    37: "Meu/minha filho(a) se preocupa com as coisas que já aconteceram.",
    38: "Quando meu/minha filho(a) fica com medo, ele se sente tonto(a).",
    39: "Meu/minha filho(a) fica nervoso(a) quando está com outras crianças ou adultos e tem que fazer algo enquanto eles lhe olham (por exemplo, ler em voz alta, falar, jogar um jogo ou praticar um esporte).",
    40: "Meu/minha filho(a) fica nervoso(a) quando vai a festas, bailes ou qualquer lugar onde estejam pessoas que ele não conhece bem.",
    41: "Meu/minha filho(a) é tímido(a).",
}

ITENS_AUTORRELATO = {
    1: "Quando eu fico com medo, eu tenho dificuldade de respirar.",
    2: "Eu sinto dor de cabeça quando estou na escola.",
    3: "Eu não gosto de estar com pessoas que não conheço bem.",
    4: "Fico com medo quando durmo fora de casa.",
    5: "Eu me preocupo se outras pessoas gostam de mim.",
    6: "Quando eu fico com medo, eu sinto como se eu fosse desmaiar.",
    7: "Eu sou nervoso(a).",
    8: "Eu sigo a minha mãe ou o meu pai aonde eles vão.",
    9: "As pessoas me dizem que pareço nervoso(a).",
    10: "Eu fico nervoso(a) com pessoas que eu não conheço bem.",
    11: "Eu tenho dor de barriga na escola.",
    12: "Quando eu fico com medo, eu acho que vou enlouquecer.",
    13: "Eu tenho medo de dormir sozinho(a).",
    14: "Eu me preocupo em ser tão bom quanto as outras crianças.",
    15: "Quando eu fico com medo, tenho a impressão de que as coisas não são reais.",
    16: "Eu tenho pesadelos com coisas ruins acontecendo com os meus pais.",
    17: "Eu fico preocupo quando tenho que ir à escola.",
    18: "Quando eu fico com medo, o meu coração bate rápido.",
    19: "Quando eu fico nervoso(a), eu tremo de medo.",
    20: "Eu tenho pesadelos com alguma coisa ruim acontecendo comigo.",
    21: "Eu fico preocupado(a) se as coisas vão dar certo para mim.",
    22: "Quando eu fico com medo, eu suo muito.",
    23: "Eu sou muito preocupado(a).",
    24: "Eu fico com muito medo sem nenhum motivo.",
    25: "Eu tenho medo de ficar sozinho(a) em casa.",
    26: "Eu tenho dificuldades para falar com pessoas que não conheço bem.",
    27: "Quando eu fico com medo, eu me sinto sufocado.",
    28: "As pessoas dizem que eu me preocupo demais.",
    29: "Eu não gosto de ficar longe da família.",
    30: "Eu tenho medo de ter ataques de ansiedade (ou ataques de pânico).",
    31: "Eu tenho medo de que alguma coisa ruim aconteça com meus pais.",
    32: "Eu fico com vergonha na frente de pessoas que não conheço bem.",
    33: "Eu me preocupo muito com o que vai acontecer no futuro.",
    34: "Quando eu fico com medo, eu tenho vontade de vomitar.",
    35: "Eu me preocupo muito em fazer as coisas bem feitas.",
    36: "Eu tenho medo de ir à escola.",
    37: "Eu me preocupo com as coisas que já aconteceram.",
    38: "Quando eu fico com medo, eu me sinto tonto(a).",
    39: "Fico nervoso(a) quando estou com outras crianças ou adultos e tenho que fazer algo enquanto eles me olham (por exemplo, ler em voz alta, falar, jogar um jogo ou praticar um esporte).",
    40: "Eu fico nervoso(a) para ir a festas, bailes ou qualquer lugar onde estejam pessoas que não conheço bem.",
    41: "Eu sou tímido(a).",
}

FATORES = {
    "panico_sintomas_somaticos": [1, 6, 9, 12, 15, 18, 19, 22, 24, 27, 30, 34, 38],
    "ansiedade_generalizada": [5, 7, 14, 21, 23, 28, 33, 35, 37],
    "ansiedade_separacao": [4, 8, 13, 16, 20, 25, 29, 31],
    "fobia_social": [3, 10, 26, 32, 39, 40, 41],
    "evitacao_escolar": [2, 11, 17, 36],
}

FATORES_TOTAL = list(range(1, 42))

FATORES_DISPLAY_NAMES = {
    "panico_sintomas_somaticos": "Pânico / Sintomas Somáticos",
    "ansiedade_generalizada": "Ansiedade Generalizada",
    "ansiedade_separacao": "Ansiedade de Separação",
    "fobia_social": "Fobia Social",
    "evitacao_escolar": "Evitação Escolar",
    "total": "Total",
}

FATORES_ANALISE = [
    "panico_sintomas_somaticos",
    "ansiedade_generalizada",
    "ansiedade_separacao",
    "fobia_social",
    "evitacao_escolar",
    "total",
]

PAIS_MAXIMOS = {
    "panico_sintomas_somaticos": 26,
    "ansiedade_generalizada": 18,
    "ansiedade_separacao": 16,
    "fobia_social": 14,
    "evitacao_escolar": 8,
    "total": 82,
}

SCARED_ITEMS_BY_FORM = {
    "child": ITENS_AUTORRELATO,
    "parent": ITENS_PAIS,
}
