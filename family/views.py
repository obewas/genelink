from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm


# Create your views here.
def person_list(request):
    query = request.GET.get('q', '')
    clan = request.GET.get('clan', '')
    people = Person.objects.all()

    if query:
        people = people.filter(last_name__icontains=query)
    if clan:
        people = people.filter(clan_name__icontains=clan)

    return render(request, 'family/person_list.html', {
        'people': people,
        'query': query,
        'clan': clan,
    })

def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'family/person_detail.html', {'person': person})

def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'family/person_form.html', {'form': form})

def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_detail', pk=pk)
    else:
        form = PersonForm(instance=person)
    return render(request, 'family/person_form.html', {'form': form})

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'family/person_confirm_delete.html', {'person': person})
