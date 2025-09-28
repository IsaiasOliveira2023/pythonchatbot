from django.db import models
from django.utils import timezone  # Embora 'timezone' não esteja sendo usado diretamente, é uma boa prática manter.

# ===============================================
# As 6 Classes (Models) do Sistema
# ===============================================

# Classe 1: Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

# -----------------------------------------------

# Classe 3: Cliente (Definida antes de Endereco e Pedido)
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    # Recomenda-se o uso de validators para CPF
    cpf = models.CharField(max_length=14, unique=True) 
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

# -----------------------------------------------

# Classe 2: Produto (Depende de Categoria)
class Produto(models.Model):
    # A classe Produto original que você enviou foi substituída por esta versão mais completa.
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    # Relacionamento: Um produto pertence a uma Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos') 
    estoque = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-criado_em']

# -----------------------------------------------

# Classe 4: Endereco (Depende de Cliente)
class Endereco(models.Model):
    # Relacionamento: Um Cliente tem um (OneToOne) Endereço principal
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='endereco')
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    padrao = models.BooleanField(default=False) # Endereço padrão para entregas

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

# -----------------------------------------------

# Classe 5: Pedido (Depende de Cliente e Endereco)
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    # Usamos PROTECT para evitar a exclusão do endereço se houver um pedido associado
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.PROTECT) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-criado_em']

# -----------------------------------------------

# Classe 6: ItemPedido (Depende de Pedido e Produto)
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    # Usamos PROTECT para evitar a exclusão do produto se houver itens de pedidos associados
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT) 
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_total = models.DecimalField(max_digits=12, decimal_places=2)

    # Sobrescreve o método save para calcular o preço unitário e total automaticamente
    def save(self, *args, **kwargs):
        # Garante que o preco_unitario seja o preço atual do Produto
        self.preco_unitario = self.produto.preco 
        self.preco_total = self.quantidade * self.produto.preco
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"