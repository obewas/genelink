from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta


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

def relationship_checker(request):
    people = Person.objects.all()
    result = None

    if request.method == 'POST':
        person1_id = request.POST.get('person1')
        person2_id = request.POST.get('person2')

        person1 = Person.objects.get(pk=person1_id)
        person2 = Person.objects.get(pk=person2_id)

        if person1 == person2:
            result = "This is the same person."

        elif person1.father == person2.father and person1.father is not None and person1.mother == person2.mother:
            result = "They are siblings."

        elif person2 in person1.get_children():
            result = f"{person1.first_name} is the parent of {person2.first_name}."

        elif person1 in person2.get_children():
            result = f"{person1.first_name} is the child of {person2.first_name}."

        elif person1.father and (person1.father == person2 or person1.mother == person2):
            result = f"{person2.first_name} is a parent of {person1.first_name}."

        elif (person1.father and person1.father.father == person2) or (person1.mother and person1.mother.father == person2):
            result = f"{person2.first_name} is a grandparent of {person1.first_name}."

        elif (
            (person1.father and person1.father in person2.get_children()) or
            (person1.mother and person1.mother in person2.get_children())
        ):
            result = f"{person2.first_name} is an uncle/aunt of {person1.first_name}."

        elif (
            (person2.father and person2.father in person1.get_children()) or
            (person2.mother and person2.mother in person1.get_children())
        ):
            result = f"{person1.first_name} is an uncle/aunt of {person2.first_name}."

        else:
            result = "No direct relationship found (MVP scope)."

    return render(request, 'family/relationship_checker.html', {
        'people': people,
        'result': result
    })


def dashboard(request):
    total_people = Person.objects.count()
    male_count = Person.objects.filter(gender='M').count()
    female_count = Person.objects.filter(gender='F').count()
    other_count = Person.objects.filter(gender='O').count()

    unique_clans = Person.objects.values('clan_name').exclude(clan_name__isnull=True).distinct().count()

    oldest = Person.objects.exclude(date_of_birth__isnull=True).order_by('date_of_birth').first()
    common_surnames = (
        Person.objects.values('last_name')
        .annotate(count=Count('last_name'))
        .order_by('-count')[:3]
    )

    context = {
        'total_people': total_people,
        'male_count': male_count,
        'female_count': female_count,
        'other_count': other_count,
        'unique_clans': unique_clans,
        'oldest': oldest,
        'common_surnames': common_surnames,
    }
    return render(request, 'family/dashboard.html', context)
