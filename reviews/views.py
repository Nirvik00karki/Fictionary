from django.shortcuts import render, redirect
from .models import ProductReview
from .forms import ProductReviewForm

def submit_review(request):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Redirect to a "Thank You" page or wherever you want after successful submission
    else:
        form = ProductReviewForm()

    return render(request, 'review_form.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')