'''
Created on Jul 10, 2012

@author: Shift IT | wwww.shiftit.com.br
'''
from django.contrib                 import admin
from autenticacao.models            import Usuario

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save()

    def delete_model(self, requqest, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete()

    def queryset(self, vRequest):
        # Tell Django to look for objects on the 'other' database.
        qs = super(MultiDBModelAdmin, self).queryset(vRequest)
        iEmpresa= Usuario().obtemEmpresaDoUsuario(vRequest.user.id)
        if iEmpresa != None:
            try:
                return qs.filter(empresa= iEmpresa)
            except:
                return qs.all()
        else:
            return qs.all()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)