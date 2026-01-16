# Como o numextenso funciona

Vou explicar a lógica por trás da conversão de números em extenso. É mais simples do que parece!

## O problema

Converter números em palavras parece fácil até você perceber todas as irregularidades do português:

- **11 a 19**: não é "dez e um", é "onze"
- **100**: sozinho é "cem", mas 101 é "cento e um"
- **Milhão**: "um milhão" mas "dois milhões"
- **Conectivos**: "mil e um" mas "mil duzentos" (sem "e")

## A solução

### 1. Tabelas de palavras

Primeiro, criamos tabelas com todas as palavras que vamos precisar:

```python
# 0-19 são casos especiais
UNIDADES = ("zero", "um", "dois", ..., "dezenove")

# Dezenas (20, 30, 40...)
DEZENAS = ("", "", "vinte", "trinta", ...)

# Centenas
CENTENAS = ("", "cento", "duzentos", "trezentos", ...)

# Classes (mil, milhão, bilhão...)
CLASSES = (
    ("", ""),
    ("mil", "mil"),
    ("milhão", "milhões"),
    ...
)
```

### 2. Dividir pra conquistar

A sacada é quebrar o número em grupos de 3 dígitos:

```
1.234.567.890
  |   |   |  └── 890 (unidades)
  |   |   └───── 567 (milhares)
  |   └───────── 234 (milhões)
  └───────────── 1   (bilhões)
```

Cada grupo segue a mesma lógica (centenas + dezenas + unidades), só muda o nome da classe.

### 3. Converter cada grupo

Pra converter um grupo de até 999:

```python
def _converter_grupo(n):
    # Casos diretos: 0-19
    if n < 20:
        return UNIDADES[n]

    # Dezenas: 20-99
    if n < 100:
        dezena = n // 10
        unidade = n % 10
        if unidade == 0:
            return DEZENAS[dezena]  # "vinte"
        return f"{DEZENAS[dezena]} e {UNIDADES[unidade]}"  # "vinte e um"

    # Centenas: 100-999
    if n == 100:
        return "cem"  # Caso especial!

    centena = n // 100
    resto = n % 100
    if resto == 0:
        return CENTENAS[centena]  # "duzentos"
    return f"{CENTENAS[centena]} e {_converter_grupo(resto)}"  # "duzentos e trinta e quatro"
```

### 4. Juntar tudo

Depois de converter cada grupo, junta com as classes:

```python
# 1.234.567 vira:
grupos = [567, 234, 1]  # Da direita pra esquerda

# Converte cada um:
# 567 -> "quinhentos e sessenta e sete"
# 234 -> "duzentos e trinta e quatro" + " mil"
# 1   -> "um" + " milhão"

# Junta:
# "um milhão, duzentos e trinta e quatro mil, quinhentos e sessenta e sete"
```

### 5. Conectivos: "e" ou vírgula?

A regra pra decidir se usa "e" ou vírgula:

- **Usa "e"** quando o próximo grupo é menor que 100 ou é exatamente 100
  - "mil **e** um" (1.001)
  - "mil **e** cem" (1.100)
- **Usa vírgula** nos outros casos (A vírgula é estilística, não obrigatória)
  - "mil**,** duzentos e trinta e quatro" (1.234)

## Moeda

Pra moeda, a lógica é:

1. Separa inteiros e centavos
2. Converte cada parte
3. Adiciona "reais" e "centavos"
4. Cuida da concordância ("um real" vs "dois reais")

```python
# 1234.56 vira:
inteiros = 1234  # "mil duzentos e trinta e quatro reais"
centavos = 56    # "cinquenta e seis centavos"
# Resultado: "mil duzentos e trinta e quatro reais e cinquenta e seis centavos"
```

## Ordinais

Ordinais são mais simples: usamos uma tabela e decompomos o número:

```python
# 42 -> "quadragésimo segundo"
# = ORDINAIS[40] + " " + ORDINAIS[2]
# = "quadragésimo" + " " + "segundo"
```

## Performance

A complexidade é O(log n) - proporcional ao número de dígitos. Pra números até trilhões (15 dígitos), é instantâneo.

## Limitações conhecidas

1. **Limite de trilhões**: poderia suportar mais, mas pra quê? Se você tá escrevendo "um quatrilhão" num cheque, o problema não é a biblioteca.

2. **"de" antes de moeda**: em "um milhão de reais", o "de" não tá implementado. Funciona, mas não fica 100% correto gramaticalmente.
