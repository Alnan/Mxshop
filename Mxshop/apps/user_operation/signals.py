from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from user_operation.models import UserFav

# post_save:接收信号的方式
#sender: 接收信号的model
@receiver(post_save, sender=UserFav)
def create_UserFav(sender, instance=None, created=False, **kwargs):
    # 是否新建收藏，因为update的时候也会进行post_save，新建才让goods收藏+1
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

@receiver(post_delete, sender=UserFav)
def delete_UserFav(sender, instance=None, created=False, **kwargs):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()