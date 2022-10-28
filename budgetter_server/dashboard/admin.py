from django.contrib import admin

from .models import Bank, Account, Transaction, Category


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_logo')

    def has_logo(self, obj: Bank):
        logo = Bank.objects.filter(name=obj.name)[0].logo
        if logo is None:
            return False
        else:
            return True

    has_logo.short_description = 'Logo'


admin.site.register(Bank, BankAdmin)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
