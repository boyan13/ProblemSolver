# ----------------------------------------------------------------------------------------------------------------------
from functools import cached_property
# ----------------------------------------------------------------------------------------------------------------------


class FormElementMixin:
    _HARVESTABLE = True

    @cached_property
    def harvestable(self):
        """Whether this element contains data."""
        return self._HARVESTABLE

    def harvest(self):
        """Get the value (or values) of this element."""
        raise ValueError("This element does not hold harvestable data.")


class FormMixin:
    def __init__(self, *args, **kwargs):
        self.to_harvest = []
        self.attributes = []
        super().__init__(*args, **kwargs)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}


class FormManagerMixin:

    def __init__(self, *args, **kwargs):
        self.subforms = []
        super().__init__(*args, **kwargs)

    @property
    def to_harvest(self):
        to_harvest = []
        for form in self.subforms.values():
            to_harvest += form.to_harvest
        return to_harvest

    @property
    def attributes(self):
        attributes = []
        for form in self.subforms.values():
            attributes += form.attributes
        return attributes

    def __getattr__(self, item):
        for form in self.subforms:
            if item in form.attributes:
                return getattr(form, item)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}
