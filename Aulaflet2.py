import flet as ft

def main(page: ft.Page):
    page.title = "PizzaDev"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    titulo = ft.Text("PizzaDev", size=40, weight=ft.FontWeight.BOLD)
    subtitulo = ft.Text("Sua pizza potiguar.", size=20, weight=ft.FontWeight.BOLD)
    versao = ft.Text("Versão didática", size=8, weight=ft.FontWeight.BOLD)
    subtitulo2 = ft.Text(f"Instruções: \nEscolha o sabor e tamanho da sua pizza.", size=12, weight=ft.FontWeight.BOLD)

    mensagem = ft.Text(
        "Nenhuma pizza selecionada",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.RED
    )
    
    def escolher(sabor):
        mensagem.value = f"Selecionada: {sabor}"
        page.update()

    card1 = ft.Container(
        padding=15,
        border_radius=12,
        bgcolor=ft.colors.WHITE,
        on_click=lambda e: escolher("Muçarela"),
        content=ft.Column([
            ft.Text("Muçarela", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("muçarela, cebola e azeitona"),
            ft.Row([ft.Text("M: R$ 32"), ft.Text("G: R$ 42")])
        ])
    )

    card2 = ft.Container(
            padding=15,
            border_radius=12,
            bgcolor=ft.colors.WHITE,
            on_click=lambda e: escolher("Calabresa"),
            content=ft.Column([
                ft.Text("Calabresa", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("calabresa, cebola, muçarela e azeitona"),
                ft.Row([ft.Text("M: R$ 32"), ft.Text("G: R$ 42")])
            ])
        )
    
    card3 = ft.Container(
            padding=15,
            border_radius=12,
            bgcolor=ft.colors.WHITE,
            on_click=lambda e: escolher("Frango"),
            content=ft.Column([
                ft.Text("Frango", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("frango, cebola, muçarela e azeitona"),
                ft.Row([ft.Text("M: R$ 32"), ft.Text("G: R$ 42")])
            ])
        )
    
    card4 = ft.Container(
            padding=15,
            border_radius=12,
            bgcolor=ft.colors.WHITE,
            on_click=lambda e: escolher("Portuguesa"),
            content=ft.Column([
                ft.Text("Portuguesa", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("milho, ervilha, presunto, cebola e muçarela"),
                ft.Row([ft.Text("M: R$ 32"), ft.Text("G: R$ 42")])
            ])
        )
    
    linhadecards = ft.Row(
        controls = [card1, card2, card3, card4],
        wrap = True,
        spacing = 20,
        run_spacing = 20
    )

    quantidade = ft.TextField(label="Quantidade", value="1")
    tamanho = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="M", label="M"),
            ft.Radio(value="G", label="G")
        ])
    )
    resultado = ft.Text()

    def calcular(e):
        if tamanho.value is None:
            resultado.value = "Selecione o tamanho da pizza."
            page.update()
            return

        if not quantidade.value or not quantidade.value.isdigit():
            resultado.value = "Digite uma quantidade inteira."
            page.update()
            return

        qtd = int(quantidade.value)
        if qtd < 1 or qtd > 10:
            resultado.value = "Quantidade deve ficar entre 1 e 10."
            page.update()
            return

        preco = 32 if tamanho.value == "M" else 42
        resultado.value = f"Parcial: R$ {preco * qtd:.2f}"
        page.update()

    page.add(
        titulo,
        subtitulo,
        versao,
        subtitulo2,
        mensagem,
        linhadecards,
        quantidade,
        ft.Text("Tamanho:"),
        tamanho,
        ft.ElevatedButton("Calcular", on_click=calcular),
        resultado
    )

ft.app(target=main)
