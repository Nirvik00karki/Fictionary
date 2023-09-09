from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from django.contrib import messages
from .models import Novel, Chapter,Payment,CartChapter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import update_session_auth_hash

def home(request):
    novels = Novel.objects.all()
    context = {'novels': novels}
    
    return render(request, 'hello1.html', context)

def novel_details(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapters = Chapter.objects.filter(novel=novel)
    context = {
        'novels': [novel],
        'chapters': chapters,
    }
    return render(request, 'novel_details.html', context)
   
@login_required
def chapter_details(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    next_chapter = chapter.next_chapter

    user_has_payment = Payment.objects.filter(user=request.user, chapter=chapter).exists()

    if not user_has_payment:
        if next_chapter:
            return redirect('novels:make_payment', chapter_id=next_chapter.id)
        else:
            # Handle the case when there are no more chapters
            return HttpResponse("You have completed all chapters.")

    context = {
        'chapter': chapter,
        'user_has_payment': user_has_payment,
    }
    return render(request, 'chapter_details.html', context)


def update_chapter_navigation(novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    chapters = Chapter.objects.filter(novel=novel)

    for i, chapter in enumerate(chapters):
        previous_index = i - 1
        next_index = i + 1

        if previous_index >= 0:
            chapter.previous_chapter = chapters[previous_index]

        if next_index < len(chapters):
            chapter.next_chapter = chapters[next_index]

        chapter.save()
# noinspection PyUnusedLocal
def add_new_chapter(request,novel_id):
    new_chapter = Chapter.objects.create( 
        novel = get_object_or_404(Novel, id=novel_id),
        previous_chapter= None,  
        next_chapter= None, 
        )
        

    # Fetch the novel ID associated with the new chapter
    novel_id = new_chapter.novel.id
    update_chapter_navigation(novel_id)

@login_required
def make_payment(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    payment = Payment.objects.filter(user=request.user, chapter=chapter).first()
    user = request.user

    # Get the chapters in the user's cart
    cart_chapters = CartChapter.objects.filter(user=user)

    total_amount = sum(cart_chapter.chapter.amount for cart_chapter in cart_chapters)

    if request.method == 'POST':
        # Process the payment for the chapters in the cart
        for cart_chapter in cart_chapters:
            amount = cart_chapter.chapter.amount
            Payment.objects.create(user=user, chapter=cart_chapter.chapter, amount=amount)

        # Clear the user's cart after successful payment
        cart_chapters.delete()

        return redirect('novels:checkout_success')

    context = {
        'cart_chapters': cart_chapters,
        'total_amount': total_amount,
    }
    return render(request, 'make_payment.html', context)



@login_required
def checkout_success(request):
    messages.success(request, 'Payment successful. Enjoy your chapters!')
    return redirect('novels:home')

    
from novels.forms import CustomUserCreationForm, CustomAuthenticationForm
from novels.models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered.')
            return redirect('novels:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('novels:home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('novels:home')

from django.core.exceptions import ObjectDoesNotExist
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = CartChapter.objects.filter(user=self.request.user)
            total_amount = sum(cart_chapter.chapter.amount for cart_chapter in order) if order else 0
            return render(self.request, 'cart.html', {'cart': order, 'total_amount': total_amount})
        except ObjectDoesNotExist:
            return redirect('/')


@login_required
def make_payment(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    payment = Payment.objects.filter(user=request.user, chapter=chapter).first()
    user = request.user

    # Get the chapters in the user's cart
    cart_chapters = CartChapter.objects.filter(user=user)

    total_amount = sum(cart_chapter.chapter.amount for cart_chapter in cart_chapters)

    if request.method == 'POST':
        # Process the payment for the chapters in the cart
        for cart_chapter in cart_chapters:
            amount = cart_chapter.chapter.amount
            Payment.objects.create(user=user, chapter=cart_chapter.chapter, amount=amount)

        # Clear the user's cart after successful payment
        cart_chapters.delete()

        return redirect('novels:checkout_success')

    context = {
        'cart_chapters': cart_chapters,
        'total_amount': total_amount,
        'payment': payment,
    }
    return render(request, 'make_payment.html', context)

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)
        user = request.user

        # Add the chapter to the user's cart
        cart_chapter, created = CartChapter.objects.get_or_create(user=user, chapter=chapter)
        if not created:
            # Increment the quantity if the chapter is already in the cart
            cart_chapter.quantity += 1
            cart_chapter.save()

        return redirect('novels:novel_details', novel_id=chapter.novel.id)

class ViewCartView(LoginRequiredMixin, View):
    def get(self, request):
        cart_chapters = CartChapter.objects.filter(user=request.user)
        chapters = [cart_chapter.chapter for cart_chapter in cart_chapters]
        total_amount = sum(chapter.amount for chapter in chapters) if chapters else 0
        return render(request, 'cart.html', {'chapters': chapters, 'total_amount': total_amount})

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)
        cart_chapter = CartChapter.objects.filter(user=request.user, chapter=chapter).first()
        if cart_chapter:
            cart_chapter.delete()

        return redirect('novels:view_cart')





