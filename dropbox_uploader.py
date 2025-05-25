import dropbox
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode
from dotenv import load_dotenv
import os

load_dotenv()  # تحميل المتغيرات من ملف .env

# قيم التكوين:
CLIENT_ID = '2d89ue74jac5ke2'           # من إعدادات تطبيقك في Dropbox
CLIENT_SECRET = 'z1vst5nylfrgjnf'    # استبدلها بالسر الخاص بك
REFRESH_TOKEN = 'Uwt_b0S4IlcAAAAAAAAAARoYtwa42JuqUvjvXQWdZk5_g2J47nr5NZiF-FrqTwKO'
ACCESS_TOKEN = 'sl.u.AFuCsbT2OznTjvRpJHBOHo4X3y9W0N7z9-ieLB9EQ9OD5vJtFj8JHqMO8Icr3Ctlf5GUQhRzsWyQuoGXcc5D0C-iFFurN17yYM8lb_hXgZ4MP5m3YRvn86TTF5ODyo5XFTc3exu49mJ6bJNaqo707LFOAP67gOPv7SCvYoYB97mRA4d09GH3fZn3fcFBE7pXXbPUCUwl2gQwBbXDGQyRspYqXBXv7BSAPYtz_JNIqrL-s1ZvmiLsa-euyw6iws3Lz8UKpP-f1DZAnQ5yJvHKQl7baHBDNhcGB4zIe0i0tYP1pXLAiRvs0yyHgIN5Gs_HmZZ06O4P8gmOA4Ud4kRfFnC4GK7sv-A7dgKBSfsX2BL3v17Q-uX4Xv2v-KtaoczKSYSdC809WKwFa-gNcV7elC6wPHfigTt1zm-gVBEZDWmkbv2mzNH3xUbmqkFJOmIkWx3JQ1LUPWsVoPr1xsRt6F5qeD-f1c-8gyLkFnpma5Vjg6cZUumW_cm2VEH_YViRpFkI_nHsM5spUYPwANTPuNZ-T1dOw8bqZDiI7OUcNMLZQa1aI9Z4LC48mTNihew2IfI7adt3qPe0Ncm2gXQ2W2Saj3BA22EuwaVHFwFR0uTDY0gej_6ZhcUzV2MUxiGnyPB47yIgqZJ-6sLGDHrZRmHaEAdq6yYIaiVsc8h9alBYcubS3hyndiVPOSzTITjxepDr9zMkAhNiheoY2VD43RU01ezvQMy4XqdzPuxCNvdwh6cb3tcMsrNs4_cDwm5aDiPje8BBvd4ATLD4rGVz42oWT9yy5e-Mt2umHOQAS-ivF5APG8lquvHkEFCTPyU2qQ7wyWXkOVNIavE0588qolYAGhyBkTihTZ0gZp3ME8xdpmYiMgDxACyXBqm8_W027mSAQ_yHl2cuNDrc5cf_tFqOWFEm9xF9IVhwHDTveSN5nWHLKuToqQPEnNTcr40LGXXCgnsj8cIEDP5RkRYNHybciu7Au253mAurohCeYsVIYpQN-nh0LefRdvk1pJRoV4J3WyaUMky5kn4_oQMWIijSbUSH2Aqw6ZlV5329qYrxQ13nmidN1REKmpyOY3GbRPsfLbXvCyZ7BI87NXJDE9m4icFrT8_OEqQXxRAA2G1HQyOlA1JG9Fdinz0Kob0uU1sbvDiWSFWWTMW2_6PTvYJ9mFWH1vmUowsz0bov28NlGfX2DkztYK-Ad-qcmgcbDy4XHIHhCYjw8s8aKIszGASRxTTaCD0tHbYpvLfHDKWkHj10hAqO1rvqeZRKHxHCETdktcxtlMJLaMk3Tet0B3eJpPyNAB_dVCbQTbiNLfIWaJQkq0jtlIaJPstY0yYZSsvC5G_zDj2samSnAqwlt5OFs4g1rYgmEtsgQdOcf5cLScZ0bbUkIQLeNaBMzZp8MV3Bl8DPZ8QAzN9ndbkzMObm'

def get_dropbox_client():
    # انشاء دالة ترجع عميل Dropbox مع تحديث تلقائي للرمز
    return dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=CLIENT_ID,
        app_secret=CLIENT_SECRET,
        oauth2_access_token=ACCESS_TOKEN
    )

def upload_to_dropbox(local_path, dropbox_path):
    dbx = get_dropbox_client()

    # رفع الملف
    with open(local_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path, mode=WriteMode("overwrite"))

    try:
        # محاولة إنشاء رابط مشاركة
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        return shared_link_metadata.url
    except ApiError as e:
        if isinstance(e.error, dropbox.sharing.CreateSharedLinkWithSettingsError) and e.error.is_shared_link_already_exists():
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True).links
            if links:
                return links[0].url
        raise e

# مثال استدعاء:
# print(upload_to_dropbox('local_file.txt', '/folder_in_dropbox/remote_file.txt'))
