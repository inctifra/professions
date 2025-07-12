from django.db import models

class Accountant(models.Model):
    name = models.CharField(max_length=255)
    memberno = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    standing = models.CharField(max_length=255)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accountant'
        unique_together = (('name', 'memberno'),)
    def __str__(self):
        if "CPA" in self.name:
            return self.name.replace("CPA", "")
        return self.name


class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.IntegerField()
    license_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    valid_till = models.DateField()
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pharmacy"
        unique_together = (("registration_number", "license_number"),)

    def __str__(self):
        return f"{self.name} ({self.registration_number})"


class Pharmtech(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.IntegerField()
    license_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    valid_till = models.DateField()
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pharmtech"
        unique_together = (("registration_number", "license_number"),)
        verbose_name = "Pharmtech"
        verbose_name_plural = "Pharmtechs"

    def __str__(self):
        return f"{self.name} ({self.registration_number})"
