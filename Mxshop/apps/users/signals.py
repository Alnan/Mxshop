# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from django.contrib.auth import get_user_model
# User = get_user_model()


# post_save：接收哪种信号，sender：接收哪个model的信号
# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     # 判断是否新建，新建才需要设置密码并保存，因为update的时候也会触发post_save
#     if created:
#         password = instance.password
#         instance.set_password(password)
#         instance.save()
