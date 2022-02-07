from email import message
from django.db import models
from .utils import get_link_data , send_email
import urllib.request
import smtplib
import time

class Link(models.Model):
    name = models.CharField(max_length=220, blank=True)
    EMAIL = models.CharField(max_length=220, blank=True)
    SET_PRICE = models.CharField(max_length=220,blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ('price_difference', '-created')
    
    
    def save(self, *args, **kwargs):
        name, price = get_link_data(self.url)
        cp = self.SET_PRICE
        cp = float(cp)
        if cp > price:
            nline = '\n'
            llname = name[0:20]+'...'
            message = f"Hello User,{nline} price of {llname} is Rs. {price} which is less than the price that you set on our site go buy it before sale runs out {nline}{nline} click below to buy {nline}{self.url}"
            send_email(message,self.EMAIL)
        old_price = self.current_price
        if self.current_price:
            if price != old_price:
                diff = price - old_price
                self.price_difference = round(diff, 2)
                self.old_price = old_price
        else:
            self.old_price = 0
            self.price_difference = 0
        
        self.name = name
        self.current_price = price
        
        super().save(*args, **kwargs)