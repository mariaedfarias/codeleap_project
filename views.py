
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_datetime')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Captura o nome de usuário enviado pela requisição
        serializer.save(username=self.request.data['username'])

class PostUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Permite atualização apenas pelo criador do post
        if serializer.instance.username == self.request.data['username']:
            serializer.save()
        else:
            raise PermissionError("Você não pode editar esse post")

    def perform_destroy(self, instance):
        # Permite exclusão apenas pelo criador do post
        if instance.username == self.request.data['username']:
            instance.delete()
        else:
            raise PermissionError("Você não pode excluir esse post")
