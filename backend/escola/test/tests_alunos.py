import shutil
import tempfile

from rest_framework.test import APITestCase
from escola.models import Aluno
from rest_framework import status
from django.core.files.base import File
from io import BytesIO
from PIL import Image
from django.test import override_settings

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class AlunosV1TestCase(APITestCase):
    @staticmethod
    def get_image_file(name="test.png", ext="png", size=(50, 50), color=(256, 0, 0)):
        """Gera uma imagem qualquer para ser usada durantes os testes"""
        file_obj = BytesIO()
        image = Image.new("RGB", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @classmethod
    def tearDownClass(cls):
        # Deleta o diretório temporário das imagens geradas para os testes
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        """Configura os detalhes iniciais para os testes serem executados"""
        self.aluno_1 = Aluno.objects.create(
            nome="Aluno Teste Um",
            rg="123456789",
            cpf="37174164803",
            data_nascimento="1990-01-01",
            foto=self.get_image_file(),
        )
        self.aluno_2 = Aluno.objects.create(
            nome="Aluno Teste Dois",
            rg="987654321",
            cpf="11174617500",
            data_nascimento="1980-02-02",
        )

    def test_requisicao_get_para_obter_todos_alunos(self):
        """Teste para verificar a requisição GET para listar os alunos"""
        response = self.client.get("/alunos/?version=v1")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(2, len(response.data))

    def test_requisicao_post_para_criar_aluno_com_foto(self):
        """Teste para verificar a requisição POST para criar um aluno com foto"""
        data = {
            "nome": "Aluno Teste Três",
            "rg": "987654321",
            "cpf": "52234136440",
            "data_nascimento": "1998-12-02",
            "foto": self.get_image_file(),
        }
        response = self.client.post("/alunos/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_post_para_criar_aluno_sem_foto(self):
        """Teste para verificar a requisição POST para criar um aluno sem foto"""
        data = {
            "nome": "Aluno Teste Quatro",
            "rg": "987654321",
            "cpf": "63469371113",
            "data_nascimento": "1998-12-02",
        }
        response = self.client.post("/alunos/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
