# backend/server/apps/endpoints/views.py file
# please add imports
import json
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from apps.ml.income_classifier.anomaly_detection import AnomalyDetector
from .models import DatosMovimiento
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# View for monitoring
def index(request):
    #data = DatosMovimiento.objects.all()
    data_set = DatosMovimiento.objects.order_by('-fecha', '-hora')
    page = request.GET.get('page', 1)
    paginator = Paginator(data_set, 10)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    context = {'data': data}
    return render(request, "endpoints/tables.html", context)

# View for predict
class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        algs = AnomalyDetector()
        prediction = algs.compute_prediction(request.data)

        return Response(prediction)