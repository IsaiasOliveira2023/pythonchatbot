from django.contrib import admin
from .models import Categoria, Produto, Cliente, Endereco, Pedido, ItemPedido

# 1. Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)

# 2. Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Mostra o nome, preço, categoria e estoque na lista
    list_display = ('nome', 'preco', 'categoria', 'estoque')
    # Permite filtrar por Categoria
    list_filter = ('categoria',)
    # Permite buscar por nome do produto
    search_fields = ('nome',)

# 3. Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Mostra nome, email e CPF na lista
    list_display = ('nome', 'email', 'cpf')
    # Permite buscar por esses campos
    search_fields = ('nome', 'email', 'cpf')

# 4. Endereco
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    # Mostra o cliente, cidade e estado
    list_display = ('cliente', 'cidade', 'estado')
    # O 'cliente__nome' permite buscar pelo nome do cliente (relacionamento ForeignKey)
    search_fields = ('cliente__nome', 'cidade')

# 5. Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Mostra dados essenciais do pedido
    list_display = ('id', 'cliente', 'status', 'total', 'criado_em')
    # Permite filtrar por status e data de criação
    list_filter = ('status', 'criado_em')
    # Permite buscar pelo nome ou email do cliente
    search_fields = ('cliente__nome', 'cliente__email')

# 6. ItemPedido
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    # Mostra pedido, produto, quantidade e preço total
    list_display = ('pedido', 'produto', 'quantidade', 'preco_total')
    # Permite buscar pelo ID do pedido ou nome do produto
    search_fields = ('pedido__id', 'produto__nome')