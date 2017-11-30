from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_extensions import mixins as mixinsx


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixinsx.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
