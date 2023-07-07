from django.contrib import admin

from .models import Bank, Account, Transaction, Category


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', )


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank', 'amount', 'color', 'last_update')
    list_filter = ('bank', )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date', 'account', 'mean')
    list_filter = ('amount', 'date', 'account')


admin.site.register(Bank, BankAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
