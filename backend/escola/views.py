from rest_framework import viewsets, generics
from escola.helper import add_header_location
from escola.serializer import AlunoSerializerV2
from escola.models import Aluno, Curso, Matricula
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from escola.serializer import (
    AlunoSerializer,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasAlunoSerializer,
    ListaAlunosMatriculadosSerializer,
)


class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos e alunas"""

    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if str(self.request.version).upper() == "V2":
            return AlunoSerializerV2
        return AlunoSerializer

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        return add_header_location(serializer, request)


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos"""

    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    http_method_names = ["get", "post", "put", "path"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        return add_header_location(serializer, request)


class MatriculaViewSet(viewsets.ModelViewSet):
    """Listando todas as matrículas"""

    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    http_method_names = ["get", "post", "put", "path"]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        return add_header_location(serializer, request)

    @method_decorator(cache_page(20))
    def dispatch(self, *args, **kwargs):
        return super(MatriculaViewSet, self).dispatch(*args, **kwargs)


class ListaMatriculasAluno(generics.ListAPIView):
    """Listando as matrículas de um aluno ou aluna"""

    def get_queryset(self):
        queryset = Matricula.objects.filter(aluno_id=self.kwargs["pk"])
        return queryset

    serializer_class = ListaMatriculasAlunoSerializer


class ListaAlunosMatriculados(generics.ListAPIView):
    """Listando alunos e alunas matriculados em um curso"""

    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs["pk"])
        return queryset

    serializer_class = ListaAlunosMatriculadosSerializer
