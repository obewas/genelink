from django.db import models

# Create your models here.
class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    clan_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    father = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children_by_father')
    mother = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children_by_mother')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_parents(self):
        return [self.father, self.mother]

    def get_children(self):
        return Person.objects.filter(models.Q(father=self) | models.Q(mother=self))
