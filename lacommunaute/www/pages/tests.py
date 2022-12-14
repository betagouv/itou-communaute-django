from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse
from machina.core.loading import get_class
from machina.test.factories.forum import create_forum


assign_perm = get_class("forum_permission.shortcuts", "assign_perm")


class HomepageTest(TestCase):
    def test_home_page(self):
        url = reverse("pages:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_is_highlighted(self):
        forum = create_forum(is_highlighted=True)
        assign_perm("can_read_forum", AnonymousUser(), forum)

        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, reverse("forum:forum", kwargs={"slug": forum.slug, "pk": forum.id}), count=1)

    def test_is_not_highlighted(self):
        forum = create_forum(is_highlighted=False)
        assign_perm("can_read_forum", AnonymousUser(), forum)

        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, reverse("forum:forum", kwargs={"slug": forum.slug, "pk": forum.id}))

    def test_is_private(self):
        forum = create_forum(is_private=True, is_highlighted=True)
        assign_perm("can_read_forum", AnonymousUser(), forum)

        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, forum.name, count=1)
        self.assertContains(response, '<p class="text-muted">Communauté privée</p>', count=1)

    def test_is_not_private(self):
        forum = create_forum(is_private=False, is_highlighted=True)
        assign_perm("can_read_forum", AnonymousUser(), forum)

        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, forum.name, count=1)
        self.assertContains(response, '<p class="text-muted">Communauté publique</p>', count=1)

    def test_can_join_forum_members(self):
        forum = create_forum(is_highlighted=True)

        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("members:join_forum_form", kwargs={"token": forum.invitation_token}))
