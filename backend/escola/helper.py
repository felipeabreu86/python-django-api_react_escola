from rest_framework import status
from rest_framework.response import Response


def add_header_location(serializer, request):
    """Adiciona o campo 'Location' ao Cabeçalho de Resposta HTTP indicando a localização do recurso criado."""
    if serializer.is_valid():
        serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        id = str(serializer.data["id"])
        response["Location"] = request.build_absolute_uri() + id
        return response
    else:
        print(serializer.errors)
