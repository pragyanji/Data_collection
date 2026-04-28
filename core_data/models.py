from django.db import models
from django.urls import reverse

class User_Details(models.Model):
    family_no = models.IntegerField()
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_details'
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
        ordering = ['-id']

# saves the data form the kobo toolbox
class Response_table(models.Model):
    metadata = models.JSONField()

    # def __str__(self):
    #     return self.metadata

    class Meta:
        db_table = 'response_table'
        verbose_name = 'Response Table'
        verbose_name_plural = 'Response Tables'
        ordering = ['-id']


class New_User(models.Model):

    name = models.CharField(max_length=200)
    age = models.IntegerField()

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


# model for the student details form  from the kobo toolbox

class Student(models.Model):
    name = models.CharField(max_length=200)
    stu_id = models.IntegerField(unique=True)
    age = models.IntegerField()
    contact = models.IntegerField()
    email = models.EmailField()
    parents_name = models.CharField(max_length=200)
    batch = models.DateField(("Batch"), auto_now=False, auto_now_add=False)
    faculty = models.CharField(max_length=200)

    class Meta:
        verbose_name = ("Student")
        verbose_name_plural = ("Students")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Student_detail", kwargs={"pk": self.pk})


class Student_fee(models.Model):
    # stu_id should be a foreign key to the student model
    stu_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    fee_amount = models.IntegerField()
    payed_amount = models.IntegerField()
    due_amount = models.IntegerField()
    pay_date = models.DateField(("Payment Date"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = ("Student_fee")
        verbose_name_plural = ("Student_fees")

    def __str__(self):
        return f"{self.stu_id.name} - {self.semester}"

    def get_absolute_url(self):
        return reverse("Student_fee_detail", kwargs={"pk": self.pk})
