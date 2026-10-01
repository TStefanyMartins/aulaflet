import flet as ft

PIZZAS = [
    {"id": "P01", "nome": "Muçarela", "m": 30, "g": 40, "ingredientes": "mussarela, tomate e orégano"},
    {"id": "P02", "nome": "Calabresa", "m": 32, "g": 42, "ingredientes": "calabresa, cebola e mussarela"},
    {"id": "P03", "nome": "Frango", "m": 32, "g": 42, "ingredientes": "frango com borda recheada"},
    {"id": "P04", "nome": "Portuguesa", "m": 35, "g": 45, "ingredientes": "presunto, ovos, cebola e azeitona"},
]

def main(page: ft.Page):
    page.title = "PizzaDev"
    page.bgcolor = "#F5F5F5"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    estado = {"pizza": None, "tamanho": "M", "quantidade": 1}

    area = ft.Container(expand=True)

    def mostrar_inicio():
        area.content = ft.Column(
            controls=[
                ft.Text("PizzaDev", size=32, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Text("Bem-vindo ao PizzaDev", size=20, color="#000000"),
                ft.ElevatedButton("Abrir Cardápio", on_click=lambda e: mostrar_cardapio())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
        area.update()

    def avisar(texto):
        page.show_dialog(ft.SnackBar(ft.Text(texto)))

    def confirmar_limpeza(e):
        dialogo = ft.AlertDialog(
        title=ft.Text("Limpar carrinho?"),
        content=ft.Text("Todos os itens serão removidos."),
        actions=[
        ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
        ft.TextButton("Confirmar", on_click=limpar_carrinho),
        ],
        )
        page.show_dialog(dialogo)

    def mostrar_cardapio():
        cards = []
        for pizza in PIZZAS:
            card = ft.Container(
                padding=15,
                border_radius=12,
                bgcolor="#FFFFFF",
                on_click=lambda e, p=pizza: selecionar_pizza(p),
                content=ft.Column([
                    ft.Text(pizza["nome"], size=20, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text(pizza["ingredientes"], color="#000000"),
                    ft.Row([
                        ft.Text(f"M: R$ {pizza['m']}", color="#000000"),
                        ft.Text(f"G: R$ {pizza['g']}", color="#000000"),
                    ]),
                ])
            )
            cards.append(card)

        area.content = ft.Column(
            controls=[
                ft.Text("Nosso Cardápio", size=26, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Row(controls=cards, wrap=True, spacing=15, run_spacing=15),
                ft.ElevatedButton("Voltar para Início", on_click=lambda e: mostrar_inicio())
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

        quantidade_input = ft.TextField(label="Quantidade", value=str(estado["quantidade"]), width=150)
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
                item_existente = next(
                    (
                        item for item in carrinho
                        if item["nome"] == pizza["nome"]
                        and item["tamanho"] == tamanho_radio.value
                    ),
                    None,
                )
                quantidade_total = quantidade
                if item_existente:
                    quantidade_total += item_existente["qtd"]

                if quantidade_total > 10:
                    quantidade_input.error_text = (
                        "O máximo permitido por sabor e tamanho é 10."
                    )
                    page.update()
                    return

                quantidade_input.error_text = None
                estado["quantidade"] = quantidade
                estado["tamanho"] = tamanho_radio.value
                preco = pizza["m"] if tamanho_radio.value == "M" else pizza["g"]
                if item_existente:
                    item_existente["qtd"] += quantidade
                else:
                    carrinho.append({
                        "nome": pizza["nome"],
                        "tamanho": tamanho_radio.value,
                        "preco": preco,
                        "qtd": quantidade,
                    })
                mostrar_carrinho()
                atualizar_carrinho()

        area.content = ft.Column(
            controls=[
                ft.Text(f"Opções para: {pizza['nome']}", size=24, weight=ft.FontWeight.BOLD, color="#000000"),
                ft.Text("Tamanho da pizza:"),
                tamanho_radio,
                quantidade_input,
                ft.Row([
                    ft.ElevatedButton("Voltar ao Cardápio", on_click=lambda e: mostrar_cardapio()),
                    ft.ElevatedButton("Ver Carrinho", on_click=avancar_carrinho),
                ], spacing=10)
            ],
            spacing=15
        )
        area.update()

    carrinho = []
    lista_visual = ft.ListView(spacing=8, expand=True)
    subtotal_texto = ft.Text("Subtotal: R$ 0,00")
    
    def atualizar_carrinho():
        lista_visual.controls.clear()
        subtotal = 0
        for item in carrinho:
            parcial = item["preco"] * item["qtd"]
            subtotal += parcial
            lista_visual.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            f'{item["nome"]} ({item["tamanho"]}) x{item["qtd"]} '
                            f"- R$ {parcial:.2f}"
                        ),
                        ft.ElevatedButton(
                            ft.Icon(ft.Icons.DELETE_OUTLINED),
                            on_click=lambda e, i=item: limpar_carrinho(e, i),
                        ),
                        ft.ElevatedButton(
                            ft.Icon(ft.Icons.ADD),
                            on_click=lambda e, i=item: adicionar_ao_carrinho(e, i),
                        )
                    ]
                )
            )

        if not carrinho:
            lista_visual.controls.append(ft.Text("Seu carrinho está vazio!"))

        subtotal_texto.value = f"Subtotal: R$ {subtotal:.2f}"

    def adicionar_ao_carrinho(e, item):
        if item["qtd"] < 10:
            item["qtd"] += 1
            atualizar_carrinho()
            page.update()
            avisar(f'1 unidade de {item["nome"]} adicionada ao carrinho.')
        else:
            avisar("O máximo permitido por sabor e tamanho é 10.")

    def limpar_carrinho(e, item=None):
        if item is None:
            carrinho.clear()
            page.pop_dialog()
            mensagem = "Carrinho limpo com sucesso!"
        else:
            carrinho.remove(item)
            mensagem = f'{item["nome"]} removida do carrinho.'

        atualizar_carrinho()
        page.update()
        avisar(mensagem)


    def mostrar_carrinho():
        area.content = ft.Column([
            ft.Text("Seu Carrinho", size=26, weight=ft.FontWeight.BOLD, color="#000000"),
            lista_visual,
            subtotal_texto,
            ft.Row([
                ft.ElevatedButton("Atualizar Carrinho", on_click=lambda e: atualizar_carrinho()),
                ft.ElevatedButton("Voltar para Seleção", on_click=lambda e: mostrar_selecao()),
                ft.ElevatedButton("Voltar ao Cardápio", on_click=lambda e: mostrar_cardapio()),
                ft.ElevatedButton("Limpar Carrinho", on_click=confirmar_limpeza)
            ], spacing=10)
        ], spacing=15)
        atualizar_carrinho()
        
        area.update()
        
    page.add(area)
    mostrar_inicio()

ft.run(main)