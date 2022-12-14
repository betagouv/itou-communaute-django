import factory
from machina.test.factories.conversation import PostFactory as BasePostFactory, TopicFactory as BaseTopicFactory

from lacommunaute.forum.factories import ForumFactory
from lacommunaute.forum_conversation.forum_polls.factories import TopicPollVoteFactory
from lacommunaute.forum_conversation.models import Topic
from lacommunaute.forum_upvote.factories import UpVoteFactory
from lacommunaute.users.factories import UserFactory


class PostFactory(BasePostFactory):
    subject = factory.Faker("sentence", nb_words=5)
    content = factory.Faker("sentence", nb_words=40)
    poster = factory.SubFactory(UserFactory)

    class Params:
        anonymous = factory.Trait(
            anonymous_key=factory.fuzzy.FuzzyInteger(42),
            username=factory.fuzzy.FuzzyText(suffix="@neuralia.co"),
            poster=None,
        )
        with_upvote = factory.Trait(
            upvote=factory.RelatedFactory(
                UpVoteFactory,
                factory_related_name="post",
                voter=factory.SelfAttribute("post.poster"),
            )
        )


class TopicFactory(BaseTopicFactory):
    forum = factory.SubFactory(ForumFactory)
    poster = factory.SubFactory(UserFactory)
    subject = factory.Faker("sentence", nb_words=5)
    type = Topic.TOPIC_POST

    class Params:
        with_post = factory.Trait(
            post=factory.RelatedFactory(
                PostFactory,
                factory_related_name="topic",
                poster=factory.SelfAttribute("topic.poster"),
            )
        )

    @factory.post_generation
    def with_like(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.likers.add(self.poster.id)

    @factory.post_generation
    def with_poll_vote(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        TopicPollVoteFactory(poll_option__poll__topic=self, voter=self.poster)
