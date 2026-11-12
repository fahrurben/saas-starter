from rest_framework import mixins, status
from rest_framework.response import Response


class CustomLoggerMixin:
    logger = None
    view_name = None

    def get_logger(self):
        return self.logger


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        logger = self.get_logger()
        logger.Info(f"-- START {self.view_name}.create, user: {request.user.id} --")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
        logger.Info(f"-- END {self.view_name}.create --")
        return response
