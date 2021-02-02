from rest_framework import serializers

from .models import AddFeesC, SubmitFees, Instalment


class AddFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFeesC
        fields = ("course", "intitute", "courseName", "forclass", "teachType", "duration", "fee_amt", "tax",
                  "final_amt", "no_of_installment", "typeOfCharge", "extra_charge", "feeDisc", "discValidity", "final_amount")


class SubmitFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitFees
        fields = (
            "student", "subject", "totalFee", "feePayed", "balanceFee", "instalmentDue", "totalInstallments"
        )


class NewInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitFees
        fields = (
            "feeObj", "instalmentNum", "paymentExp", "paymentDone"
        )
