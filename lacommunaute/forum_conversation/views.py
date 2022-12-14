import logging

from django.contrib import messages
from django.db.models import Count, Exists, OuterRef
from django.urls import reverse
from machina.apps.forum_conversation import views
from machina.core.loading import get_class

from lacommunaute.forum_conversation.forms import PostForm
from lacommunaute.forum_upvote.models import UpVote


logger = logging.getLogger(__name__)

TrackingHandler = get_class("forum_tracking.handler", "TrackingHandler")
track_handler = TrackingHandler()


class SuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            "forum:forum",
            kwargs={
                "pk": self.forum_post.topic.forum.pk,
                "slug": self.forum_post.topic.forum.slug,
            },
        )


class FormValidMixin:
    def form_valid(self, *args, **kwargs):
        valid = super().form_valid(*args, **kwargs)
        track_handler.mark_topic_read(self.forum_post.topic, self.request.user)
        return valid


class TopicCreateView(SuccessUrlMixin, FormValidMixin, views.TopicCreateView):
    pass


class TopicUpdateView(SuccessUrlMixin, FormValidMixin, views.TopicUpdateView):
    pass


class PostCreateView(SuccessUrlMixin, FormValidMixin, views.PostCreateView):
    pass


class PostUpdateView(SuccessUrlMixin, FormValidMixin, views.PostUpdateView):
    pass


class PostDeleteView(views.PostDeleteView):
    def get_success_url(self):
        messages.success(self.request, self.success_message)

        return reverse(
            "forum:forum",
            kwargs={
                "slug": self.object.topic.forum.slug,
                "pk": self.object.topic.forum.pk,
            },
        )


class TopicView(views.TopicView):
    def get_topic(self):
        topic = super().get_topic()
        topic.has_liked = self.topic.likers.filter(id=self.request.user.id).exists()
        topic.likes = self.topic.likers.count()
        return topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.topic.get_absolute_url()
        context["form"] = PostForm(forum=self.topic.forum, user=self.request.user)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            upvotes_count=Count("upvotes"),
            # using user.id instead of user, to manage anonymous user journey
            has_upvoted=Exists(UpVote.objects.filter(post=OuterRef("pk"), voter__id=self.request.user.id)),
        )
