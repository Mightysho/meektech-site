from django import forms


class VisitorDateRangeExportForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"})
    )
