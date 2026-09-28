import flet as ft


PIZZAS = [
    {
        "id": "P01",
        "nome": "Marguerita",
        "m": 22,
        "g": 35,
        "ingredientes": "Molho, queijo e manjericão"
    },
    {
        "id": "P02",
        "nome": "Portuguesa",
        "m": 35,
        "g": 45,
        "ingredientes": "Presunto, queijo, ovo, cebola e azeitona"
    },
    {
        "id": "P03",
        "nome": "Frango",
        "m": 32,
        "g": 42,
        "ingredientes": "Frango, queijo e catupiry"
    },
    {
        "id": "P04",
        "nome": "Muçarela",
        "m": 30,
        "g": 40,
        "ingredientes": "Molho e muçarela"
    },
    {
        "id": "P05",
        "nome": "Calabresa",
        "m": 32,
        "g": 42,
        "ingredientes": "Calabresa, cebola e queijo"
    },
]


def main(page: ft.Page):

    page.title = "PizzaDev"
    page.padding = 20
    page.bgcolor = "#F5F5F5"

    # -------------------------
    # ESTADO DA APLICAÇÃO
    # -------------------------

    estado = {
        "pizza": None,
        "tamanho": "M",
        "quantidade": 1,
        "carrinho": []
    }

    area = ft.Container(expand=True)

    # -------------------------
    # INÍCIO
    # -------------------------

    def mostrar_inicio():

        pizza_escolhida = (
            f"Pizza escolhida: {estado['pizza']['nome']}"
            if estado["pizza"]
            else "Nenhuma pizza escolhida"
        )

        area.content = ft.Column(
            controls=[
                ft.Text(
                    "PizzaDev",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_900
                ),

                ft.Text(
                    "Bem-vindo ao PizzaDev",
                    size=22
                ),

                ft.Text(
                    "Dupla responsável: Stefany e João",
                    size=12
                ),

                ft.Text(
                    pizza_escolhida,
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),

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

    # -------------------------
    # CARDÁPIO
    # -------------------------

    def mostrar_cardapio():

        cards = []

        for pizza in PIZZAS:

            selecionada = (
                estado["pizza"] is not None
                and estado["pizza"]["id"] == pizza["id"]
            )

            cards.append(
                ft.Container(
                    width=250,
                    padding=15,
                    border_radius=12,

                    bgcolor=(
                        "#D7E8FF"
                        if selecionada
                        else "#FFFFFF"
                    ),

                    border=ft.border.all(
                        2,
                        ft.colors.BLUE
                    ) if selecionada else None,

                    on_click=lambda e, p=pizza: selecionar_pizza(p),

                    content=ft.Column(
                        controls=[
                            ft.Text(
                                pizza["nome"],
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                pizza["ingredientes"]
                            ),

                            ft.Text(
                                f"M: R$ {pizza['m']:.2f}"
                            ),

                            ft.Text(
                                f"G: R$ {pizza['g']:.2f}"
                            ),

                            ft.Text(
                                "Selecionada"
                                if selecionada
                                else "Clique para selecionar",
                                color=ft.colors.BLUE_900,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        spacing=6
                    )
                )
            )

        area.content = ft.Column(
            controls=[
                ft.Text(
                    "Nosso Cardápio",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    "Escolha uma pizza:"
                ),

                ft.Row(
                    controls=cards,
                    wrap=True,
                    spacing=15,
                    run_spacing=15
                ),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Voltar para Início",
                            on_click=lambda e: mostrar_inicio()
                        ),

                        ft.ElevatedButton(
                            "Ir para Seleção",
                            on_click=lambda e: mostrar_selecao()
                        )
                    ]
                )
            ],

            spacing=15,
            scroll=ft.ScrollMode.AUTO
        )

        area.update()

    # -------------------------
    # SELECIONAR PIZZA
    # -------------------------

    def selecionar_pizza(pizza):

        estado["pizza"] = pizza

        mostrar_selecao()

    # -------------------------
    # SELEÇÃO
    # -------------------------

    def mostrar_selecao():

        if estado["pizza"] is None:

            area.content = ft.Column(
                controls=[
                    ft.Text(
                        "Nenhuma pizza selecionada.",
                        size=20
                    ),

                    ft.ElevatedButton(
                        "Voltar para Cardápio",
                        on_click=lambda e: mostrar_cardapio()
                    )
                ]
            )

            area.update()
            return

        pizza = estado["pizza"]

        tamanho = ft.RadioGroup(
            value=estado["tamanho"],

            content=ft.Row(
                controls=[
                    ft.Radio(
                        value="M",
                        label=f"M - R$ {pizza['m']:.2f}"
                    ),

                    ft.Radio(
                        value="G",
                        label=f"G - R$ {pizza['g']:.2f}"
                    )
                ]
            )
        )

        quantidade = ft.TextField(
            label="Quantidade",
            value=str(estado["quantidade"]),
            width=150
        )

        mensagem = ft.Text()

        def continuar(e):

            if tamanho.value is None:
                mensagem.value = "Selecione o tamanho."
                mensagem.color = ft.colors.RED
                mensagem.update()
                return

            if not quantidade.value.isdigit():
                mensagem.value = "Digite uma quantidade válida."
                mensagem.color = ft.colors.RED
                mensagem.update()
                return

            qtd = int(quantidade.value)

            if qtd < 1 or qtd > 10:
                mensagem.value = "A quantidade deve estar entre 1 e 10."
                mensagem.color = ft.colors.RED
                mensagem.update()
                return

            estado["tamanho"] = tamanho.value
            estado["quantidade"] = qtd

            adicionar_ao_carrinho()

        area.content = ft.Column(
            controls=[
                ft.Text(
                    "Seleção",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    pizza["nome"],
                    size=24,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    pizza["ingredientes"]
                ),

                ft.Divider(),

                ft.Text(
                    "Escolha o tamanho:"
                ),

                tamanho,

                quantidade,

                mensagem,

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Voltar para Cardápio",
                            on_click=lambda e: mostrar_cardapio()
                        ),

                        ft.ElevatedButton(
                            "Adicionar ao Carrinho",
                            on_click=continuar
                        )
                    ]
                )
            ],

            spacing=15
        )

        area.update()

    # -------------------------
    # ADICIONAR AO CARRINHO
    # -------------------------

    def adicionar_ao_carrinho():

        pizza = estado["pizza"]

        if estado["tamanho"] == "M":
            preco = pizza["m"]
        else:
            preco = pizza["g"]

        item = {
            "pizza": pizza,
            "tamanho": estado["tamanho"],
            "quantidade": estado["quantidade"],
            "preco": preco
        }

        # Carrinho começa vazio.
        # Depois da confirmação, recebe o item.
        estado["carrinho"] = [item]

        mostrar_carrinho()

    # -------------------------
    # CARRINHO
    # -------------------------

    def mostrar_carrinho():

        if len(estado["carrinho"]) == 0:

            area.content = ft.Column(
                controls=[
                    ft.Text(
                        "Carrinho",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        "Carrinho vazio."
                    ),

                    ft.ElevatedButton(
                        "Voltar para Cardápio",
                        on_click=lambda e: mostrar_cardapio()
                    )
                ],

                spacing=15
            )

            area.update()
            return

        item = estado["carrinho"][0]

        pizza = item["pizza"]
        quantidade = item["quantidade"]
        tamanho = item["tamanho"]
        preco = item["preco"]

        total = quantidade * preco

        area.content = ft.Column(
            controls=[
                ft.Text(
                    "Carrinho",
                    size=28,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Container(
                    padding=15,
                    bgcolor="#FFFFFF",
                    border_radius=12,

                    content=ft.Column(
                        controls=[
                            ft.Text(
                                pizza["nome"],
                                size=22,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Text(
                                pizza["ingredientes"]
                            ),

                            ft.Text(
                                f"Tamanho: {tamanho}"
                            ),

                            ft.Text(
                                f"Quantidade: {quantidade}"
                            ),

                            ft.Text(
                                f"Preço unitário: R$ {preco:.2f}"
                            ),

                            ft.Text(
                                f"Total: R$ {total:.2f}",
                                size=20,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        spacing=8
                    )
                ),

                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Voltar para Seleção",
                            on_click=lambda e: mostrar_selecao()
                        ),

                        ft.ElevatedButton(
                            "Voltar para Início",
                            on_click=lambda e: mostrar_inicio()
                        )
                    ]
                )
            ],

            spacing=15
        )

        area.update()

    # -------------------------
    # INICIA A APLICAÇÃO
    # -------------------------

    page.add(
        ft.Text(
            "PizzaDev",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_900,
            text_align=ft.TextAlign.CENTER
        ),

        area
    )

    mostrar_inicio()


ft.app(target=main)
