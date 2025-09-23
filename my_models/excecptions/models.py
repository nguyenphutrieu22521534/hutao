from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)

    def __str__(self):
        return self.name

def get_person_by_email(email):
    try:
        person = Person.objects.get(email=email)
    except Person.DoesNotExist:
        return None
    except Person.MultipleObjectsReturned:
        person = Person.objects.filter(email=email).order_by('id').first()
    return person


result = get_person_by_email("someone@example.com")
if result is None:
    print("Không tìm thấy người.")
else:
    print("Tìm được:", result.name)
