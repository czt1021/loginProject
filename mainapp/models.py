from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=100)
    token = models.CharField(max_length=32)
    photo = models.ImageField(upload_to='photos')

    def toDict(self):
        # 将对象转成dict
        print(self.photo.__dict__)
        return {"id":self.id,
                "passwd": self.passwd,
                "username": self.username,
                "photo": self.photo.name}
