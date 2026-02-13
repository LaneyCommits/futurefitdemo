from django import forms


class GapAnalysisForm(forms.Form):
    resume_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 14,
            'placeholder': 'Paste your resume text here...',
            'class': 'form-textarea',
        }),
        label='Your Resume',
        required=True,
    )
    job_listing_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 14,
            'placeholder': 'Paste the job description or listing here...',
            'class': 'form-textarea',
        }),
        label='Job Listing',
        required=True,
    )
