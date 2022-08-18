from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack


class SnacksTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='fakeemail@email.com', password='password'
        )
        self.snack = Snack.objects.create(
            name='French Fries', description='Fried wedges of potato', purchaser=self.user,
        )

    def test_snack_list_view(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack-list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_snack_detail_view(self):
        response = self.client.get(reverse('snack_detail', args='1'))
        out_of_range = self.client.get("/12/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(out_of_range.status_code, 404)
        self.assertContains(response, 'Fried wedges of potato')
        self.assertTemplateUsed(response, 'snack-detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_snack_create_view(self):
        response = self.client.get(reverse('snack_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack-create.html')
        self.assertTemplateUsed(response, 'base.html')

        response = self.client.post(
            reverse('snack_create'),
            {
                'name': 'Potato Chips',
                'description': 'Fried thin slices of potato',
                'purchaser': self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse('snack_detail', args='2'))
        self.assertContains(response, 'added by test')
        self.assertContains(response, 'Potato Chips')

    def test_snack_delete_view(self):
        response = self.client.get(reverse('snack_delete', args='1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack-delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_snack_update_view(self):
        response = self.client.post(
            reverse('snack_update', args='1'),
            {'name': 'JoJos', 'description': 'Fried thick wedges of potato', 'purchaser': self.user.id}
        )
        self.assertRedirects(response, reverse('snack_detail', args='1'))

