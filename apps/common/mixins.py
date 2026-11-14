from rest_framework import mixins, status
from rest_framework.response import Response


class CustomLoggerMixin:
    logger = None
    view_name = None

    def get_logger(self):
        return self.logger


class CustomListModelMixin(mixins.ListModelMixin):
    pass


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        logger = self.get_logger()
        logger.Info(
            f"-- START {self.view_name}.create, user: {request.user.id} --",
            extra={"data": request.data},
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
        logger.Info(f"-- END {self.view_name}.create --")
        return response


class CustomRetrieveModelMixin(mixins.RetrieveModelMixin):
    pass


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        logger = self.get_logger()

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        logger.Info(
            f"-- START {self.view_name}.update, user: {request.user.id} --",
            extra={"id": instance.id, "data": request.data},
        )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        logger.Info(f"-- END {self.view_name}.update --")
        return Response(serializer.data)


class CustomDestroyModelMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        logger = self.get_logger()

        instance = self.get_object()

        logger.Info(
            f"-- START {self.view_name}.destroy, user: {request.user.id} --",
            extra={"id": instance.id},
        )
        self.perform_destroy(instance)

        logger.Info(f"-- END {self.view_name}.destroy --")
        return Response(status=status.HTTP_204_NO_CONTENT)
