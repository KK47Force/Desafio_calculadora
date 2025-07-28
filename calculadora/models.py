from django.db import models
from django.contrib.auth import get_user_model # Importa o modelo de usuário ativo do Django

# Obtém o modelo de usuário ativo. Isso garante que o ForeignKey aponte para o User correto.
User = get_user_model()

class Operacao(models.Model):
    IDUsuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operacoes')
    Parametros = models.CharField(max_length=255, null=False, blank=False)
    Resultado = models.CharField(max_length=255, null=False, blank=False)
    DtInclusao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Operacao'
        ordering = ['-DtInclusao']
        verbose_name = 'Operação'
        verbose_name_plural = 'Operações'

    def __str__(self):
        return f"Usuário: {self.IDUsuario.username} | Operação: {self.Parametros} = {self.Resultado} | Em: {self.DtInclusao.strftime('%d/%m/%Y %H:%M')}"