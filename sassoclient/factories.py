import factory
from faker import Factory
from django.contrib.auth import get_user_model

fake = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)
    username = factory.LazyAttribute(lambda a: fake.user_name())


