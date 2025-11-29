from django.contrib import admin

from .models import Bank, Account, Transaction, Category


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'bic', 'swift')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bank', 'amount', 'color', 'last_update', 'status')
    list_filter = ('bank', 'status')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date', 'account', 'mean')
    list_filter = ('date', 'account')

admin.site.register(Bank, BankAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
