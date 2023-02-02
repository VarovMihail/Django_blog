# from action.models import Follower
#
#
# class FollowService():
#     def __init__(self, follower, content_maker):
#         self.follower = follower
#         self.content_maker = content_maker
#
#     def get_subscribe_status(self) -> int:
#         if Follower.objects.filter(follower=self.follower, content_maker=self.content_maker):
#             subscribe_status = 1
#         else:
#             subscribe_status = -1
#
#         return subscribe_status
