import graphene
from graphene_django import DjangoObjectType
import django_filters

from django.db import models

from .models import UserProfile, Tag, Category, ThesisPaper, ResearchPaper, Assignment


class UserProfileFilterSet(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = '__all__'
        filter_overrides = {
            models.ImageField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                },
            },
        }


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filterset_class = UserProfileFilterSet


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = "__all__"


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"


class ThesisPaperType(DjangoObjectType):
    class Meta:
        model = ThesisPaper
        fields = "__all__"


class ResearchPaperType(DjangoObjectType):
    class Meta:
        model = ResearchPaper
        fields = "__all__"


class AssignmentType(DjangoObjectType):
    class Meta:
        model = Assignment
        fields = "__all__"


class Query(graphene.ObjectType):
    all_user_profiles = graphene.List(UserProfileType)
    all_tags = graphene.List(TagType)
    all_categories = graphene.List(CategoryType)
    all_thesis_papers = graphene.List(ThesisPaperType)
    all_research_papers = graphene.List(ResearchPaperType)
    all_assignments = graphene.List(AssignmentType)

    def resolve_all_user_profiles(self, info):
        return UserProfile.objects.all()

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_thesis_papers(self, info):
        return ThesisPaper.objects.all()

    def resolve_all_research_papers(self, info):
        return ResearchPaper.objects.all()

    def resolve_all_assignments(self, info):
        return Assignment.objects.all()


schema = graphene.Schema(query=Query)
