from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from mybase.models import Comment, Page, PostHistory, PostLike, Topic, TopicHistory, UserProfile


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
    def test_make_post_page_includes_simples_error_display_integration(self):
        creator = self.create_user('preview-author')
        topic = self.create_topic('Preview Topic')
        self.login(creator)

        response = self.client.get(
            reverse('mybase:make_post', args=[topic.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-simples-error-panel')
        self.assertContains(response, 'data-simples-error-list')
        self.assertContains(response, 'CallableSimplesIntegration.js')

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

    def test_make_post_allows_second_post_in_same_topic(self):
        topic_reviewer = self.create_user('topic-reviewer')
        self.login(topic_reviewer)

        response = self.client.post(
            reverse('mybase:make_post', args=[self.topic.slug]),
            {
                'title': 'Duplicate Topic Post',
                'body': 'This should not be created',
            },
        )

        created_post = Page.objects.filter(topic=self.topic).order_by('-id').first()

        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[self.topic.slug, created_post.slug]),
        )
        self.assertEqual(Page.objects.filter(topic=self.topic).count(), 2)
        self.assertEqual(created_post.author, topic_reviewer)
        self.assertEqual(created_post.title, 'Duplicate Topic Post')

    def test_make_post_with_duplicate_title_in_same_topic_gets_unique_slug(self):
        topic_reviewer = self.create_user('duplicate-title-reviewer')
        self.login(topic_reviewer)

        response = self.client.post(
            reverse('mybase:make_post', args=[self.topic.slug]),
            {
                'title': self.post.title,
                'body': 'A second post with the same title',
            },
        )

        duplicate_post = Page.objects.filter(topic=self.topic).order_by('-id').first()

        self.assertNotEqual(duplicate_post.pk, self.post.pk)
        self.assertEqual(duplicate_post.slug, 'original-title-2')
        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[self.topic.slug, duplicate_post.slug]),
        )

    def test_make_post_allows_second_post_for_same_author(self):
        second_topic = self.create_topic('Release Notes')
        self.login(self.author)

        response = self.client.post(
            reverse('mybase:make_post', args=[second_topic.slug]),
            {
                'title': 'Second Author Post',
                'body': 'This should not be created',
            },
        )

        created_post = Page.objects.get(topic=second_topic)

        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[second_topic.slug, created_post.slug]),
        )
        self.assertEqual(created_post.author, self.author)
        self.assertEqual(created_post.title, 'Second Author Post')

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

    def test_edit_post_to_existing_title_gets_unique_slug(self):
        other_post = Page.objects.create(
            author=self.other_user,
            topic=self.topic,
            title='Another Title',
            body='Other body',
        )
        self.login(self.author)

        response = self.client.post(
            reverse('mybase:edit_post', args=[self.topic.slug, self.post.slug]),
            {
                'title': other_post.title,
                'body': 'Updated body content',
            },
        )

        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Another Title')
        self.assertEqual(self.post.slug, 'another-title-2')
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


class FormFlowTests(ForumTestCase):
    def test_sign_up_creates_profile_logs_user_in_and_redirects_home(self):
        response = self.client.post(
            reverse('sign_up'),
            {
                'username': 'new-user',
                'email': 'new-user@example.com',
                'password1': 'safe-password-123',
                'password2': 'safe-password-123',
            },
        )

        created_user = User.objects.get(username='new-user')
        self.assertRedirects(response, reverse('mybase:home'))
        self.assertTrue(UserProfile.objects.filter(user=created_user).exists())
        self.assertEqual(self.client.session.get('_auth_user_id'), str(created_user.pk))

    def test_user_login_respects_safe_next_redirect(self):
        response = self.client.post(
            reverse('user_login'),
            {
                'username': self.author.username,
                'password': self.password,
                'next': reverse('mybase:make_topic'),
            },
        )

        self.assertRedirects(response, reverse('mybase:make_topic'))
        self.assertEqual(self.client.session.get('_auth_user_id'), str(self.author.pk))

    def test_edit_user_profile_updates_user_and_profile_fields(self):
        self.login(self.author)

        response = self.client.post(
            reverse('edit_user_profile'),
            {
                'username': 'updated-author',
                'email': 'updated-author@example.com',
                'bio': 'Updated bio text',
            },
        )

        self.author.refresh_from_db()
        profile = UserProfile.objects.get(user=self.author)

        self.assertRedirects(response, reverse('view_profile', args=[self.author.username]))
        self.assertEqual(self.author.username, 'updated-author')
        self.assertEqual(self.author.email, 'updated-author@example.com')
        self.assertEqual(profile.bio, 'Updated bio text')

    def test_make_topic_rejects_whitespace_only_name(self):
        self.login(self.author)

        response = self.client.post(
            reverse('mybase:make_topic'),
            {
                'name': '   ',
                'description': 'Whitespace-only topic name',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Topic name cannot be blank.')
        self.assertFalse(Topic.objects.filter(description='Whitespace-only topic name').exists())

    def test_view_post_rejects_whitespace_only_comment(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]),
            {
                'body': '   ',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comment cannot be blank.')
        self.assertFalse(Comment.objects.filter(author=self.other_user, post=self.post).exists())


class BackendInteractionTests(ForumTestCase):
    def test_toggle_like_post_redirects_to_topic_and_updates_count(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:toggle_like_post', args=[self.topic.slug, self.post.slug])
        )

        self.post.refresh_from_db()
        self.topic.refresh_from_db()
        self.assertRedirects(response, reverse('mybase:view_topic', args=[self.topic.slug]))
        self.assertTrue(PostLike.objects.filter(user=self.other_user, post=self.post, topic=self.topic).exists())
        self.assertEqual(self.post.likes, 1)
        self.assertEqual(self.topic.likes, 1)

    def test_like_post_creates_like_updates_count_and_honours_next_redirect(self):
        self.login(self.other_user)

        response = self.client.post(
            reverse('mybase:like_post', args=[self.topic.slug, self.post.slug]),
            {
                'next': reverse('mybase:home'),
            },
        )

        self.post.refresh_from_db()
        self.topic.refresh_from_db()
        self.assertRedirects(response, reverse('mybase:home'))
        self.assertTrue(PostLike.objects.filter(user=self.other_user, post=self.post, topic=self.topic).exists())
        self.assertEqual(self.post.likes, 1)
        self.assertEqual(self.topic.likes, 1)

    def test_like_post_second_request_removes_like_and_resets_count(self):
        self.login(self.other_user)
        self.client.post(reverse('mybase:like_post', args=[self.topic.slug, self.post.slug]))

        response = self.client.post(
            reverse('mybase:like_post', args=[self.topic.slug, self.post.slug])
        )

        self.post.refresh_from_db()
        self.topic.refresh_from_db()
        self.assertRedirects(
            response,
            reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]),
        )
        self.assertFalse(PostLike.objects.filter(user=self.other_user, post=self.post, topic=self.topic).exists())
        self.assertEqual(self.post.likes, 0)
        self.assertEqual(self.topic.likes, 0)

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
        PostLike.objects.create(user=self.other_user, post=self.post, topic=self.topic)
        self.login(self.other_user)

        response = self.client.get(
            reverse('mybase:view_topic', args=[self.topic.slug])
        )

        self.topic.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.topic.views, 1)
        self.assertTrue(TopicHistory.objects.filter(user=self.other_user, topic=self.topic).exists())
        self.assertEqual(len(response.context['posts']), 1)
        self.assertTrue(response.context['posts'][0].user_has_liked)
        self.assertContains(
            response,
            reverse('mybase:toggle_like_post', args=[self.topic.slug, self.post.slug]),
        )
        self.assertContains(response, self.author.username)

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

    def test_search_results_include_named_topic_and_post_links(self):
        response = self.client.get(
            reverse('mybase:search'),
            {'q': 'Original', 'search_in': 'all', 'sort_by': 'most_liked'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('mybase:view_topic', args=[self.topic.slug]))
        self.assertContains(response, reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]))
        self.assertEqual(response.context['post_results'][0].topic, self.topic)
        self.assertEqual(response.context['post_results'][0].author, self.author)

    def test_view_profile_includes_stats_and_recent_post_links(self):
        Comment.objects.create(author=self.author, post=self.post, body='Profile comment')
        PostLike.objects.create(user=self.other_user, post=self.post, topic=self.topic)

        response = self.client.get(reverse('view_profile', args=[self.author.username]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post_count'], 1)
        self.assertEqual(response.context['comment_count'], 1)
        self.assertEqual(response.context['like_count'], 1)
        self.assertContains(response, reverse('mybase:view_post', args=[self.topic.slug, self.post.slug]))
        self.assertContains(response, reverse('mybase:view_topic', args=[self.topic.slug]))

    def test_saved_timestamps_are_timezone_aware(self):
        comment = Comment.objects.create(author=self.other_user, post=self.post, body='Aware timestamp')
        post_history = PostHistory.objects.create(user=self.other_user, post=self.post)
        topic_history = TopicHistory.objects.create(user=self.other_user, topic=self.topic)

        self.post.refresh_from_db()

        self.assertTrue(timezone.is_aware(self.post.created_at))
        self.assertTrue(timezone.is_aware(comment.created_at))
        self.assertTrue(timezone.is_aware(post_history.access_time))
        self.assertTrue(timezone.is_aware(topic_history.access_time))
