from rest_framework.response import Response


def check_admin(func):
    def verify_func(self,request,*args,**kwargs):
        if request.user.is_superuser:

            return func(self,request,*args,**kwargs)

        else:
            return Response('can\'t access this page, admin only')

    return verify_func
    