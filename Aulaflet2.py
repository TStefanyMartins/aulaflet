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

    estado = {"pizza": None, "tamanho": "M", "quantidade": 1, "recebimento": "retirada"}
    carrinho = []
    area = ft.Container(expand=True)

    nome = ft.TextField(label="Nome", width=350)
    telefone = ft.TextField(label="Telefone", width=350)
    endereco = ft.TextField(label="Rua", width=350, visible=False)

    pagamento = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="dinheiro", label="Dinheiro"),
        ft.Radio(value="pix", label="Pix"),
        ft.Radio(value="cartao", label="Cartão")
    ]), value="dinheiro")

    valor_recebido = ft.TextField(label="Valor recebido", visible=True, width=250)
    troco_texto = ft.Text("Troco: R$ 0,00", color="#000000")
    observacao = ft.TextField(label="Observação", multiline=True, max_length=120, width=350)

    lista_visual = ft.ListView(spacing=8, expand=True)
    subtotal_texto = ft.Text("Subtotal: R$ 0,00", color="#000000")
    taxa_texto = ft.Text("Taxa de entrega: R$ 0,00", color="#000000")
    total_texto = ft.Text("Total: R$ 0,00", size=20, weight=ft.FontWeight.BOLD, color="#000000")

    def avisar(texto): page.show_dialog(ft.SnackBar(ft.Text(texto)))

    def calcular_subtotal():
        return sum(item["preco"] * item["qtd"] for item in carrinho)

    def calcular_total():
        return calcular_subtotal() + (6.00 if estado["recebimento"] == "entrega" else 0.00)

    def atualizar_troco():
        if pagamento.value != "dinheiro": troco_texto.value = "Troco: R$ 0,00"; return
        if not valor_recebido.value.strip(): troco_texto.value = "Troco: R$ 0,00"; return
        try:
            recebido = float(valor_recebido.value.replace(",", "."))
            total = calcular_total()
            troco_texto.value = f"Troco: R$ {recebido - total:.2f}" if recebido >= total else "Troco: valor insuficiente"
        except ValueError: troco_texto.value = "Troco: valor inválido"

    def atualizar_total():
        subtotal = calcular_subtotal()
        taxa = 6.00 if estado["recebimento"] == "entrega" else 0.00
        subtotal_texto.value = f"Subtotal: R$ {subtotal:.2f}"
        taxa_texto.value = f"Taxa de entrega: R$ {taxa:.2f}"
        total_texto.value = f"Total: R$ {subtotal + taxa:.2f}"
        atualizar_troco()
        page.update()

    def validar():
        nome.error_text = None if nome.value.strip() else "Informe o nome"
        digitos = "".join(c for c in telefone.value if c.isdigit())
        telefone.error_text = None if len(digitos) in (10, 11) else "Use DDD + número"
        endereco.error_text = None if estado["recebimento"] != "entrega" or endereco.value.strip() else "Informe o endereço"
        pagamento_valido = True

        if pagamento.value == "dinheiro":
            if not valor_recebido.value.strip():
                valor_recebido.error_text = "Informe o valor recebido"
                pagamento_valido = False
            else:
                try:
                    recebido = float(valor_recebido.value.replace(",", "."))
                    total = calcular_total()
                    valor_recebido.error_text = None if recebido >= total else f"O valor deve ser maior ou igual a R$ {total:.2f}"
                    pagamento_valido = recebido >= total
                except ValueError:
                    valor_recebido.error_text = "Informe um valor válido"
                    pagamento_valido = False
        else:
            valor_recebido.error_text = None

        page.update()
        return nome.error_text is None and telefone.error_text is None and endereco.error_text is None and pagamento_valido

    def recebimento_mudou(e):
        estado["recebimento"] = e.control.value
        endereco.visible = e.control.value == "entrega"
        atualizar_total()

    def pagamento_mudou(e):
        valor_recebido.visible = pagamento.value == "dinheiro"
        if pagamento.value != "dinheiro": valor_recebido.error_text = None; troco_texto.value = "Troco: R$ 0,00"
        page.update()

    pagamento.on_change = pagamento_mudou
    valor_recebido.on_change = lambda e: (atualizar_troco(), page.update())

    def mostrar_inicio():
        area.content = ft.Column([
            ft.Text("PizzaDev", size=32, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Text("Bem-vindo ao PizzaDev", size=20, color="#000000"),
            ft.ElevatedButton("Abrir Cardápio", on_click=lambda e: mostrar_cardapio())
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
        area.update()

    def mostrar_cardapio():
        cards = []
        for pizza in PIZZAS:
            cards.append(ft.Container(
                padding=15, border_radius=12, bgcolor="#FFFFFF",
                on_click=lambda e, p=pizza: selecionar_pizza(p),
                content=ft.Column([
                    ft.Text(pizza["nome"], size=20, weight=ft.FontWeight.BOLD, color="#000000"),
                    ft.Text(pizza["ingredientes"], color="#000000"),
                    ft.Row([
                        ft.Text(f"M: R$ {pizza['m']:.2f}", color="#000000"),
                        ft.Text(f"G: R$ {pizza['g']:.2f}", color="#000000")
                    ])
                ])
            ))

        area.content = ft.Column([
            ft.Text("Nosso Cardápio", size=26, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Row(controls=cards, wrap=True, spacing=15, run_spacing=15),
            ft.ElevatedButton("Voltar para Início", on_click=lambda e: mostrar_inicio())
        ], spacing=15, scroll=ft.ScrollMode.AUTO)
        area.update()

    def selecionar_pizza(pizza):
        estado["pizza"] = pizza
        mostrar_selecao()

    def mostrar_selecao():
        pizza = estado["pizza"]
        if pizza is None: mostrar_cardapio(); return

        quantidade_input = ft.TextField(label="Quantidade", value=str(estado["quantidade"]), width=150)
        tamanho_radio = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="M", label="M"),
            ft.Radio(value="G", label="G")
        ]), value=estado["tamanho"])

        def adicionar_carrinho(e):
            if not quantidade_input.value:
                quantidade_input.error_text = "Informe a quantidade"; page.update(); return

            if not quantidade_input.value.isdigit():
                quantidade_input.error_text = "Informe uma quantidade válida"; page.update(); return

            quantidade = int(quantidade_input.value)

            if quantidade <= 0:
                quantidade_input.error_text = "A quantidade deve ser maior que zero"; page.update(); return

            item_existente = next((item for item in carrinho if item["nome"] == pizza["nome"] and item["tamanho"] == tamanho_radio.value), None)

            if quantidade + (item_existente["qtd"] if item_existente else 0) > 10:
                quantidade_input.error_text = "O máximo permitido por sabor e tamanho é 10."; page.update(); return

            quantidade_input.error_text = None
            estado["quantidade"] = quantidade
            estado["tamanho"] = tamanho_radio.value
            preco = pizza["m"] if tamanho_radio.value == "M" else pizza["g"]

            if item_existente: item_existente["qtd"] += quantidade
            else: carrinho.append({"nome": pizza["nome"], "tamanho": tamanho_radio.value, "preco": preco, "qtd": quantidade})

            atualizar_carrinho()
            mostrar_carrinho()
            avisar(f"{quantidade}x {pizza['nome']} ({tamanho_radio.value}) adicionada ao carrinho!")

        area.content = ft.Column([
            ft.Text(f"Opções para: {pizza['nome']}", size=24, weight=ft.FontWeight.BOLD, color="#000000"),
            ft.Text("Tamanho da pizza:", color="#000000"),
            tamanho_radio,
            quantidade_input,
            ft.Row([
                ft.ElevatedButton("Voltar ao Cardápio", on_click=lambda e: mostrar_cardapio()),
                ft.ElevatedButton("Adicionar ao Carrinho", on_click=adicionar_carrinho)
            ], spacing=10)
        ], spacing=15)
        area.update()

    def atualizar_carrinho():
        lista_visual.controls.clear()

        for item in carrinho:
            parcial = item["preco"] * item["qtd"]
            lista_visual.controls.append(ft.Row([
                ft.Text(f'{item["nome"]} ({item["tamanho"]}) x{item["qtd"]} - R$ {parcial:.2f}'),
                ft.IconButton(icon=ft.icons.DELETE_OUTLINED, tooltip="Remover item", on_click=lambda e, i=item: limpar_carrinho(e, i)),
                ft.IconButton(icon=ft.icons.REMOVE, tooltip="Diminuir quantidade", on_click=lambda e, i=item: remover_uma_unidade(e, i)),
                ft.IconButton(icon=ft.icons.ADD, tooltip="Aumentar quantidade", on_click=lambda e, i=item: adicionar_ao_carrinho(e, i))
            ]))

        if not carrinho: lista_visual.controls.append(ft.Text("Seu carrinho está vazio!"))
        atualizar_total()

    def adicionar_ao_carrinho(e, item):
        if item["qtd"] < 10:
            item["qtd"] += 1
            atualizar_carrinho()
            page.update()
            avisar(f'1 unidade de {item["nome"]} adicionada ao carrinho.')
        else: avisar("O máximo permitido por sabor e tamanho é 10.")

    def remover_uma_unidade(e, item):
        if item["qtd"] > 1:
            item["qtd"] -= 1
        else:
            carrinho.remove(item)
        atualizar_carrinho()
        page.update()

    def confirmar_limpeza(e):
        dialogo = ft.AlertDialog(
            title=ft.Text("Limpar carrinho?"),
            content=ft.Text("Todos os itens serão removidos."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("Confirmar", on_click=limpar_carrinho)
            ]
        )
        page.show_dialog(dialogo)

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

    def finalizar_pedido(e):
        if not carrinho:
            avisar("Seu carrinho está vazio."); return

        if not validar(): return

        total = calcular_total()

        if pagamento.value == "dinheiro":
            recebido = float(valor_recebido.value.replace(",", "."))
            pagamento_info = f"Pagamento: Dinheiro\nValor recebido: R$ {recebido:.2f}\nTroco: R$ {recebido - total:.2f}"
        elif pagamento.value == "pix":
            pagamento_info = "Pagamento: Pix"
        else:
            pagamento_info = "Pagamento: Cartão"

        mensagem = f"Pedido realizado com sucesso!\n\nCliente: {nome.value}\n{pagamento_info}\nTotal: R$ {total:.2f}"

        if estado["recebimento"] == "entrega": mensagem += f"\nEndereço: {endereco.value}"
        if observacao.value.strip(): mensagem += f"\nObservação: {observacao.value.strip()}"

        avisar(mensagem)

    def mostrar_carrinho():
        recebimento = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="retirada", label="Retirada no local"),
                ft.Radio(value="entrega", label="Entrega")
            ]),
            value=estado["recebimento"],
            on_change=recebimento_mudou
        )

        area.content = ft.Column([
            ft.Text("Seu Carrinho", size=26, weight=ft.FontWeight.BOLD, color="#000000"),
            lista_visual,
            ft.Divider(),
            ft.Text("Dados do cliente", size=20, weight=ft.FontWeight.BOLD, color="#000000"),
            nome,
            telefone,
            ft.Text("Como deseja receber?", color="#000000"),
            recebimento,
            endereco,
            ft.Divider(),
            ft.Text("Forma de pagamento", size=20, weight=ft.FontWeight.BOLD, color="#000000"),
            pagamento,
            valor_recebido,
            troco_texto,
            observacao,
            ft.Text("A observação é opcional e pode ter até 120 caracteres.", size=12, color="#666666"),
            ft.Divider(),
            subtotal_texto,
            taxa_texto,
            total_texto,
            ft.Row([
                ft.ElevatedButton("Atualizar Carrinho", on_click=lambda e: atualizar_carrinho()),
                ft.ElevatedButton("Voltar para Seleção", on_click=lambda e: mostrar_selecao()),
                ft.ElevatedButton("Voltar ao Cardápio", on_click=lambda e: mostrar_cardapio()),
                ft.ElevatedButton("Limpar Carrinho", on_click=confirmar_limpeza),
                ft.ElevatedButton("Finalizar Pedido", on_click=finalizar_pedido)
            ], spacing=10)
        ], spacing=15, scroll=ft.ScrollMode.AUTO)

        atualizar_carrinho()
        area.update()

    page.add(area)
    mostrar_inicio()


ft.app(target=main)
