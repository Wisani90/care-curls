from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_noop
# from django.utils.decorators import classmethod
from profiles.models import UserProfile


# Create your models here.

class Tag(models.Model):
    word        = models.CharField(max_length=35)
    slug        = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.word

    def __str__(self):
        return self.word



class Product(models.Model):
    title = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True,)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True,)
    active = models.BooleanField(_("Active"), default=True,
        help_text=_("Is this product publicly visible."),
    )

    isbn = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    image = models.FileField(
        upload_to='fileuploads\%Y\%m\%d',
        null=True,
        blank=True,
    )

    RATING_CHOICE = (
        ('1', ugettext_noop('Worst')),
        ('2', ugettext_noop('Bed')),
        ('3', ugettext_noop('Average')),
        ('4', ugettext_noop('Good')),
        ('5', ugettext_noop('Best')),
    )
    ratings = models.CharField(
        blank=True, null=True, max_length=1, db_index=True, choices=RATING_CHOICE
    )
    tags = models.ManyToManyField(Tag,related_name='product', blank=False, null=False)

    def __str__(self):
        return self.title


class Cart(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit_price'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

# product = property(get_product, set_product)

# hair profiles
class HairType(models.Model):
    name = models.CharField(max_length=128, blank=True)
    texture = models.CharField(max_length=128, blank=True)
    porosity = models.CharField(max_length=128, blank=True)
    tenacity = models.CharField(max_length=128, blank=True)
    density = models.CharField(max_length=128, blank=True)
    elasticity = models.CharField(max_length=128, blank=True)

    def score(self):
        txtr = self.texture
        prst = self.porosity
        tnct = self.tenacity
        dnst = self.density
        elasticity = self.elasticity
        # consider weightings
        return (txtr + prst + tnct + dnst + elasticity) / 5


class HairProfile(models.Model):
    hair_type = models.ForeignKey(HairType, verbose_name=_('hair type'), on_delete=models.CASCADE)
    length = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('hair length'))
    colour = models.CharField(max_length=128, blank=True)
    greasy = models.BooleanField(default=False)

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    comment = models.TextField()

    def __str__(self):
        return "{user} - {hair}".format(user=self.owner.username, hair=self.hair_type.name)

    @classmethod
    def get_hair_profile(owner=None):
        hair_profile = None
        if owner:
            hair_profile = HairProfile.objects.get(owner=user) 
        return hair_profile