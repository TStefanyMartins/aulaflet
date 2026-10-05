import flet as ft


PIZZAS = [
    {
        "id": "P01",
        "nome": "Muçarela",
        "m": 30,
        "g": 40,
        "ingredientes": "mussarela, tomate e orégano"
    },
    {
        "id": "P02",
        "nome": "Calabresa",
        "m": 32,
        "g": 42,
        "ingredientes": "calabresa, cebola e mussarela"
    },
    {
        "id": "P03",
        "nome": "Frango",
        "m": 32,
        "g": 42,
        "ingredientes": "frango com borda recheada"
    },
    {
        "id": "P04",
        "nome": "Portuguesa",
        "m": 35,
        "g": 45,
        "ingredientes": "presunto, ovos, cebola e azeitona"
    },
]


def main(page: ft.Page):
    page.title = "PizzaDev"
    page.bgcolor = "#F5F5F5"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {
        "pizza": None,
        "tamanho": "M",
        "quantidade": 1,
        "recebimento": "retirada",
    }

    carrinho = []

    area = ft.Container(expand=True)

    nome = ft.TextField(
        label="Nome",
        width=350
    )

    telefone = ft.TextField(
        label="Telefone",
        width=350
    )

    endereco = ft.TextField(
        label="Rua",
        width=350,
        visible=False
    )

    lista_visual = ft.ListView(
        spacing=8,
        expand=True
    )

    subtotal_texto = ft.Text(
        "Subtotal: R$ 0,00",
        color="#000000"
    )

    taxa_texto = ft.Text(
        "Taxa de entrega: R$ 0,00",
        color="#000000"
    )

    total_texto = ft.Text(
        "Total: R$ 0,00",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#000000"
    )

    def avisar(texto):
        page.show_dialog(
            ft.SnackBar(
                ft.Text(texto)
            )
        )

    def validar():
        # Nome
        if nome.value.strip():
            nome.error_text = None
        else:
            nome.error_text = "Informe o nome"

        # Telefone
        digitos = "".join(
            c for c in telefone.value
            if c.isdigit()
        )

        if len(digitos) in (10, 11):
            telefone.error_text = None
        else:
            telefone.error_text = "Use DDD + número"

        # Endereço
        if estado["recebimento"] == "entrega":
            if endereco.value.strip():
                endereco.error_text = None
            else:
                endereco.error_text = "Informe o endereço"
        else:
            endereco.error_text = None

        page.update()

        return (
            nome.error_text is None
            and telefone.error_text is None
            and endereco.error_text is None
        )

    def recebimento_mudou(e):
        estado["recebimento"] = e.control.value

        # Só mostra endereço quando for entrega
        endereco.visible = (
            e.control.value == "entrega"
        )

        atualizar_total()

        page.update()

    def calcular_subtotal():
        subtotal = 0

        for item in carrinho:
            subtotal += item["preco"] * item["qtd"]

        return subtotal

    def atualizar_total():
        subtotal = calcular_subtotal()

        if estado["recebimento"] == "entrega":
            taxa = 5.00
        else:
            taxa = 0.00

        total = subtotal + taxa

        subtotal_texto.value = (
            f"Subtotal: R$ {subtotal:.2f}"
        )

        taxa_texto.value = (
            f"Taxa de entrega: R$ {taxa:.2f}"
        )

        total_texto.value = (
            f"Total: R$ {total:.2f}"
        )

        page.update()

    def mostrar_inicio():
        area.content = ft.Column(
            controls=[
                ft.Text(
                    "PizzaDev",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),

                ft.Text(
                    "Bem-vindo ao PizzaDev",
                    size=20,
                    color="#000000"
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

    def mostrar_cardapio():
        cards = []

        for pizza in PIZZAS:

            card = ft.Container(
                padding=15,
                border_radius=12,
                bgcolor="#FFFFFF",

                on_click=lambda e, p=pizza:
                    selecionar_pizza(p),

                content=ft.Column([
                    ft.Text(
                        pizza["nome"],
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#000000"
                    ),

                    ft.Text(
                        pizza["ingredientes"],
                        color="#000000"
                    ),

                    ft.Row([
                        ft.Text(
                            f"M: R$ {pizza['m']:.2f}",
                            color="#000000"
                        ),

                        ft.Text(
                            f"G: R$ {pizza['g']:.2f}",
                            color="#000000"
                        ),
                    ])
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

        if pizza is None:
            mostrar_cardapio()
            return

        quantidade_input = ft.TextField(
            label="Quantidade",
            value=str(estado["quantidade"]),
            width=150
        )

        tamanho_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(
                    value="M",
                    label="M"
                ),

                ft.Radio(
                    value="G",
                    label="G"
                ),
            ]),

            value=estado["tamanho"]
        )

        def adicionar_carrinho(e):

            if not quantidade_input.value:
                quantidade_input.error_text = (
                    "Informe a quantidade"
                )

                page.update()
                return

            if not quantidade_input.value.isdigit():
                quantidade_input.error_text = (
                    "Informe uma quantidade válida"
                )

                page.update()
                return

            quantidade = int(
                quantidade_input.value
            )

            if quantidade <= 0:
                quantidade_input.error_text = (
                    "A quantidade deve ser maior que zero"
                )

                page.update()
                return
            
            item_existente = None

            for item in carrinho:

                if (
                    item["nome"] == pizza["nome"]
                    and
                    item["tamanho"] == tamanho_radio.value
                ):
                    item_existente = item
                    break

            quantidade_total = quantidade

            if item_existente:
                quantidade_total += item_existente["qtd"]

            if quantidade_total > 10:

                quantidade_input.error_text = (
                    "O máximo permitido por sabor "
                    "e tamanho é 10."
                )

                page.update()
                return

            quantidade_input.error_text = None

            estado["quantidade"] = quantidade

            estado["tamanho"] = (
                tamanho_radio.value
            )

            if tamanho_radio.value == "M":
                preco = pizza["m"]
            else:
                preco = pizza["g"]

            if item_existente:

                item_existente["qtd"] += quantidade

            else:

                carrinho.append({
                    "nome": pizza["nome"],
                    "tamanho": tamanho_radio.value,
                    "preco": preco,
                    "qtd": quantidade
                })

            atualizar_carrinho()

            mostrar_carrinho()

            avisar(
                f"{quantidade}x {pizza['nome']} "
                f"({tamanho_radio.value}) "
                "adicionada ao carrinho!"
            )

        area.content = ft.Column(
            controls=[

                ft.Text(
                    f"Opções para: {pizza['nome']}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),

                ft.Text(
                    "Tamanho da pizza:",
                    color="#000000"
                ),

                tamanho_radio,

                quantidade_input,

                ft.Row([
                    ft.ElevatedButton(
                        "Voltar ao Cardápio",
                        on_click=lambda e:
                            mostrar_cardapio()
                    ),

                    ft.ElevatedButton(
                        "Adicionar ao Carrinho",
                        on_click=adicionar_carrinho
                    )
                ], spacing=10)
            ],

            spacing=15
        )

        area.update()

    def atualizar_carrinho():

        lista_visual.controls.clear()

        subtotal = 0

        for item in carrinho:

            parcial = (
                item["preco"] *
                item["qtd"]
            )

            subtotal += parcial

            lista_visual.controls.append(
                ft.Row(
                    controls=[

                        ft.Text(
                            f'{item["nome"]} '
                            f'({item["tamanho"]}) '
                            f'x{item["qtd"]} '
                            f'- R$ {parcial:.2f}'
                        ),

                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINED,
                            on_click=lambda e, i=item:
                                limpar_carrinho(e, i)
                        ),

                        ft.IconButton(
                            icon=ft.icons.REMOVE,
                            on_click=lambda e, i=item:
                                remover_uma_unidade(e, i)
                        ),

                        ft.IconButton(
                            icon=ft.icons.ADD,
                            on_click=lambda e, i=item:
                                adicionar_ao_carrinho(e, i)
                        )
                    ]
                )
            )

        if not carrinho:

            lista_visual.controls.append(
                ft.Text(
                    "Seu carrinho está vazio!"
                )
            )

        subtotal_texto.value = (
            f"Subtotal: R$ {subtotal:.2f}"
        )

        atualizar_total()

    def adicionar_ao_carrinho(e, item):

        if item["qtd"] < 10:

            item["qtd"] += 1

            atualizar_carrinho()

            page.update()

            avisar(
                f'1 unidade de '
                f'{item["nome"]} '
                'adicionada ao carrinho.'
            )

        else:

            avisar(
                "O máximo permitido por "
                "sabor e tamanho é 10."
            )

    def remover_uma_unidade(e, item):

        if item["qtd"] > 1:
            item["qtd"] -= 1
        else:
            carrinho.remove(item)

        atualizar_carrinho()

        page.update()

    def confirmar_limpeza(e):

        dialogo = ft.AlertDialog(

            title=ft.Text(
                "Limpar carrinho?"
            ),

            content=ft.Text(
                "Todos os itens serão removidos."
            ),

            actions=[

                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e:
                        page.pop_dialog()
                ),

                ft.TextButton(
                    "Confirmar",
                    on_click=limpar_carrinho
                )
            ]
        )

        page.show_dialog(dialogo)

    def limpar_carrinho(e, item=None):

        if item is None:

            carrinho.clear()

            page.pop_dialog()

            mensagem = (
                "Carrinho limpo com sucesso!"
            )

        else:

            carrinho.remove(item)

            mensagem = (
                f'{item["nome"]} '
                "removida do carrinho."
            )

        atualizar_carrinho()

        page.update()

        avisar(mensagem)

    def finalizar_pedido(e):

        if not carrinho:

            avisar(
                "Seu carrinho está vazio."
            )

            return

        # Valida nome, telefone e endereço
        if not validar():
            return

        subtotal = calcular_subtotal()

        if estado["recebimento"] == "entrega":
            taxa = 6.00
        else:
            taxa = 0.00

        total = subtotal + taxa

        mensagem = (
            "Pedido realizado com sucesso!\n"
            f"Cliente: {nome.value}\n"
            f"Total: R$ {total:.2f}"
        )

        if estado["recebimento"] == "entrega":

            mensagem += (
                f"\nEndereço: {endereco.value}"
            )

        avisar(mensagem)

    def mostrar_carrinho():

        recebimento = ft.RadioGroup(

            content=ft.Column([

                ft.Radio(
                    value="retirada",
                    label="Retirada no local"
                ),

                ft.Radio(
                    value="entrega",
                    label="Entrega"
                )
            ]),

            value=estado["recebimento"],

            on_change=recebimento_mudou
        )

        area.content = ft.Column(

            controls=[

                ft.Text(
                    "Seu Carrinho",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),

                lista_visual,

                subtotal_texto,

                ft.Divider(),

                ft.Text(
                    "Dados do cliente",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#000000"
                ),

                nome,

                telefone,

                ft.Text(
                    "Como deseja receber?",
                    color="#000000"
                ),

                recebimento,

                endereco,

                taxa_texto,

                total_texto,

                ft.Row([

                    ft.ElevatedButton(
                        "Atualizar Carrinho",
                        on_click=lambda e:
                            atualizar_carrinho()
                    ),

                    ft.ElevatedButton(
                        "Voltar para Seleção",
                        on_click=lambda e:
                            mostrar_selecao()
                    ),

                    ft.ElevatedButton(
                        "Voltar ao Cardápio",
                        on_click=lambda e:
                            mostrar_cardapio()
                    ),

                    ft.ElevatedButton(
                        "Limpar Carrinho",
                        on_click=confirmar_limpeza
                    ),

                    ft.ElevatedButton(
                        "Finalizar Pedido",
                        on_click=finalizar_pedido
                    )
                ], spacing=10)
            ],

            spacing=15,

            scroll=ft.ScrollMode.AUTO
        )

        atualizar_carrinho()

        area.update()

    page.add(area)

    mostrar_inicio()

ft.app(target=main)
