"""
Aqui ficam todas as palavras usadas na conversão.

Separei num arquivo próprio pra facilitar manutenção e deixar
o código principal mais limpo. Se um dia precisar adicionar
outra língua, é só criar outro arquivo de constantes.
"""

# Números de 0 a 19 (casos especiais do português)
# Do 11 ao 19 não segue o padrão "dez e um", então precisam de tratamento especial
UNIDADES = (
    "zero", "um", "dois", "três", "quatro",
    "cinco", "seis", "sete", "oito", "nove",
    "dez", "onze", "doze", "treze", "quatorze",
    "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"
)

# Dezenas (20, 30, 40...)
DEZENAS = (
    "", "", "vinte", "trinta", "quarenta",
    "cinquenta", "sessenta", "setenta", "oitenta", "noventa"
)

# Centenas (100, 200, 300...)
# Note que 100 sozinho é "cem", mas 101-199 usa "cento"
CENTENAS = (
    "", "cento", "duzentos", "trezentos", "quatrocentos",
    "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"
)

# Classes numéricas (mil, milhão, bilhão, trilhão)
# Cada tupla tem: (singular, plural)
# A concordância muda: "um milhão" vs "dois milhões"
CLASSES = (
    ("", ""),                      # unidades (sem nome)
    ("mil", "mil"),                # milhares (não muda no plural)
    ("milhão", "milhões"),         # milhões
    ("bilhão", "bilhões"),         # bilhões
    ("trilhão", "trilhões"),       # trilhões
)

# Ordinais masculinos (1º, 2º, 3º...)
ORDINAIS_MASCULINO = {
    1: "primeiro", 2: "segundo", 3: "terceiro", 4: "quarto", 5: "quinto",
    6: "sexto", 7: "sétimo", 8: "oitavo", 9: "nono", 10: "décimo",
    11: "décimo primeiro", 12: "décimo segundo", 13: "décimo terceiro",
    14: "décimo quarto", 15: "décimo quinto", 16: "décimo sexto",
    17: "décimo sétimo", 18: "décimo oitavo", 19: "décimo nono",
    20: "vigésimo", 30: "trigésimo", 40: "quadragésimo", 50: "quinquagésimo",
    60: "sexagésimo", 70: "septuagésimo", 80: "octogésimo", 90: "nonagésimo",
    100: "centésimo", 200: "ducentésimo", 300: "trecentésimo",
    400: "quadringentésimo", 500: "quingentésimo", 600: "sexcentésimo",
    700: "septingentésimo", 800: "octingentésimo", 900: "nongentésimo",
    1000: "milésimo"
}

# Ordinais femininos
ORDINAIS_FEMININO = {
    1: "primeira", 2: "segunda", 3: "terceira", 4: "quarta", 5: "quinta",
    6: "sexta", 7: "sétima", 8: "oitava", 9: "nona", 10: "décima",
    11: "décima primeira", 12: "décima segunda", 13: "décima terceira",
    14: "décima quarta", 15: "décima quinta", 16: "décima sexta",
    17: "décima sétima", 18: "décima oitava", 19: "décima nona",
    20: "vigésima", 30: "trigésima", 40: "quadragésima", 50: "quinquagésima",
    60: "sexagésima", 70: "septuagésima", 80: "octogésima", 90: "nonagésima",
    100: "centésima", 200: "ducentésima", 300: "trecentésima",
    400: "quadringentésima", 500: "quingentésima", 600: "sexcentésima",
    700: "septingentésima", 800: "octingentésima", 900: "nongentésima",
    1000: "milésima"
}

# Moeda brasileira
MOEDA_BRL = {
    "inteiro_singular": "real",
    "inteiro_plural": "reais",
    "decimal_singular": "centavo",
    "decimal_plural": "centavos",
    "simbolo": "R$"
}
