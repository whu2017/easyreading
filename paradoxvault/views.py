# coding: utf-8
from rest_framework import status, generics, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import *


class SelectionView(viewsets.ModelViewSet):

    def get(self, request, questionbank_id, *args, **kwargs):
        try:
            questionbank = QuestionBank.objects.get(pk=questionbank_id)
            try:
                selection = Selection.objects.get(fk=questionbank)
                options = SelectionOptions.objects.get_queryset(fk=selection.pk)
            except ObjectDoesNotExist as e:
                raise NotFound()
        except ObjectDoesNotExist as e:
            raise NotFound()

        return Response({
            {
                "id": selection.pk,
                "question_type": selection.question_type,
                "score": selection.grade,
                "question": selection.question,
                "selection": options,
                "answer": selection.answer,
                "difficulty": selection.difficulty,
                "picked": '',
                "choose": '',
                "show": 'false',

            },
        })


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class QuestionBankView(generics.ListAPIView):

    permission_classes = ()
    authentication_classes = ()
    queryset = QuestionBank.objects.all()
    serializer_class = QuestionBankListSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', 'author')
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        serializer = QuestionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        subject = serializer.validated_data.get('subjects_name', '')
        subject_obj = None
        if subject:
            category_set = Subject.objects.filter(name=subject)
            if not category_set.exists():
                return Response(data={
                    "message": "科目不存在"
                }, status=status.HTTP_400_BAD_REQUEST)
            subject_obj = category_set[0]

        if subject_obj is not None:
            self.queryset = self.queryset.filter(subject=subject_obj)
        queryset = self.filter_queryset(self.queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuestionBankItemView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, questiobank_id, *args, **kwargs):
        try:
            questiobank = QuestionBank.objects.get(pk=questiobank_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        serializer = QuestionBankItemSerializer(questiobank)
        return Response(serializer.data)


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class QuestionCommentListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, questionbank_id, *args, **kwargs):
        try:
            questionbank = QuestionBank.objects.get(pk=questionbank_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        paginator = CommentPagination()
        queryset = QuestionComment.objects.filter(questionbank=questionbank, parent=None)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentDisplaySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, questionbank_id, *args, **kwargs):
        serializer = CommentPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        try:
            questionbank = QuestionBank.objects.get(pk=questionbank_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        score = serializer.validated_data['score']
        content = serializer.validated_data['content']
        parent_id = serializer.validated_data['parent_id']

        if parent_id == 0:
            comment = QuestionComment.objects.create(user=user, questionbank=questionbank, score=score, content=content)
        else:
            comment = QuestionComment.objects.create(user=user, questionbank=questionbank, score=score, content=content, parent_id=parent_id)
        return Response(CommentDisplaySerializer(comment).data)


class QuestionCommentItemView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = QuestionComment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise NotFound()
        return Response(CommentDisplaySerializer(comment).data)


class QuestionCommentChildrenView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = QuestionComment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise NotFound()

        paginator = CommentPagination()
        queryset = QuestionComment.objects.filter(parent=comment)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentDisplaySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
