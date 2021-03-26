from django.db import models
# from cinemadb.settings import AUTH_USER_MODEL

class Movie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.DurationField(max_length=180, default=120)
    ganre = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Session(models.Model):
    start = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return self.start

class Ticket(models.Model):
    price = models.FloatField()
    seat = models.IntegerField()
    owner = models.OneToOneField(Client, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.price

class Worker(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    salary = models.FloatField()

    def __str__(self):
        return self.name





    
