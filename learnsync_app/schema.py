import graphene
from graphene_django import DjangoObjectType
from .models import UserProfile

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ("id", "full_name", "bio", "profile_image", "social_site_urls")

class Query(graphene.ObjectType):
    user_profile = graphene.Field(UserProfileType)

    def resolve_user_profile(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user.userprofile
        return None

schema = graphene.Schema(query=Query)
