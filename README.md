# numextenso 🇧🇷

Biblioteca Python pra converter números em extenso em português brasileiro.

Sabe quando você precisa escrever "mil duzentos e trinta e quatro" num cheque ou fatura? Então, essa biblioteca faz isso pra você.

## Instalação

```bash
pip install numextenso
```

Ou direto do repositório:

```bash
pip install https://github.com/rwbe/numextenso.git
```

## Uso rápido

### No código Python

```python
from numextenso import por_extenso, por_extenso_moeda, por_extenso_ordinal

# Números inteiros
por_extenso(42)          # 'quarenta e dois'
por_extenso(1001)        # 'mil e um'
por_extenso(1000000)     # 'um milhão'
por_extenso(-50)         # 'menos cinquenta'

# Valores em reais
por_extenso_moeda(1234.56)  # 'mil duzentos e trinta e quatro reais e cinquenta e seis centavos'
por_extenso_moeda(0.99)     # 'noventa e nove centavos'

# Ordinais
por_extenso_ordinal(1)                  # 'primeiro'
por_extenso_ordinal(3, feminino=True)   # 'terceira'
por_extenso_ordinal(42)                 # 'quadragésimo segundo'
```

### Na linha de comando

```bash
# Número simples
numextenso 1234
# Saída: mil duzentos e trinta e quatro

# Com moeda
numextenso 99.90 --moeda
# Saída: noventa e nove reais e noventa centavos

# Ordinal
numextenso 5 --ordinal
# Saída: quinto

# Ordinal feminino
numextenso 3 -o -f
# Saída: terceira
```

## Licença

MIT
