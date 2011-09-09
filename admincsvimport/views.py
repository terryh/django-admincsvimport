# -*- coding: utf-8 -*-
#   :author Terry Huang.
#   :license: BSD

import zipfile

#from django.db import connections, router, transaction, DEFAULT_DB_ALIAS
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

class UploadFileForm(forms.Form):
     file  = forms.FileField(label=_('File path'))
     #natural_key = forms.CharField(widget=forms.HiddenInput())

def export_as_csv_action(description="Export selected objects as CSV file",
                         **options):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    token from http://djangosnippets.org/snippets/2020/, but direct use serializers **options
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        csvdata = serializers.serialize('csv', queryset, **options) 
        response = HttpResponse(csvdata, mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
        return response
    export_as_csv.short_description = description
    return export_as_csv

@staff_member_required
def get_import(request, app_label, model):
    """ Usage:
        (r'^admin/(?P<app_label>.*)/(?P<model>.*)/import/', 'admincsvimport.views.get_import'),
    """
    ct = ContentType.objects.get(app_label=app_label, model=model)
    model_class = ct.model_class()
    app_label = ct.app_label
    model_name = ct.name
    opts = model_class._meta
    
    def process_data(data):
        #####################################################################  
        # start to process csv data here 
        objs = serializers.deserialize('csv',data)
        for o in objs:
            o.save()
        # end to process csv data here 
        #####################################################################  
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            upload_file = request.FILES['file']
            
            if upload_file.content_type.endswith('zip'):
                # zip file
                zip_file = zipfile.ZipFile(upload_file) 
                bad_file = zip_file.testzip()
                if bad_file:
                    return HttpResponse("Sorry, don't support this file format.")
                
                for filename in sorted(zip_file.namelist()):
                    if not filename.endswith('csv'):
                        continue
                    
                    data = zip_file.read(filename)
                    if len(data):
                        process_data(data)
            elif upload_file.content_type.endswith('csv'):
                process_data(upload_file.read())
            else:
                return HttpResponse("Sorry, don't support this file format.")
            
            return HttpResponseRedirect('/admin/%s/%s/' % (app_label, model_name))
    else:
        form = UploadFileForm()

    return render_to_response('admin/import_csv.html',locals(), context_instance=RequestContext(request))

