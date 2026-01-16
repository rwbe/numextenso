"""numextenso - Converte números em extenso em português brasileiro.

Uma biblioteca simples e direta pra transformar números em texto.
Útil pra cheques, faturas, documentos e qualquer lugar onde você
precisa escrever o valor por extenso.
"""

from .conversor import por_extenso, por_extenso_moeda, por_extenso_ordinal

__version__ = "1.0.0"
__author__ = "Ricardo Willian"
__all__ = ["por_extenso", "por_extenso_moeda", "por_extenso_ordinal"]
