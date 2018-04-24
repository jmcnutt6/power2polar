from import_export.admin import ImportMixin

from datetime import datetime, timedelta
import csv
import StringIO

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

from .models import PowerSchoolStudent
from .models import PolarisStudent
from .models import LibrarianStudent
from .import_export_resources import LibrarianStudentResource


class PowerSchoolStudentAdmin(admin.ModelAdmin):
    list_display = ["nameLast", "nameFirst", "studentID"]
    search_fields = ["nameLast", "nameFirst", "studentID"]
    list_filter = ["enrolled", "school"]

    def create_csv(self, request, queryset):
        queryset = queryset.filter(polaris=None,enrolled=True)
        if not queryset:
            return
        rightnow = datetime.now()
        f = StringIO.StringIO()
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['patronBarcode',
                         'nameFirst',
                         'nameLast',
                         'birthDate',
                         'studentID',
                         'grade',
                         'teacher',
            ])

        for s in queryset:
            writer.writerow(['',
                             s.nameFirst,
                             s.nameLast,
                             s.birthDate,
                             s.studentID,
                             s.grade,
                             s.teacher,
                ])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        filename = filename = "LibrarianStudent_{}.csv".format(rightnow.strftime("%Y%m%d%H%M"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    create_csv.label = "Create CSV"
    create_csv.short_description = "Create Librarian CSV exculding students with existing barcodes"

    actions = ['create_csv']


class PolarisStudentAdmin(admin.ModelAdmin):
    list_display = ["nameLast",
                    "nameFirst",
                    "birthDate",
                    "patronBarcode",
                    "exported"]
    search_fields = ["nameLast", "nameFirst", "patronBarcode"]
    readonly_fields = ("powerschool",)
    list_filter = ["exported","renewable", "enrolled", "userDefinedFeild5",]

    def updater(self, request, queryset):
        queryset = queryset.filter(renewable=True, enrolled=True)
        if not queryset:
            return
        rightnow = datetime.now()
        f = StringIO.StringIO()
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['1',
                         rightnow.strftime("%H:%M:%S"),
                         rightnow.strftime("%m/%d/%Y"),
                         '3',
                         '160',
                         '267',
                         '4.1R2'])
        
        for s in queryset:
            update_fields = s.updateFromPowerschool()
            if 'enrolled' in update_fields: update_fields.remove('enrolled')
            if update_fields:
                writer.writerow(s.getPolarisTRNList())

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        filename = filename = "Updated_{}.TRN".format(rightnow.strftime("%Y%m%d%H%M"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    updater.label = "Update"
    updater.short_description = "Update, excluding non-renewable or unenrolled students"

    def exporter(self, request, queryset):
        queryset = queryset.filter(exported=False)
        if not queryset:
            return
        rightnow = datetime.now()
        f = StringIO.StringIO()
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['1',
                         rightnow.strftime("%H:%M:%S"),
                         rightnow.strftime("%m/%d/%Y"),
                         '3',
                         '160',
                         '267',
                         '4.1R2'])

        for s in queryset:
            s.creationDate = rightnow
            s.registrationDate = rightnow
            s.expirationDate = rightnow + timedelta(days=365)
            s.addressCheckDate = rightnow + timedelta(days=365*99)
            s.exported = True
            writer.writerow(s.getPolarisTRNList())
            s.save()

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        filename = filename = "PTF_{}_{}.TRN".format(rightnow.strftime("%Y%m%d%H%M"), "1")
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    exporter.label = "Export"
    exporter.short_description = "Export selected, unexported students"

    def mark_unexported(self, request, queryset):
        for polaris in queryset:
            polaris.exported = False
            polaris.save()

    mark_unexported.label = "Mark unexported"
    mark_unexported.short_description = "Mark selected students as unexported"

    def mark_exported(self, request, queryset):
        for polaris in queryset:
            polaris.exported = True
            polaris.save()

    mark_exported.label = "Mark exported"
    mark_exported.short_description = "Mark selected students as \
                                        exported without exporting"

    def extend_expiration(self, request, queryset):
        queryset = queryset.filter(renewable=True, enrolled=True)
        if not queryset:
            return
        rightnow = datetime.now()
        f = StringIO.StringIO()
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['1',
                         rightnow.strftime("%H:%M:%S"),
                         rightnow.strftime("%m/%d/%Y"),
                         '3',
                         '160',
                         '267',
                         '4.1R2'])
        
        attributes = ['recordCode','nameLast','nameFirst','patronCodeID','patronBranchID','patronBarcode','expirationDate']
        for s in queryset:
            s.expirationDate = rightnow + timedelta(days=365)
            writer.writerow(s.getPolarisTRNList(attributes=attributes))
            s.save()

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        filename = filename = "Extend_Expiration_{}.TRN".format(rightnow.strftime("%Y%m%d%H%M"))
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    extend_expiration.label = "Extend expiration"
    extend_expiration.short_description = "Extend expiration, excluding non-renewable or unenrolled students"

    actions = ['exporter', 'mark_unexported', 'mark_exported', 'extend_expiration', 'updater']


class LibrarianStudentAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = LibrarianStudentResource
    list_display = ["nameLast",
                    "nameFirst",
                    "studentID",
                    "patronBarcode",
                    "merged"]
    search_fields = ["nameLast", "nameFirst", "studentID", "patronBarcode"]
    list_filter = ["merged"]

    def merger(self, request, queryset):
        for librarian in queryset.filter(merged=False):
            studentID = librarian.studentID
            studentID = (9-len(studentID))*"0"+studentID
            powerschool = PowerSchoolStudent.objects.get(studentID=studentID)
            powerschool.createPolarisStudent()
            librarian.updatePolarisStudent()

    merger.label = "Merge"
    merger.short_description = "Merge selected, unmergered students"

    def mark_unmerged(self, request, queryset):
        for librarian in queryset:
            librarian.merged = False
            librarian.save()

    mark_unmerged.label = "Mark unmerged"
    mark_unmerged.short_description = "Mark selected students as unmerged"

    actions = ['merger', 'mark_unmerged']


admin.site.register(PowerSchoolStudent, PowerSchoolStudentAdmin)
admin.site.register(PolarisStudent, PolarisStudentAdmin)
admin.site.register(LibrarianStudent, LibrarianStudentAdmin)
