from factory import Faker
from factory.django import DjangoModelFactory
from faker import Faker as Fake
from dj_promocodes.promocodes.models import Promocode, Transaction

fake = Fake()


class PromocodeFactory(DjangoModelFactory):
    class Meta:
        model = Promocode

    title = Faker("name")
    description = Faker("sentence")
    quantity = fake.pyint(min_value=0, max_value=9999, step=1)
    code = Faker("name")
    start_date = Faker("date")
    end_date = Faker("date")
    frequency_of_use = fake.pyint(min_value=0, max_value=9999, step=1)


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction
