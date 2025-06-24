from django import forms

class ElectricityBillForm(forms.Form):
    connection_id = forms.CharField(
        label="Connection ID", 
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., TNEB12345'})
    )
    customer_name = forms.CharField(
        label="Customer Name", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., NAME'})
    )
    previous_reading = forms.IntegerField(
        label="Previous Reading",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'in kWh'})
    )
    current_reading = forms.IntegerField(
        label="Current Reading",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'in kWh'})
    )

    def clean(self):
        cleaned_data = super().clean()
        prev = cleaned_data.get("previous_reading")
        curr = cleaned_data.get("current_reading")
        if prev is not None and curr is not None and curr < prev:
            raise forms.ValidationError("Current reading cannot be less than previous reading.")

class DeleteBillForm(forms.Form):
    connection_id = forms.CharField(
        label="Connection ID to Delete",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., TNEB12345'})
    )

class SearchBillForm(forms.Form):
    connection_id = forms.CharField(
        label="Connection ID to Search",
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., TNEB12345'})
    )
