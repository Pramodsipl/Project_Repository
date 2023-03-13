
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model,login,logout
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
import json
from account_app.models import Register_model
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string


User=get_user_model()


@api_view(["POST"])
def register_api(request):

    spc=['@','#','$','%','&','^','_','*']

    if 'email' not in request.data:
        return Response({"status":"fail","msg":"please enter the email"})

 #email valadtion
    

    if User.objects.filter(email=request.data['email'].strip()).exists():
        return Response({"status":"fail","msg":"this email is allredy exists"})
    if request.data['email'] == "":
        return Response({"status":"fail","msg":"email fiels must be fillup"})

    # first_name validations
    if 'first_name' not in request.data:
        return Response({"status":"fail","msg":"please enter the firstname"})

    if request.data['first_name'] == "":
          return Response({"status":"fail","msg":"first_name fiels must be fillup"})

    
    for a in request.data['first_name'].strip():
            if a in spc:
                return Response({"status":"fail","msg":"fistname can not contain special character"})
            if a.isdigit():
                return Response({"status":"fail","msg":"firstname can not digit name"})



    # last_name validations
    if 'last_name' not in request.data:
        return Response({"status":"fail","msg":"please enter the last_name"})

    if request.data['last_name']=="":
          return Response({"status":"fail","msg":"last_name fiels must be fillup"})

    for k in request.data['last_name']:
        if k in spc:
            return Response({"status":"fail","msg":"lastname can not contain special character"})
        if k.isdigit():
            return Response({"status":"fail","msg":"lastname can not digit name"})

# address validtion
    if 'address' not in request.data:
        return Response({"status":"fail","msg":"please enter the address"})

    if request.data['address']=="":
          return Response({"status":"fail","msg":"address fiels must be fillup"})

    for v in request.data['address']:
        if v in spc:
            return Response({"status":"fail","msg":"address can not contain special character"})
        if v.isdigit():
            return Response({"status":"fail","msg":"address can not digit name"})
    
    # city validtion
    if 'city' not in request.data:
        return Response({"status":"fail","msg":"please enter the city"})

    if request.data['city']=="":
          return Response({"status":"fail","msg":"city fiels must be fillup"})

    for v in request.data['city']:
        if v in spc:
            return Response({"status":"fail","msg":"city can not contain special character"})
        if v.isdigit():
            return Response({"status":"fail","msg":"city can not digit name"})
        
        

    # password validations

    l, u, p, d = 0, 0, 0, 0
    if 'password' not in request.data:
        return Response({"status":"fail","msg":"please enter the password"})

    if request.data['password']== "":
          return Response({"status":"fail","msg":"password fiels must be fillup"})

    if (len(request.data['password']) >= 8):
        for i in request.data['password']:
            if i.isupper():
                  l+=1
            elif i.islower():
                    u+=1
            elif i.isdigit():
                    p+=1
            elif i in spc:
                    d+=1

    else:
        #"Password Must Be More Then 8 Character Long..."
        return Response({"status":"fail","msg":"Password Must Be More Then 8 Character Long"})
    
    
          
    if request.data['password'] != request.data['confirm_pasword']:
        return Response({"status":"fail","msg":"your password doses not matched"})

    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(request.data['password'])):

           user=User.objects.create_user(email = request.data['email'].strip(), password = request.data['password'],first_name=request.data["first_name"],last_name=request.data["last_name"])
           Register_model.objects.create(user_id=user, address=request.data['address'], city=request.data['city'])

           token=Token.objects.get_or_create(user=user)
           token = " ".join([str(i) for i in token]).replace("True",'').strip()
           user.is_active=False
           user.save()
           subject="testing mail"
           from_mail='test1.softude@gmail.com'
        #    msg='<p> welcome to <b> on your gemail for verification </b></p?'
           msg= f' this is your activaction  link is http://127.0.0.1:8000/account_app/activate_account/'+token
        #    mail_mesage='<p> hiii pramod <b> you are welcome </b></p>'
           name=request.data["first_name"]
           mail_mesage =render_to_string('index.html',{'msgg':msg,'name':name})
           to=request.data['email']
           mail_mesage=EmailMultiAlternatives(subject, mail_mesage, from_mail, [to])
           mail_mesage.content_subtype='html'
           mail_mesage.send()


        

           # mail sending
        #    send_mail(
        #       'test sending mail',
        #         mail_mesage,
        #       'test1.softude@gmail.com',
        #       [request.data['email']],
        #       fail_silently=False,
        #       )
           return Response({"status":"successful","message": "You have successfully registred."})
    else:
        return Response({"status":"fail","msg":"Password Must Be Stronge Type"})

 # for login activation        
@api_view(["GET"])
def activate_account(request, token): 
    if Token.objects.filter(key = token).exists():
        tokens=Token.objects.get(key=token)
        tokens.user.is_active = True
        tokens.user.save()
        tokens.delete()
        return Response({"status":"success",'msg':'Your account has been activate successfully'})
    else:
        return Response({"status":"faild",'msg':'Activation link is invalid!'})


    # return Response({"status":"fail","msg":"check"})

@api_view(["POST"])
def logout_user(request):
    try:
        # user_token=key=request.headers["Authorization"]
        token=Token.objects.get(key=request.headers["Authorization"])
        token.user
        token.user_id
        logout(request)
        token.delete()
        return Response({"status":"succcess","message":"logout succesfull"})
    except:
        return Response({'status': 'fail', 'message': 'token is invalid.'})



    


# login user
@api_view(["POST"])
def login_api(request):
    try:
         E_mail=request.data['email']
         P_ssword=request.data['password']
         if not User.objects.filter(email=E_mail).exists():
             return Response({"status":"faild","msg":"you are not vaild for login"})
         else:
            user = authenticate(email=E_mail, password=P_ssword)
            if user:
                login(request,user)

                token=Token.objects.get_or_create(user=user)
                token = " ".join([str(i) for i in token]).replace("True",'').strip()

                return Response({'status':'success','token':token})
            return Response({'status':'fail', 'msg':"invalid creditionls"})
    except Exception:
        pass
    return Response({'status':400,'msg':"something went wrong"})


# reset password

@api_view(["POST"])   
def reset_password(request):
    email = request.data['email']
    user=User.objects.get(email=email)
    Register_model.objects.get(user_id=user)
    token=Token.objects.get_or_create(user=user)
    token = " ".join([str(i) for i in token]).replace("False",'').strip()
    mail_mesage = f'hey your Reset passward link is http://127.0.0.1:8000/account_app/change_password/'+token
    send_mail('test sending mail',
              mail_mesage,
              'test1.softude@gmail.com',
              [request.data['email']],
              fail_silently=False,
              )
    return Response({"status":"success","msg":"forgetpassward"})




# get user data based on id 
# @api_view(['GET'])
# def get_data(request, var=None):

#     try:
#         if var:
#             user=User.objects.filter(id=var).values('id',"email","first_name","last_name")
#             ud = Register_model.objects.filter(user_id = user[0]["id"]).values("city", 'address')
#             data = user[0]
#             for i,j in ud[0].items():
#                 data[i]=j
#             else:
#                 return Response({"status":"success","message":"users data","data":data})
#     except:
#         return Response({'status':"fail","msg":"user_id is not  avaliable please enter valid user_id"})
    
#     user=User.objects.all().values('id','email','first_name','last_name')
#     ud=Register_model.objects.all().values('address','city')

#     for i in range(len(user)):
#         for j,k in ud[i].items():
#                 user[i][j]=k
#     return Response({"status":"success","data":user})

# get user's data based on user's token


@api_view(['GET'])
def get_data(request):
    try:
        user_token= request.headers["Authorization"]
        # print(user_token)
        user1=Token.objects.get(key = user_token)
        user2=user1.user
        # print(user2)
        user_id1=user2.id
        if user_id1:
            user=User.objects.filter(id=user_id1).values('id',"email","first_name","last_name")
            ud = Register_model.objects.filter(user_id = user[0]["id"]).values("city", 'address')
            data = user[0]
            for i,j in ud[0].items():
                data[i]=j
            else:
                return Response({"status":"success","message":"users data","data":data})
    except:
         return Response({'status': 'fail', 'message': 'usertoken is invalid.'})
    










# totally or competlly update user data
    

@api_view(['PUT'])
def update_user_data(request,update_id):
    user=User.objects.filter(id=update_id)
    if user.exists():
        user.update( first_name=request.data['first_name'], last_name=request.data['last_name'])
        Register_model.objects.filter(user_id=update_id).update( address=request.data['address'], city=request.data['city'])
        return Response({"status":"success","msg":"data updated successfully"})
    else:
        return Response({"status":"faild","msg":"sorry cant update user is not avalible"})

# delete users data

@api_view(['DELETE'])
def delete_user_data(request,delete_id):
    user= User.objects.filter(id=delete_id)
    if user.exists():
        user.delete() 
        Register_model.objects.filter(user_id=delete_id)
        return Response({"status":"success","msg":"data successfully deleated"})
    else:
        return Response({"status":"faild","msg":"this user_id is not available"})

        
# partallu updated users data
@api_view(['PATCH'])
def partial_update(request,pathch_id=None):

    user=User.objects.filter(id=pathch_id)
    if user.exists():
        my_dict=dict(request.data.lists())
        total_data={}
        user_update_data={}
        register_update_data={} 
        for k,v in my_dict.items():
            total_data.update({k:v[0]})
        if 'first_name' in total_data:
            user_update_data['first_name']=request.data['first_name']

        if 'last_name' in total_data:
            user_update_data['last_name']=request.data['last_name']

        if 'email' in total_data:
            user_update_data['email']=request.data['email']

        if 'address' in total_data:
            register_update_data['address']=request.data['address']

        if 'city' in total_data:
            register_update_data['city']=request.data['city']

        user.update(**user_update_data)

        Register_model.objects.filter(user_id=pathch_id).update(**register_update_data)
        return Response({"status":"success","msg":"data updated successfully"})
    else:
        return Response({"status":"faild","msg":"sorry cant update user is not avalible"})

# change password
@api_view(['POST'])
def change_password(request):
    # email = request.data['email']
    # old_password = request.data['old_password']
    # user = authenticate(email=email, password=old_password)
    try:
        user_token= request.headers["Authorization"]

        # user_token=request.data["Token"]
        # print(user_token)
        user1=Token.objects.get(key = user_token)
        user1=user1.user
        if user_token:
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']
            first_isalpha = new_password[0].isalpha()

            if user1.check_password(new_password):
                return Response({'status': 'fail', 'message': 'sorry can not updeted because your old pass_word and new_password are  same'}) 

            if new_password != confirm_password:
                return Response({'status': 'fail', 'message': 'New password and confirm password are not matched.'})
            if len(new_password) < 8:
                return Response({'status': 'fail', 'message': 'Password must be at least 8 characters long.'})
            if all(c.isalpha() == first_isalpha for c in new_password):
                return Response({'status': 'fail', 'message': 'Password must be a combination of characters with '
                                                            'numbers or special characters.'})
            user=User.objects.get(email=user1)
            user.set_password(new_password)
            user.save()
            return Response({'status': 'success', 'message': 'Password updated successfully'})
        return Response({'status': 'fail', 'message': 'Old password did not match.'})
    except: 
        return Response({'status': 'fail', 'message': 'token is invalid.'})

