"""
Interface de linha de comando (CLI) do numextenso.

Uso:
    numextenso 1234              # Saída: mil duzentos e trinta e quatro
    numextenso 1234.56 --moeda   # Saída: mil duzentos e trinta e quatro reais...
    numextenso 5 --ordinal       # Saída: quinto
    numextenso 5 -o -f           # Saída: quinta (ordinal feminino)
"""

import argparse
import sys

from . import __version__, por_extenso, por_extenso_moeda, por_extenso_ordinal


def criar_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos."""
    parser = argparse.ArgumentParser(
        prog="numextenso",
        description="Converte números em extenso em português brasileiro.",
        epilog="Exemplos:\n"
               "  numextenso 1234\n"
               "  numextenso 99.90 --moeda\n"
               "  numextenso 3 --ordinal --feminino\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "numero",
        type=str,
        help="O número a ser convertido (use ponto pra decimal: 1234.56)"
    )

    parser.add_argument(
        "-m", "--moeda",
        action="store_true",
        help="Formata como valor monetário (reais e centavos)"
    )

    parser.add_argument(
        "-o", "--ordinal",
        action="store_true",
        help="Converte para ordinal (primeiro, segundo...)"
    )

    parser.add_argument(
        "-f", "--feminino",
        action="store_true",
        help="Usa forma feminina do ordinal (primeira, segunda...)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    return parser


def main(args: list = None) -> int:
    """
    Função principal do CLI.

    Retorna:
        0 em caso de sucesso, 1 em caso de erro
    """
    parser = criar_parser()
    opts = parser.parse_args(args)

    try:
        # Converte o input pra número
        numero_str = opts.numero.replace(",", ".")  # aceita vírgula como decimal

        if "." in numero_str:
            numero = float(numero_str)
        else:
            numero = int(numero_str)

        # Decide qual conversão usar
        if opts.ordinal:
            if isinstance(numero, float):
                print("Erro: ordinais não suportam decimais", file=sys.stderr)
                return 1
            resultado = por_extenso_ordinal(numero, feminino=opts.feminino)

        elif opts.moeda:
            resultado = por_extenso_moeda(numero)

        else:
            if isinstance(numero, float) and numero != int(numero):
                print(
                    "Dica: use --moeda pra converter valores com centavos",
                    file=sys.stderr
                )
                return 1
            resultado = por_extenso(int(numero))

        print(resultado)
        return 0

    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
