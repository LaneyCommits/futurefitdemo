from django.shortcuts import render
from django.views.generic import TemplateView
from .analysis import run_gap_analysis
from .forms import GapAnalysisForm


class HomeView(TemplateView):
    template_name = 'resume_analysis/home.html'


def gap_analysis_view(request):
    result = None
    if request.method == 'POST':
        form = GapAnalysisForm(request.POST)
        if form.is_valid():
            resume_text = form.cleaned_data['resume_text']
            job_listing_text = form.cleaned_data['job_listing_text']
            result = run_gap_analysis(resume_text, job_listing_text)
    else:
        form = GapAnalysisForm()
    return render(request, 'resume_analysis/gap_analysis.html', {'form': form, 'result': result})
