from django.db import models

class ElectricityBill(models.Model):
    connection_id = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    units_consumed = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.connection_id} - {self.customer_name}"
