# get_dropbox_tokens.py

import dropbox

APP_KEY = '2d89ue74jac5ke2'
APP_SECRET = 'z1vst5nylfrgjnf'

auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

authorize_url = auth_flow.start()
print("🔗 افتح الرابط التالي في المتصفح وامنح التطبيق الإذن:\n", authorize_url)

auth_code = input("📥 الصق الكود الذي حصلت عليه بعد الموافقة: ").strip()
oauth_result = auth_flow.finish(auth_code)

print("\n✅ تم الحصول على الرموز بنجاح:")
print("Access Token:", oauth_result.access_token)
print("Refresh Token:", oauth_result.refresh_token)
