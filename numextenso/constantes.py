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
