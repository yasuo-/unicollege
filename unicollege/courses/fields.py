from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model


class OrderField(models.PositiveIntegerField):
    """This is your custom OrderField.
    It inherits from the PositiveIntegerField field provided by Django.
    Your OrderField field takes an optional for_fields parameter that allows you to indicate the fields
    that the order has to be calculated with respect to.
    """
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: Model, add: bool):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                qs = self.model.objects.all()

                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)

                # get the order if the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1

            except ObjectDoesNotExist:
                value = 0

            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
