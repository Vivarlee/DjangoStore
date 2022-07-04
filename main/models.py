from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('S', 'shirt'),
    ('SW', 'sport wear'),
    ('OW', 'outwear'),
)


LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Item(models.Model):
    name = models.CharField('Наименование', max_length=50)
    price = models.FloatField('Цена')
    about = models.TextField('описание')
    image = models.ImageField(upload_to="main/images", default="main/images/1379863340_439961967_1.jpg")
    category = models.CharField('Категория', choices= CATEGORY_CHOICES, max_length=2)
    label = models.CharField('Ярлык',choices=LABEL_CHOICES, max_length=1, default="D")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)  # there should only be one order which wasn't 'ordered'

    def __str__(self):
        return "Order of " + self.User.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_cost(self):
        return self.item.price * self.quantity