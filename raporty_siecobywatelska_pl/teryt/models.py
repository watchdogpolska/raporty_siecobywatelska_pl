from teryt_tree.models import JednostkaAdministracyjna


class JST(JednostkaAdministracyjna):
    # def institution_qs(self):
    #     Institution = self.institution_set.model
    #     return Institution.objects.area(self)

    class Meta:
        proxy = True
