from pyexpat import model
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField()



class Item(models.Model):
    LABELS = (
        ('BestSeller', 'BestSeller'),
        ('New', 'New'),
        ('Spicy🔥', 'Spicy🔥'),
    )   

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info')
    )

    CATEGORY_LABELS = (
        ('Dessert', 'پیش غذا'),
        ('Main Meal', 'غذای اصلی'),
        ('Drink', 'نوشیدنی'),
    )   

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250,blank=True)
    price = models.FloatField()
    pieces = models.IntegerField(default=6)
    instructions = models.CharField(max_length=250,default="Jain Option Available")
    image = models.ImageField(default='default.png', upload_to="Foods/")
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="sushi_name")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, choices=CATEGORY_LABELS, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:dishes", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })


    def get_image(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" alt="{self.title}" width="100" height="100">')
        else:
            return mark_safe(f'<img src="/media/post-images/no-image-6663.svg" alt="NO IMAGE" width="100" height="100">')
    
    get_image.short_description = "image"

    

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review

class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'سفارش فعال'),
        ('Delivered', 'تحویل داده شد')
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.item.title
    
    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'pk' : self.pk
        })

    def update_status_url(self):
        return reverse("main:update_status", kwargs={
            'pk' : self.pk
        })
    


