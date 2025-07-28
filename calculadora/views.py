from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse  
import json
from .models import Operacao


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'calculadora/calculadora.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_operations = Operacao.objects.filter(
            IDUsuario=self.request.user).order_by('-DtInclusao')[:5]

        history_data = []
        for op in recent_operations:
            history_data.append({
                'parametros': op.Parametros,
                'resultado': op.Resultado,
                'dt_inclusao': op.DtInclusao.strftime('%H:%M')
            })

        context['initial_history'] = json.dumps(
            history_data)  # Passa o histórico como JSON string
        return context


class ProcessOperationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # Recebe os dados JSON do corpo da requisição
            data = json.loads(request.body)
            action = data.get('action', 'calculate')

            if action == 'clear_history':
                # Apaga todas as operações do usuário logado
                Operacao.objects.filter(IDUsuario=request.user).delete()

                return JsonResponse({
                    'success': True,
                    'message': 'Histórico limpo com sucesso',
                    'history': [] 
                })

            expression = data.get('expression')

            if not expression:
                return JsonResponse({'error': 'Nenhuma expressão fornecida.'}, status=400)
            
            expression_eval = expression.replace('×', '*').replace('÷', '/')

            try:
                result = eval(expression_eval)
            except (SyntaxError, ZeroDivisionError, TypeError) as e:
                return JsonResponse({'error': f'Erro na expressão: {e}'}, status=400)


            # Salvar a operação no banco de dados
            Operacao.objects.create(
                IDUsuario=request.user,  
                Parametros=expression,
                Resultado=str(result)  
            )

            recent_operations = Operacao.objects.filter(
                IDUsuario=request.user).order_by('-DtInclusao')[:5]
            history_data = []
            for op in recent_operations:
                history_data.append({
                    'parametros': op.Parametros,
                    'resultado': op.Resultado,
                    'dt_inclusao': op.DtInclusao.strftime('%H:%M')
                })

            return JsonResponse({
                'result': result,
                'history': history_data
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Requisição inválida. JSON mal formatado.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Ocorreu um erro inesperado: {e}'}, status=500)
