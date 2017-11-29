# standard library
import json

# django
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# local django
from user.decorators import is_health_professional
from prescription.models import Prescription


class SugestionsCid(View):
    """
    Responsible for obtaining suggested prescriptions to the CID.
    """

    @method_decorator(login_required)
    @method_decorator(is_health_professional)
    def dispatch(self, *args, **kwargs):
        return super(SugestionsCid, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            id_cid = request.POST.get('id', False)
            prescriptions = Prescription.objects.filter(cid=id_cid, health_professional=request.user.healthprofessional)

            result = dict()
            list_prescription = []
            result['status'] = "success"

            for prescription in prescriptions:
                prescription_item = {}
                prescription_item['id'] = prescription.id
                prescription_item['cid'] = prescription.cid.description
                prescription_item['medicines'] = self.get_medicines(prescription)
                # prescription_item['exams'] = self.get_exams(prescription)
                list_prescription.append(prescription_item)

            result['data'] = list_prescription

            mimetype = 'application/json'
            return HttpResponse(json.dumps(result), mimetype)

    def get_medicines(self, prescription):
        list_medicines = []
        for medicine in prescription.medicines.all():
            medicine_item = {}
            medicine_item['name'] = medicine.name
            list_medicines.append(medicine_item)

        for medicine in prescription.manipulated_medicines.all():
            medicine_item = {}
            medicine_item['name'] = medicine.recipe_name
            list_medicines.append(medicine_item)

        return list_medicines

    def get_exams(self, prescription):
        list_exams = []
        for exam in prescription.default_exams.all():
            exam_item = {}
            exam_item['name'] = exam.description
            list_exams.append(exam_item)

        for exam in prescription.custom_exams.all():
            exam_item = {}
            exam_item['name'] = exam.name
            list_exams.append(exam_item)

        return list_exams