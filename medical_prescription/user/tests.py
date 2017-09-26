from django.test import TestCase

from user.models import User
from user.views import ResetPasswordProfile
from user.forms import PatientForm, HealthProfessionalForm
# Create your tests here.


class LoginTeste(TestCase):
    def setUp(self):
        self.user = User()
        self.user.name = "Felipe"
        self.user.date_of_birth = "1995-01-01"
        self.user.phone = "9999-9999"
        self.user.sex = "F"
        self.user.email = "user@user.com"
        self.user.password = "testando"
        self.user.save()

    def test_save_name(self):
        self.assertEqual(self.user.name, "Felipe")

    def test_save_date_of_birth(self):
        self.assertEqual(self.user.date_of_birth, "1995-01-01")

    def test_save_phone(self):
        self.assertEqual(self.user.phone, "9999-9999")

    def test_save_sex(self):
        self.assertEqual(self.user.sex, "F")

    def test_save_email(self):
        self.assertEqual(self.user.email, "user@user.com")

    def test_save_password(self):
        self.assertEqual(self.user.password, "testando")

    def test_get_short_name(self):
        user_name = User.objects.get(name="Felipe")
        print("AQUI" + user_name.name)
        self.assertEqual(user_name.get_short_name(), "Felipe")


class MyTests(TestCase):

    def setUp(self):
        self.name_valid = 'Teste Nome'
        self.name_invalid = 'a'

        self.date_of_birth_valid = '10/12/1990'
        self.date_of_birth_invalid = '18'

        self.phone_valid = '123456789'
        self.phone_invalid = '456'

        self.email_valid = 'admin@admin.com'
        self.email_invalid = 'admin.com'

        self.sex_valid = 'M'
        self.sex_invalid = 'A'

        self.crm_valid = '12345'
        self.crm_invalid = '1'

        self.crm_state_valid = 'DF'
        self.crm_state_invalid = 'a'

        self.id_document_valid = '12345678910'
        self.id_document_invalid = '1234'

        self.password_valid = '1234567'
        self.password_invalid = '1234567891011'

    def test_forms_patient_is_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_patient_name_is_not_valid(self):
        form_data = {'name': self.name_invalid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_phone_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_invalid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'password_confirmation': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_email_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_invalid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_password_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_invalid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_password_confirmation_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_invalid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_id_document_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_invalid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_date_of_birth_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_invalid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_patient_sex_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'id_document': self.id_document_valid,
                     'sex': self.sex_invalid,
                     'date_of_birth': self.date_of_birth_valid}
        form = PatientForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_is_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_forms_health_professional_name_is_not_valid(self):
        form_data = {'name': self.name_invalid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_phone_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_invalid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'password_confirmation': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_email_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_invalid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_password_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_invalid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_password_confirmation_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_invalid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_crm_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_invalid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_crm_state_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_invalid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_valid}

        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_sex_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_invalid,
                     'date_of_birth': self.date_of_birth_valid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_forms_health_professional_date_of_birth_is_not_valid(self):
        form_data = {'name': self.name_valid,
                     'phone': self.phone_valid,
                     'email': self.email_valid,
                     'password': self.password_valid,
                     'confirm_password': self.password_valid,
                     'crm': self.crm_valid,
                     'crm_state': self.crm_state_valid,
                     'sex': self.sex_valid,
                     'date_of_birth': self.date_of_birth_invalid}
        form = HealthProfessionalForm(data=form_data)
        self.assertFalse(form.is_valid())
