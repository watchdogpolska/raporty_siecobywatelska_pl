from teryt_tree.factories import JednostkaAdministracyjnaFactory

from .import models


class JSTFactory(JednostkaAdministracyjnaFactory):
    class Meta:
        model = models.JST
