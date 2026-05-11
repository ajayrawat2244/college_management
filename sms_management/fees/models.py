from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import TenantModel


class FeeRecord(TenantModel):
    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="fee_record"
    )
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    academic_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def pending_amount(self):
        return max(self.total_fees - self.discount_amount - self.paid_amount, Decimal("0.00"))

    @property
    def is_fully_paid(self):
        return self.pending_amount <= Decimal("0.00")

    def clean(self):
        if self.student and self.tenant_id and self.student.tenant_id != self.tenant_id:
            raise ValidationError("Student and fee record must belong to the same tenant.")

        if self.paid_amount < 0:
            raise ValidationError({"paid_amount": "Paid amount cannot be negative."})

        if self.total_fees < 0:
            raise ValidationError({"total_fees": "Total fees cannot be negative."})

        if self.discount_amount < 0:
            raise ValidationError({"discount_amount": "Discount amount cannot be negative."})

        if self.paid_amount > self.total_fees:
            raise ValidationError({"paid_amount": "Paid amount cannot exceed total fees."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.academic_year}"


class FeeInstallment(TenantModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        OVERDUE = "OVERDUE", "Overdue"

    fee_record = models.ForeignKey(
        FeeRecord,
        on_delete=models.CASCADE,
        related_name="installments"
    )
    title = models.CharField(max_length=100, blank=True)
    installment_no = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    paid_on = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("fee_record", "installment_no")
        ordering = ["due_date", "installment_no"]

    @property
    def balance(self):
        return max(self.amount - self.paid_amount, Decimal("0.00"))

    def clean(self):
        if self.fee_record and self.tenant_id and self.fee_record.tenant_id != self.tenant_id:
            raise ValidationError("Installment and fee record must belong to the same tenant.")

        if self.amount < 0:
            raise ValidationError({"amount": "Amount cannot be negative."})

        if self.paid_amount < 0:
            raise ValidationError({"paid_amount": "Paid amount cannot be negative."})

        if self.paid_amount > self.amount:
            raise ValidationError({"paid_amount": "Paid amount cannot exceed installment amount."})

        if self.due_date and self.due_date < timezone.localdate() and self.status == self.Status.PENDING:
            self.status = self.Status.OVERDUE

    def save(self, *args, **kwargs):
        if self.due_date and self.due_date < timezone.localdate() and self.status == self.Status.PENDING:
            self.status = self.Status.OVERDUE
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fee_record.student} - Installment {self.installment_no}"


class StudentWallet(TenantModel):
    student = models.OneToOneField(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.student and self.tenant_id and self.student.tenant_id != self.tenant_id:
            raise ValidationError("Wallet and student must belong to the same tenant.")

        if self.balance < 0:
            raise ValidationError({"balance": "Wallet balance cannot be negative."})

    def add_balance(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        self.balance += amount
        self.full_clean()
        self.save(update_fields=["balance", "updated_at"])

    def deduct_balance(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        if amount > self.balance:
            raise ValidationError("Insufficient wallet balance.")
        self.balance -= amount
        self.full_clean()
        self.save(update_fields=["balance", "updated_at"])

    def __str__(self):
        return f"{self.student} Wallet"