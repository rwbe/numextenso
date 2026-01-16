"""
Interface gráfica do numextenso.

Uma GUI moderna usando CustomTkinter pra converter números em extenso
sem precisar abrir o terminal.

Uso:
    pip install numextenso[gui]
    python -m numextenso.gui
"""

try:
    import customtkinter as ctk
except ImportError:
    print("Pra usar a GUI, instale: pip install numextenso[gui]")
    exit(1)

from . import por_extenso, por_extenso_moeda, por_extenso_ordinal

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NumExtensoApp(ctk.CTk):
    """Janela principal da aplicação."""

    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("numextenso")
        self.geometry("600x500")
        self.minsize(500, 400)

        # Grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria todos os widgets da interface."""

        # === Header ===
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        titulo = ctk.CTkLabel(
            header,
            text="🔢 numextenso",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            header,
            text="Converte números em extenso em português brasileiro",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitulo.pack(anchor="w")

        # === Input ===
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        input_label = ctk.CTkLabel(
            input_frame,
            text="Digite o número:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.entrada = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ex: 1234.56",
            font=ctk.CTkFont(size=16),
            height=45
        )
        self.entrada.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        self.entrada.bind("<Return>", lambda e: self._converter())

        # === Opções ===
        opcoes_frame = ctk.CTkFrame(self)
        opcoes_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        opcoes_label = ctk.CTkLabel(
            opcoes_frame,
            text="Tipo de conversão:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        opcoes_label.pack(anchor="w", padx=15, pady=(15, 10))

        # Radio buttons pro tipo
        self.tipo_var = ctk.StringVar(value="cardinal")

        tipos_frame = ctk.CTkFrame(opcoes_frame, fg_color="transparent")
        tipos_frame.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkRadioButton(
            tipos_frame,
            text="Cardinal (quarenta e dois)",
            variable=self.tipo_var,
            value="cardinal",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            tipos_frame,
            text="Moeda (quarenta e dois reais)",
            variable=self.tipo_var,
            value="moeda",
            font=ctk.CTkFont(size=13)
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            tipos_frame,
            text="Ordinal (quadragésimo segundo)",
            variable=self.tipo_var,
            value="ordinal",
            font=ctk.CTkFont(size=13)
        ).pack(side="left")

        # Checkbox feminino (só pra ordinal)
        self.feminino_var = ctk.BooleanVar(value=False)
        self.feminino_check = ctk.CTkCheckBox(
            opcoes_frame,
            text="Feminino (primeira, segunda...)",
            variable=self.feminino_var,
            font=ctk.CTkFont(size=13)
        )
        self.feminino_check.pack(anchor="w", padx=15, pady=(0, 15))

        # Botão converter
        self.btn_converter = ctk.CTkButton(
            self,
            text="Converter",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            command=self._converter
        )
        self.btn_converter.grid(row=3, column=0, padx=20, pady=10, sticky="new")

        # === Resultado ===
        resultado_frame = ctk.CTkFrame(self)
        resultado_frame.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        resultado_frame.grid_columnconfigure(0, weight=1)
        resultado_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        resultado_label = ctk.CTkLabel(
            resultado_frame,
            text="Resultado:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        resultado_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.resultado_text = ctk.CTkTextbox(
            resultado_frame,
            font=ctk.CTkFont(size=15),
            wrap="word",
            state="disabled"
        )
        self.resultado_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

        # Botão copiar
        self.btn_copiar = ctk.CTkButton(
            resultado_frame,
            text="📋 Copiar",
            width=100,
            height=32,
            command=self._copiar
        )
        self.btn_copiar.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="e")

    def _converter(self):
        """Executa a conversão do número."""
        texto = self.entrada.get().strip()

        if not texto:
            self._mostrar_resultado("Digite um número pra converter!", erro=True)
            return

        try:
            # Aceita vírgula como decimal
            texto = texto.replace(",", ".")

            # Determina se é decimal
            if "." in texto:
                numero = float(texto)
            else:
                numero = int(texto)

            tipo = self.tipo_var.get()

            if tipo == "moeda":
                resultado = por_extenso_moeda(numero)
            elif tipo == "ordinal":
                if isinstance(numero, float) and numero != int(numero):
                    self._mostrar_resultado("Ordinais não suportam decimais!", erro=True)
                    return
                resultado = por_extenso_ordinal(
                    int(numero),
                    feminino=self.feminino_var.get()
                )
            else:  # cardinal
                if isinstance(numero, float) and numero != int(numero):
                    self._mostrar_resultado(
                        "Use 'Moeda' pra números decimais!",
                        erro=True
                    )
                    return
                resultado = por_extenso(int(numero))

            self._mostrar_resultado(resultado)

        except ValueError as e:
            self._mostrar_resultado(f"Erro: {e}", erro=True)
        except Exception as e:
            self._mostrar_resultado(f"Erro inesperado: {e}", erro=True)

    def _mostrar_resultado(self, texto: str, erro: bool = False):
        """Mostra o resultado na caixa de texto."""
        self.resultado_text.configure(state="normal")
        self.resultado_text.delete("1.0", "end")
        self.resultado_text.insert("1.0", texto)
        self.resultado_text.configure(state="disabled")

        # Muda cor se for erro
        if erro:
            self.resultado_text.configure(text_color="#ff6b6b")
        else:
            self.resultado_text.configure(text_color=("gray10", "gray90"))

    def _copiar(self):
        """Copia o resultado pro clipboard."""
        self.resultado_text.configure(state="normal")
        texto = self.resultado_text.get("1.0", "end").strip()
        self.resultado_text.configure(state="disabled")

        if texto:
            self.clipboard_clear()
            self.clipboard_append(texto)

            # Feedback visual
            texto_original = self.btn_copiar.cget("text")
            self.btn_copiar.configure(text="✓ Copiado!")
            self.after(1500, lambda: self.btn_copiar.configure(text=texto_original))


def main():
    """Inicia a GUI."""
    app = NumExtensoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
