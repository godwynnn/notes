from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Security(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True,null= True,)
    secret_question = models.CharField(max_length=225,blank=True,default='')
    secret_answer = models.CharField(max_length=225,blank=True,default='')
    previous_email = models.CharField(max_length=225,blank=True,default='')
    last_token = models.CharField(max_length=225,blank=True,default='')
    profile_updated = models.BooleanField(default=False,blank=True)
    suspension_count = models.IntegerField(default=0,blank=True)
    briefly_suspended = models.BooleanField(default=False,blank=True)
    time_suspended = models.DateTimeField(null=True, blank=True)
    time_suspended_timestamp = models.IntegerField(default=0,blank=True)
    locked = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=45, blank=True, default ='')
    email_confirmed = models.BooleanField(default=False)
    two_factor_auth_enabled = models.BooleanField(default=False)
    email_change_request = models.BooleanField(default=False)
    pending_email = models.EmailField(default='',blank=True)
    login_attempt_count = models.IntegerField(default=0)
    class Meta:
        db_table = 'security'


    def save(self,*args, **kwargs):

        if self.suspension_count>2:
            self.briefly_suspended = True
            self.time_suspended =  datetime.datetime.now()
            self.time_suspended_timestamp = datetime.datetime.now().timestamp()
        secret_question=''
        for char in self.secret_question:
            if char ==  '?':
                continue
            else:
                secret_question = secret_question +char
        self.secret_question = secret_question+'?'
        super(Security,self).save()




class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    picture=models.ImageField(null=True,blank=True,upload_to='images/')
    is_temporary_password=models.BooleanField(default=False,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: PROFILE"

    class Meta:
        db_table='profiles'



class Facilities(models.Model):
    name=models.CharField(max_length=225,blank=True)
    facility_id=models.PositiveBigIntegerField(default=0,null=True,blank=True)
    user=models.ManyToManyField(User,blank=True,related_name='users')

    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}: FACILITY"
    
    
    class Meta:
        db_table='facilities'

    # def save(self,*args,**kwargs):
    #     count=0
    #     if len(Facilities.objects.all())>=1:
    #         count=len(Facilities.objects.all())+1
    #     self.facility_id=count
    #     super(Facilities,self).save(*args,**kwargs)
                
# class AssingFacility(models.Model):
#     facility=models.ForeignKey(Facilities,null=True,related_name='facilities', blank=True,on_delete=models.CASCADE)
#     user=models.ForeignKey(User,null=True,blank=True,related_name='users',on_delete=models.CASCADE)
#     date_added=models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.email} {self.facility}: FACILITY "

# class Meta:
#         db_table='assing_facility\'s'
    


class Notes(models.Model):
    note=models.TextField(null=True,blank=True,max_length=100)
    facility=models.ForeignKey(Facilities,null=True,blank=True,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True,null= True)
    date_time_added=models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User,blank=True,related_name="shared_users")
    shared=models.BooleanField(default=False)
    def delete(self,*args,**kwargs):
        self.is_deleted = True
        super(Notes,self).save(*args,**kwargs)    
    
    # def save(self,*args,**kwargs):
    #     users=User.objects.all()
    #     for user in users:
    #         if user  in self.shared_with.all():
    #             self.shared=True
    #         else:
    #             self.shared = False

    #     super(Notes,self).save(*args,**kwargs) 
    
    def __str__(self):
        return f"{self.user.email} Notes"

    
    class Meta:
        db_table='notes'
        ordering=['-date_time_added']


        

class Comments(models.Model):
    note=models.ForeignKey(Notes,on_delete=models.DO_NOTHING,related_name='comments',max_length=10000)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING,blank=True,null= True)
    comment=models.TextField(null=True,blank=True)
    date_time_added=models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def delete(self,*args,**kwargs):
        self.is_deleted = True
        super(Comments,self).save(*args,**kwargs)    
    
    
    def __str__(self):
        return f"Comment by {self.note.user.first_name}"

    class Meta:
        ordering=['-date_time_added']
        db_table='comments'