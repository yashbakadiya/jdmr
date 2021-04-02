from django.db import models

import qrcode

# Create your models here.


class Qrcode(models.Model):
    certificate_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def save(self, *args, **kwargs):
        # Creating an instance of qrcode
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        qr.add_data(self.link)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        imgname = self.name+".png"
        img.save("media/qr_codes/"+imgname)
        self.qr_code = "qr_codes/"+imgname
        super(Qrcode, self).save(*args, **kwargs)
        
        

class Certificate(models.Model):
    certificate_num = models.CharField(max_length=30)
    register_num = models.CharField(max_length=30)
    issued = models.BooleanField(default=False)
    issued_date = models.DateField(default=None, null=True, blank=True)


class Certificate_sign(models.Model):
    sign = models.ImageField(upload_to="sign")
