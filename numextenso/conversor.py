"""
O coração da biblioteca - onde a mágica acontece.

A ideia é simples: quebrar o número em grupos de 3 dígitos
e converter cada grupo, adicionando a classe correspondente
(mil, milhão, bilhão, etc).

Exemplo: 1.234.567
- 1 -> "um" + "milhão"
- 234 -> "duzentos e trinta e quatro" + "mil"
- 567 -> "quinhentos e sessenta e sete"
- Resultado: "um milhão, duzentos e trinta e quatro mil, quinhentos e sessenta e sete"
"""

from .constantes import (
    CENTENAS,
    CLASSES,
    DEZENAS,
    MOEDA_BRL,
    ORDINAIS_FEMININO,
    ORDINAIS_MASCULINO,
    UNIDADES,
)


def _converter_grupo(n: int) -> str:
    """
    Converte um número de 0 a 999 em extenso.

    Essa é a função base - ela sabe lidar com centenas, dezenas e unidades.
    Números maiores são quebrados em grupos de 3 dígitos e essa função
    é chamada pra cada grupo.
    """
    if n == 0:
        return ""

    if n < 20:
        return UNIDADES[n]

    if n < 100:
        dezena = n // 10
        unidade = n % 10
        if unidade == 0:
            return DEZENAS[dezena]
        return f"{DEZENAS[dezena]} e {UNIDADES[unidade]}"

    # Centenas
    centena = n // 100
    resto = n % 100

    # Caso especial: 100 é "cem", não "cento"
    if n == 100:
        return "cem"

    if resto == 0:
        return CENTENAS[centena]

    return f"{CENTENAS[centena]} e {_converter_grupo(resto)}"


def por_extenso(numero: int | float, aceitar_decimal: bool = False) -> str:
    """
    Converte um número inteiro em extenso.

    Parâmetros:
        numero: O número a ser convertido (até trilhões)
        aceitar_decimal: Se True, trunca decimais; se False, levanta erro

    Retorna:
        String com o número por extenso

    Exemplos:
        >>> por_extenso(0)
        'zero'
        >>> por_extenso(100)
        'cem'
        >>> por_extenso(1001)
        'mil e um'
        >>> por_extenso(1000000)
        'um milhão'
    """
    # Validação de tipo
    if not isinstance(numero, (int, float)):
        raise TypeError(f"Esperava int ou float, recebi {type(numero).__name__}")

    # Trata decimais
    if isinstance(numero, float):
        if not aceitar_decimal and numero != int(numero):
            raise ValueError(
                "Número decimal passado pra função de inteiros. "
                "Use por_extenso_moeda() pra valores com centavos."
            )
        numero = int(numero)

    # Números negativos
    if numero < 0:
        return f"menos {por_extenso(abs(numero))}"

    # Zero é caso especial
    if numero == 0:
        return "zero"

    # Limite: trilhões
    max_valor = 999_999_999_999_999
    if numero > max_valor:
        raise ValueError(f"Número muito grande. Máximo suportado: {max_valor:,}")

    # Quebra em grupos de 3 dígitos (da direita pra esquerda)
    grupos = []
    temp = numero
    while temp > 0:
        grupos.append(temp % 1000)
        temp //= 1000

    # Converte cada grupo e adiciona a classe
    partes = []
    for i, grupo in enumerate(grupos):
        if grupo == 0:
            continue

        texto_grupo = _converter_grupo(grupo)
        nome_classe = CLASSES[i]

        # Adiciona nome da classe (mil, milhão, etc)
        if i > 0:  # Não adiciona nada pras unidades
            # Concordância especial pro português:
            # - "mil" (sem "um" na frente)
            # - "um milhão", "dois milhões" (com número e concordância)
            if i == 1:  # milhares
                if grupo == 1:
                    texto_grupo = "mil"  # "um mil" -> "mil"
                else:
                    texto_grupo += " mil"
            else:  # milhões, bilhões, trilhões
                plural = grupo > 1
                if grupo == 1:
                    texto_grupo = "um " + nome_classe[0]  # "um milhão"
                else:
                    texto_grupo += " " + nome_classe[1 if plural else 0]

        partes.append((texto_grupo, grupo))

    # Junta as partes com conectivos apropriados
    partes.reverse()
    grupos.reverse()

    if len(partes) == 1:
        return partes[0][0]

    resultado = []
    for i, (texto, valor) in enumerate(partes):
        resultado.append(texto)

        # Decide se usa vírgula, "e" ou espaço
        if i < len(partes) - 1:
            prox_valor = partes[i + 1][1]
            # Usa "e" se o próximo é < 100 ou centena exata (100, 200, etc)
            if prox_valor < 100 or prox_valor % 100 == 0:
                resultado.append(" e ")
            # Se o grupo atual é só "mil" (1000) e próximo tem centenas com resto,
            # usa só espaço (não vírgula)
            elif valor == 1 and texto == "mil":
                resultado.append(" ")
            else:
                resultado.append(", ")

    return "".join(resultado)


def por_extenso_moeda(valor: float | int, moeda: dict = None) -> str:
    """
    Converte um valor monetário em extenso.

    Parâmetros:
        valor: O valor a ser convertido (ex: 1234.56)
        moeda: Dicionário com nomes da moeda (opcional, padrão é BRL)

    Retorna:
        String com o valor por extenso

    Exemplos:
        >>> por_extenso_moeda(1)
        'um real'
        >>> por_extenso_moeda(1234.56)
        'mil duzentos e trinta e quatro reais e cinquenta e seis centavos'
        >>> por_extenso_moeda(0.01)
        'um centavo'
    """
    if moeda is None:
        moeda = MOEDA_BRL

    if not isinstance(valor, (int, float)):
        raise TypeError(f"Esperava int ou float, recebi {type(valor).__name__}")

    if valor < 0:
        return f"menos {por_extenso_moeda(abs(valor), moeda)}"

    # Separa inteiros e centavos
    # Usa round pra evitar problemas de ponto flutuante (0.1 + 0.2 = 0.30000000004)
    valor_cents = round(valor * 100)
    inteiros = valor_cents // 100
    centavos = valor_cents % 100

    partes = []

    # Parte inteira
    if inteiros > 0:
        texto_inteiro = por_extenso(inteiros)
        nome_moeda = moeda["inteiro_plural"] if inteiros > 1 else moeda["inteiro_singular"]
        partes.append(f"{texto_inteiro} {nome_moeda}")

    # Centavos
    if centavos > 0:
        texto_centavos = por_extenso(centavos)
        nome_centavos = moeda["decimal_plural"] if centavos > 1 else moeda["decimal_singular"]
        partes.append(f"{texto_centavos} {nome_centavos}")

    if not partes:
        return f"zero {moeda['inteiro_plural']}"

    return " e ".join(partes)


def por_extenso_ordinal(numero: int, feminino: bool = False) -> str:
    """
    Converte um número em ordinal por extenso.

    Parâmetros:
        numero: O número a ser convertido (1-1000)
        feminino: Se True, usa forma feminina (primeira, segunda...)

    Retorna:
        String com o ordinal por extenso

    Exemplos:
        >>> por_extenso_ordinal(1)
        'primeiro'
        >>> por_extenso_ordinal(1, feminino=True)
        'primeira'
        >>> por_extenso_ordinal(42)
        'quadragésimo segundo'
    """
    if not isinstance(numero, int):
        raise TypeError(f"Ordinais só funcionam com inteiros, recebi {type(numero).__name__}")

    if numero < 1 or numero > 1000:
        raise ValueError("Ordinais suportados de 1 a 1000")

    tabela = ORDINAIS_FEMININO if feminino else ORDINAIS_MASCULINO

    # Caso direto na tabela
    if numero in tabela:
        return tabela[numero]

    # Decompõe o número
    partes = []

    # Centenas
    if numero >= 100:
        centena = (numero // 100) * 100
        partes.append(tabela[centena])
        numero = numero % 100

    # Dezenas
    if numero >= 20:
        dezena = (numero // 10) * 10
        partes.append(tabela[dezena])
        numero = numero % 10

    # Unidades (ou 11-19)
    if numero > 0:
        partes.append(tabela[numero])

    return " ".join(partes)
