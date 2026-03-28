from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from mybase.models import Comment, Page, PostHistory, PostLike, Topic, TopicHistory


class ForumTestCase(TestCase):
    password = 'testpass123'

    def setUp(self):
        self.author = self.create_user('author')
        self.other_user = self.create_user('other-user')
        self.topic = self.create_topic('General Discussion')
        self.post = Page.objects.create(
            author=self.author,
            topic=self.topic,
            title='Original Title',
            body='Original body',
        )

    def create_user(self, username):
        return User.objects.create_user(username=username, password=self.password)

    def create_topic(self, name):
        return Topic.objects.create(name=name, description=f'{name} description')

    def create_post(self, username, topic_name, title, body='Body text'):
        user = self.create_user(username)
        topic = self.create_topic(topic_name)
        post = Page.objects.create(
            author=user,
            topic=topic,
            title=title,
            body=body,
        )
        return user, topic, post

    def login(self, user):
        self.client.login(username=user.username, password=self.password)


class PostEditorTests(ForumTestCase):
    def test_make_post_creates_post_and_redirects_to_detail(self):
        creator = self.create_user('creator')
        topic = self.create_topic('Announcements')
        self.login(creator)

        response = self.client.post(
            reverse('mybase:make_post', args=[topic.slug]),
            {
                'title': 'Fresh Post',
                'body': '<simples><p>Hello world</p></simples>',
            },
        )

        created_post = Page.objects.get(topic=topic)
        self.assertEqual(created_post.author, creator)
        self.assertEqual(created_post.title, 'Fresh Post')
        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[topic.slug, created_post.slug]),
        )

    def test_make_post_rejects_second_post_in_same_topic(self):
        topic_reviewer = self.create_user('topic-reviewer')
        self.login(topic_reviewer)

        response = self.client.post(
            reverse('mybase:make_post', args=[self.topic.slug]),
            {
                'title': 'Duplicate Topic Post',
                'body': 'This should not be created',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'This topic already has a post and cannot accept another one right now.',
        )
        self.assertEqual(Page.objects.filter(topic=self.topic).count(), 1)

    def test_make_post_rejects_second_post_for_same_author(self):
        second_topic = self.create_topic('Release Notes')
        self.login(self.author)

        response = self.client.post(
            reverse('mybase:make_post', args=[second_topic.slug]),
            {
                'title': 'Second Author Post',
                'body': 'This should not be created',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Your account already has a post and cannot create another one right now.',
        )
        self.assertFalse(Page.objects.filter(topic=second_topic).exists())

    def test_edit_post_prefills_existing_content_for_author(self):
        self.login(self.author)

        response = self.client.get(
            reverse('mybase:edit_post', args=[self.topic.slug, self.post.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Post')
        self.assertContains(response, 'Original Title')
        self.assertContains(response, 'Original body')

    def test_edit_post_updates_post_and_redirects(self):
        self.login(self.author)

        response = self.client.post(
            reverse('mybase:edit_post', args=[self.topic.slug, self.post.slug]),
            {
                'title': 'Updated Title',
                'body': 'Updated body content',
            },
        )

        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.body, 'Updated body content')
        self.assertEqual(self.post.slug, 'updated-title')
        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]),
        )

    def test_edit_post_rejects_non_author(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:edit_post', args=[self.topic.slug, self.post.slug]),
            {
                'title': 'Malicious Update',
                'body': 'Should not save',
            },
        )

        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.post.title, 'Original Title')
        self.assertEqual(self.post.body, 'Original body')


class BackendInteractionTests(ForumTestCase):
    def test_like_post_creates_like_updates_count_and_honours_next_redirect(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:like_post', args=[self.topic.slug, self.post.slug]),
            {
                'next': reverse('mybase:home'),
            },
        )

        self.post.refresh_from_db()
        self.assertRedirects(response, reverse('mybase:home'))
        self.assertTrue(PostLike.objects.filter(user=self.other_user, post=self.post).exists())
        self.assertEqual(self.post.likes, 1)

    def test_like_post_second_request_removes_like_and_resets_count(self):
        self.login(self.other_user)
        self.client.post(reverse('mybase:like_post', args=[self.topic.slug, self.post.slug]))

        response = self.client.post(
            reverse('mybase:like_post', args=[self.topic.slug, self.post.slug])
        )

        self.post.refresh_from_db()
        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]),
        )
        self.assertFalse(PostLike.objects.filter(user=self.other_user, post=self.post).exists())
        self.assertEqual(self.post.likes, 0)

    def test_view_post_post_request_adds_comment_records_history_and_increments_views(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]),
            {
                'body': 'Nice post',
            },
        )

        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.views, 1)
        self.assertTrue(PostHistory.objects.filter(user=self.other_user, post=self.post).exists())
        self.assertTrue(Comment.objects.filter(author=self.other_user, post=self.post, body='Nice post').exists())
        self.assertContains(response, 'Nice post')

    def test_view_topic_records_history_and_marks_post_as_liked_for_user(self):
        PostLike.objects.create(user=self.other_user, post=self.post)
        self.login(self.other_user)

        response = self.client.get(
            reverse('mybase:view_topic', args=[self.topic.slug])
        )

        self.topic.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.topic.views, 1)
        self.assertTrue(TopicHistory.objects.filter(user=self.other_user, topic=self.topic).exists())
        self.assertEqual(len(response.context['posts']), 1)
        self.assertTrue(response.context['posts'][0]['user_has_liked'])

    def test_home_lists_recent_topics_and_posts_from_history(self):
        self.login(self.other_user)
        self.client.get(reverse('mybase:view_topic', args=[self.topic.slug]))
        self.client.get(reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]))

        response = self.client.get(reverse('mybase:home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.topic, response.context['recent_topics'])
        self.assertIn(self.post, response.context['recent_posts'])
        self.assertContains(response, self.topic.name)
        self.assertContains(response, self.post.title)

    def test_saved_timestamps_are_timezone_aware(self):
        comment = Comment.objects.create(author=self.other_user, post=self.post, body='Aware timestamp')
        post_history = PostHistory.objects.create(user=self.other_user, post=self.post)
        topic_history = TopicHistory.objects.create(user=self.other_user, topic=self.topic)

        self.post.refresh_from_db()

        self.assertTrue(timezone.is_aware(self.post.created_at))
        self.assertTrue(timezone.is_aware(comment.created_at))
        self.assertTrue(timezone.is_aware(post_history.access_time))
        self.assertTrue(timezone.is_aware(topic_history.access_time))
