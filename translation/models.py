from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Endpoint(models.Model):
    """
    Model to keep track of ML endpoints.
    Attributes:
        name: The name of endpoint used in API URL,
        owner: String with owner name
        created_at: DateTime when the endpoint was created
    """

    name = models.CharField(max_length=256)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MLAlgorithm(models.Model):
    """
    Model represents ML Algorithm to be used
     Attributes:
        name: The name of the algorithm.
        description: The short description of how the algorithm works.
        code: The code of the algorithm.
        version: The version of the algorithm similar to software versioning.
        owner: The name of the owner.
        created_at: The date when MLAlgorithm was added.
        parent_endpoint: The reference to the Endpoint.
    """

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)
    code = models.CharField(max_length=600000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MLRequest(models.Model):
    """
    MLRequest will keep information about all requests to ML algorithms.
    Attributes:
        input_data: The input data to ML algorithm in JSON format.
        full_response: The response of the ML algorithm.
        response: The response of the ML algorithm in JSON format.
        feedback: The feedback about the response in JSON format.
        created_at: The date when request was created.
        parent_mlalgorithm: The reference to MLAlgorithm used to compute response
    """

    input_data = models.CharField(max_length=20000)
    full_response = models.CharField(max_length=20000)
    response = models.CharField(max_length=20000)
    feedback = models.CharField(max_length=5000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.input_data)


class EnglishToHindiTranslation(models.Model):
    """
    EnglishToHindiTranslation will contain key value pairs
    of english to hindi translation
    Attributes:
        english: The key/ word to be translated
        hindi: The value with all possible options of translation in json format
    """

    english = models.CharField(max_length=255)
    hindi = models.JSONField(blank=True)

    def __str__(self):
        return self.english


class myuploadfile(models.Model):
    f_name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to="",blank=False,null=False)
    translated_file = models.FileField(upload_to="")

    def __str__(self):
        return self.f_name

class review(models.Model):

    rating=models.IntegerField()
    comment=models.TextField(max_length=500)

    def __str__(self):
        return str(self.rating)+ " " + self.comment


