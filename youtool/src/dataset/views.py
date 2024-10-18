import time

from django.apps import apps
from django.db.models import Q
from django.shortcuts import render

from dataset.models import *


def busca(request):
    model = request.GET.get("model") or "Empresa1"
    uf = request.GET.get("uf") or ""
    termo = request.GET.get("termo") or ""

    resultados = []
    total_time = None
    if uf or termo:
        Model = apps.get_model("dataset", model)
        start = time.time()
        resultados = Model.objects.filter(codigo_situacao_cadastral=2)
        if uf:
            resultados = resultados.filter(uf=uf)
        if termo:
            if model == "Empresa4":
                resultados = resultados.search(termo)
            else:
                resultados = resultados.filter(Q(razao_social__icontains=termo) | Q(nome_fantasia__icontains=termo))
        resultados = list(resultados[:1_000])
        end = time.time()
        total_time = f"{end - start:.3f}"

    return render(
        request,
        "busca.html",
        {
            "uf": uf,
            "termo": termo,
            "total_time": total_time,
            "resultados": resultados,
            "ufs": ['AP', 'AC', 'AM', 'RO', 'RR', 'TO', 'PA'],
            "models": [f"Empresa{x}" for x in range(1, 5)],
            "model": model,
        },
    )
