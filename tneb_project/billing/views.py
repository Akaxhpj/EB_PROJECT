from django.shortcuts import render, get_object_or_404, redirect
from billing.models import ElectricityBill
from billing.forms import ElectricityBillForm, DeleteBillForm, SearchBillForm

def homepage(request):
    if request.method == "POST":
        form = ElectricityBillForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            connection_id = data["connection_id"]

            # Check for duplicate connection ID
            if ElectricityBill.objects.filter(connection_id=connection_id).exists():
                return render(request, "duplicate_entry.html")

            previous = data["previous_reading"]
            current = data["current_reading"]

            if current < previous:
                return render(request, "invalid_readings.html")

            units = current - previous
            amount = calculate_bill(units)

            bill = ElectricityBill(
                connection_id=connection_id,
                customer_name=data["customer_name"],
                previous_reading=previous,
                current_reading=current,
                units_consumed=units,
                amount=amount
            )
            bill.save()
            return redirect("/show/")
        else:
            return render(request, "invalid_readings.html")
    else:
        form = ElectricityBillForm()

    return render(request, "add_bill.html", {"form": form})


def show(request):
    bills = ElectricityBill.objects.all().values()
    return render(request, "show_bills.html", {"bills": bills})


def update(request):
    if request.method == "POST":
        form = ElectricityBillForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                bill = ElectricityBill.objects.get(connection_id=data["connection_id"])
            except ElectricityBill.DoesNotExist:
                return render(request, "not_found.html")

            if data["current_reading"] < data["previous_reading"]:
                return render(request, "invalid_readings.html")

            bill.customer_name = data["customer_name"]
            bill.previous_reading = data["previous_reading"]
            bill.current_reading = data["current_reading"]
            bill.units_consumed = bill.current_reading - bill.previous_reading
            bill.amount = calculate_bill(bill.units_consumed)
            bill.save()
            return redirect("/show/")
        else:
            return render(request, "form_error.html")
    else:
        form = ElectricityBillForm()

    return render(request, "update_bill.html", {"form": form})


def delete(request):
    if request.method == "POST":
        form = DeleteBillForm(request.POST)
        if form.is_valid():
            connection_id = form.cleaned_data["connection_id"]
            try:
                bill = ElectricityBill.objects.get(connection_id=connection_id)
                bill.delete()
                return redirect("/show/")
            except ElectricityBill.DoesNotExist:
                return render(request, "not_found.html")
        else:
            return render(request, "form_error.html")
    else:
        form = DeleteBillForm()

    return render(request, "delete_bill.html", {"form": form})


def search(request):
    if request.method == "POST":
        form = SearchBillForm(request.POST)
        if form.is_valid():
            connection_id = form.cleaned_data["connection_id"]
            try:
                bill = ElectricityBill.objects.get(connection_id=connection_id)
                return render(request, "show_bills.html", {"bills": [bill]})
            except ElectricityBill.DoesNotExist:
                return render(request, "not_found.html")
        else:
            return render(request, "form_error.html")
    else:
        form = SearchBillForm()

    return render(request, "search_bill.html", {"form": form})


def calculate_bill(units):
    if units <= 100:
        return units * 1.5
    elif units <= 300:
        return (100 * 1.5) + (units - 100) * 2.5
    else:
        return (100 * 1.5) + (200 * 2.5) + (units - 300) * 4
