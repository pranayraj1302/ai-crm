from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Interaction
from django.utils import timezone
from .AI import generate_followup_email
from django.contrib.auth.decorators import login_required

@login_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


@login_required
def add_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company = request.POST.get('company')
        notes = request.POST.get('notes')

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            notes=notes
        )
        return redirect('contact_list')

    return render(request, 'contacts/add_contact.html')


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    interactions = contact.interactions.all()

    return render(request, 'contacts/contact_detail.html', {
        'contact': contact,
        'interactions': interactions
    })


@login_required
def add_interaction(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    if request.method == 'POST':
        interaction_type = request.POST.get('interaction_type')
        notes = request.POST.get('notes')

        Interaction.objects.create(
            contact=contact,
            interaction_type=interaction_type,
            notes=notes,
            date=timezone.now()
        )

        return redirect('contact_detail', pk=pk)

    return render(request, 'contacts/add_interaction.html', {'contact': contact})


@login_required
def generate_email(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    interactions = contact.interactions.all()

    try:
        email_content = generate_followup_email(contact, interactions)
    except Exception as e:
        email_content = f"Error generating email: {str(e)}"

    return render(request, 'contacts/generated_email.html', {
        'contact': contact,
        'email_content': email_content
    })