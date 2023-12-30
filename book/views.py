from django.shortcuts import render,redirect
from .models import Book,BorrowedBook,Review,Profile
from .forms import ReviewForm
from django.views.generic import DetailView,TemplateView,ListView,CreateView
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

class DetailBookView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('id')
        book = Book.objects.get(pk=book_id)
        context['book'] = book
        
        

        borrowed_book = BorrowedBook.objects.filter(book=book, account=self.request.user.account, returned=False).first()
        if borrowed_book:
            context['borrowed_book'] = borrowed_book

        # book = self.object
        comments = book.review.all()
        comment_form = ReviewForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = ReviewForm(data=self.request.POST)
        book = self.get_object() 
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book  
            new_comment.save()
        return self.get(request, *args, **kwargs)
    


# def profileView (request):
#     data = BorrowedBook.objects.all()
#     return render(request, 'profile.html', {'data': data})
    
def profileView (request):
    user_profile, created = Profile.objects.get_or_create(account=request.user.account)
    print(user_profile)
    data = user_profile.borrowed_book.all()
    return render(request, 'profile.html', {'data': data})

def borrow(request,id):
    book = Book.objects.get(pk=id) # id diye book ta dhorechi
    book_price =book.borrow_price # book er price
    account = request.user.account # user account
    initial_balance = account.balance# user er bortoman balance
    
    if initial_balance >= book_price:  
        new_balance = initial_balance - book_price # borrow korar por balance

        account.balance = new_balance # user er balance update kora hoise
        account.save(update_fields=['balance']) # update save

        borrowed_book = BorrowedBook.objects.create( # Borrowed_book e instance create korechi eta nije nijei save hoye jabe database e 
            book=book,
            account=account,
            balance_after_borrow=new_balance,
            # returned= True
        )

        user_profile, created = Profile.objects.get_or_create(account=request.user.account)
        user_profile.borrowed_book.add(borrowed_book)

        mail_subject = "Borrowed Successfully"
        messages = render_to_string("borrowed_mail.html", {
            'user': request.user,
            'book_price' : book_price,
        })
        send_email = EmailMultiAlternatives(mail_subject, messages, to=[request.user.email])
        send_email.attach_alternative(messages, "text/html")
        send_email.send()

        return redirect("detail_book", id=id)
    else:
        return redirect("detail_book", id=id)
        

    
def returned(request,id):
    borrowed_book = BorrowedBook.objects.get(pk=id)
    book_id = borrowed_book.book_id
    book_title = borrowed_book.book.title

    # print(f"Account****************** {Bbook} {Bbook.book.borrow_price}")
    # print (f"Account****************** {book}")
    # book = Book.objects.get(pk=id) 

    book_price =borrowed_book.book.borrow_price 
    account = request.user.account # user account
    initial_balance = account.balance # user er bortoman balance

    borrowed_book.returned = True
    borrowed_book.save(update_fields=['returned'])

    new_balance = initial_balance + book_price
    account.balance = new_balance # user er balance update kora hoise
    account.save(update_fields=['balance']) # update save

    return redirect("profile")
    