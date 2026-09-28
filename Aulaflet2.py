import flet as ft

PIZZAS = [
    {"id":"P01", "nome":"Marguerita", "m":22, "g":35},
    {"id":"P01", "nome":"Portuguesa", "m":35, "g":45},
    {"id":"P01", "nome":"Frango", "m":32, "g":42},
    {"id":"P01", "nome":"Muçarela", "m":30, "g":40},
    {"id":"P02", "nome":"Calabresa", "m":32, "g":42},
]

def main(page: ft.Page):
    page.title = "PizzaDev"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER 
    
    titulo = ft.Text(
        "PizzaDev",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
        text_align=ft.TextAlign.CENTER,
    )

    subtitulo = ft.Text(
        "Sua pizza potiguar.",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
        text_align=ft.TextAlign.CENTER,
    )

    versao = ft.Text(
        "Versão didática",
        size=8,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
        text_align=ft.TextAlign.CENTER,
    )

    subtitulo2 = ft.Text(
        "Instruções: \nEscolha o sabor e tamanho da sua pizza.",
        size=12,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
        text_align=ft.TextAlign.CENTER,
    )

    mensagem = ft.Text(
        "Nenhuma pizza selecionada",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.RED
    )
    
    def escolher(sabor):
        mensagem.value = f"Selecionada: {sabor}"
        page.update()

    """card1 = ft.Container(
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
        )"""
    
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

    def criar_card(sabor):
        return ft.Container(
            padding=12,
            on_click=lambda e: escolher(sabor["nome"]),
            border_radius=12,
            content=ft.Column([
                ft.Text(sabor["nome"], size=20),
                ft.Text(f'M: R$ {sabor["m"]} | G: R$ {sabor["g"]}')
            ])
        )
    cards = []
    for sabor in PIZZAS:
        card = criar_card(sabor)
        cards.append(card)
        
    linhadecards = ft.Row(
            controls=cards,
            wrap=True,
            spacing=20,
            run_spacing=20,
        )

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
        resultado,
    )

ft.app(target=main)
