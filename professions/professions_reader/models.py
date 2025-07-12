from django.db import models


class Accountant(models.Model):
    name = models.CharField(max_length=255)
    memberno = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    standing = models.CharField(max_length=255)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "accountant"
        unique_together = (("name", "memberno"),)

    def __str__(self):
        if "CPA" in self.name:
            return self.name.replace("CPA", "")
        return self.name


class Advocates(models.Model):
    name = models.TextField(blank=True)
    profile_image = models.TextField(blank=True)
    advocate_number = models.TextField(unique=True, blank=True)
    postal_address = models.TextField(blank=True)
    email = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    law_firm = models.TextField(blank=True)
    detail_page = models.TextField(blank=True)
    cpd_compliance = models.JSONField(blank=True)
    practice_distribution = models.JSONField(blank=True)
    meta = models.JSONField(blank=True)
    timestamp = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

    class Meta:
        managed = False
        db_table = "advocates"
    def __str__(self):
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
