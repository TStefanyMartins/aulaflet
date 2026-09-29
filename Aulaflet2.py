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
    page.bgcolor = "#F5F5F5"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"pizza": None, "tamanho": "M", "quantidade": 1}

    carrinho = []
    lista_visual = ft.ListView(spacing=8, expand=True)
    subtotal_texto = ft.Text("Subtotal: R$ 0,00")

    area = ft.Container(expand=True)

    def atualizar_carrinho():
        lista_visual.controls.clear()
        subtotal = 0

        for item in carrinho:
            parcial = item["preco"] * item["qtd"]
            subtotal += parcial

            lista_visual.controls.append(
                ft.Text(
                    f'{item["nome"]} - Tamanho: {item["tamanho"]} - '
                    f'Quantidade: {item["qtd"]} - R$ {parcial:.2f}'
                )
            )

        subtotal_texto.value = f"Subtotal: R$ {subtotal:.2f}"
        page.update()

    def adicionar_ao_carrinho():
        pizza = estado["pizza"]
        tamanho = estado["tamanho"]
        quantidade = estado["quantidade"]

        preco = pizza["m"] if tamanho == "M" else pizza["g"]

        for item in carrinho:
            if item["nome"] == pizza["nome"] and item["tamanho"] == tamanho:

                item["qtd"] = min(item["qtd"] + quantidade, 10)

                atualizar_carrinho()
                return

        carrinho.append({
            "nome": pizza["nome"],
            "tamanho": tamanho,
            "qtd": min(quantidade, 10),
            "preco": preco
        })

        atualizar_carrinho()

    def mostrar_inicio():
        area.content = ft.Column(
            controls=[
                ft.Text("PizzaDev", size=32, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Text("Bem-vindo ao PizzaDev", size=20, color="#000000"),
                ft.ElevatedButton(
                    "Abrir Cardápio",
                    on_click=lambda e: mostrar_cardapio()
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
        area.update()

    def mostrar_cardapio():
        cards = []

        for pizza in PIZZAS:
            card = ft.Container(
                padding=15,
                border_radius=12,
                bgcolor="#FFFFFF",
                on_click=lambda e, p=pizza: selecionar_pizza(p),
                content=ft.Column([
                    ft.Text(
                        pizza["nome"],
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#000000"
                    ),
                    ft.Row([
                        ft.Text(f"M: R$ {pizza['m']}", color="#000000"),
                        ft.Text(f"G: R$ {pizza['g']}", color="#000000"),
                    ]),
                ])
            )
            cards.append(card)

        area.content = ft.Column(
            controls=[
                ft.Text(
                    "Nosso Cardápio",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),
                ft.Row(
                    controls=cards,
                    wrap=True,
                    spacing=15,
                    run_spacing=15
                ),
                ft.ElevatedButton(
                    "Voltar para Início",
                    on_click=lambda e: mostrar_inicio()
                )
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO
        )
        area.update()

    def selecionar_pizza(pizza):
        estado["pizza"] = pizza
        mostrar_selecao()

    def mostrar_selecao():
        pizza = estado["pizza"]

        if not pizza:
            mostrar_cardapio()
            return

        quantidade_input = ft.TextField(
            label="Quantidade",
            value=str(estado["quantidade"]),
            width=150
        )

        tamanho_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="M", label="M"),
                ft.Radio(value="G", label="G"),
            ]),
            value=estado["tamanho"]
        )

        def avancar_carrinho(e):
            if quantidade_input.value.isdigit() and int(quantidade_input.value) > 0:

                quantidade = int(quantidade_input.value)

                if quantidade > 10:
                    quantidade = 10

                estado["quantidade"] = quantidade
                estado["tamanho"] = tamanho_radio.value

                adicionar_ao_carrinho()
                mostrar_carrinho()

        area.content = ft.Column(
            controls=[
                ft.Text(
                    f"Opções para: {pizza['nome']}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),
                ft.Text("Tamanho da pizza:"),
                tamanho_radio,
                quantidade_input,
                ft.Row([
                    ft.ElevatedButton(
                        "Voltar ao Cardápio",
                        on_click=lambda e: mostrar_cardapio()
                    ),
                    ft.ElevatedButton(
                        "Adicionar ao Carrinho",
                        on_click=avancar_carrinho
                    ),
                    ft.ElevatedButton(
                        "Voltar para Início",
                        on_click=lambda e: mostrar_inicio()
                    )
                ], spacing=10)
            ],
            spacing=15
        )
        area.update()

    def mostrar_carrinho():
        atualizar_carrinho()

        if not carrinho:
            area.content = ft.Column([
                ft.Text(
                    "Seu carrinho está vazio!",
                    size=22,
                    color="#000000"
                ),
                ft.ElevatedButton(
                    "Ir para o Cardápio",
                    on_click=lambda e: mostrar_cardapio()
                )
            ])
        else:
            area.content = ft.Column([
                ft.Text(
                    "Seu Carrinho",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),

                lista_visual,

                subtotal_texto,

                ft.Row([
                    ft.ElevatedButton(
                        "Voltar ao Cardápio",
                        on_click=lambda e: mostrar_cardapio()
                    ),
                    ft.ElevatedButton(
                        "Voltar para Seleção",
                        on_click=lambda e: mostrar_selecao()
                    )
                ], spacing=10)
            ], spacing=15)

        area.update()

    page.add(area)
    mostrar_inicio()

ft.app(target=main)
