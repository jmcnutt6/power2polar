from import_export import resources

from django.core.exceptions import ObjectDoesNotExist

from .models import LibrarianStudent, PowerSchoolStudent
from .utils import is_luhn_valid


class LibrarianStudentResource(resources.ModelResource):

    def before_import(self, dataset, dry_run):
        barcode_set = set([])
        duplicate_barcodes = []
        barcodes = dataset['patronBarcode']
        studentIDs = dataset['studentID']

        for barcode in barcodes:
            if barcode not in barcode_set:
                barcode_set.add(barcode)
            elif barcode not in duplicate_barcodes:
                duplicate_barcodes.append(barcode)

        invalid_barcodes = [barcode for barcode in barcodes
                            if not is_luhn_valid(barcode)
                            or len(barcode) != 14]

        if invalid_barcodes:
            msg = "Import contains invalid barcode(s): {}".format(",".join(invalid_barcodes))
            raise ValueError(msg)

        if duplicate_barcodes:
            msg = "Import contains duplicate barcodes: {}".format(",".join(duplicate_barcodes))
            raise ValueError(msg)

        bad_studentIDs = []
        for studentID in studentIDs:
            studentID = (9-len(studentID))*"0"+studentID
            try:
                PowerSchoolStudent.objects.get(studentID=studentID)
            except ObjectDoesNotExist:
                bad_studentIDs.append(studentID)

        if bad_studentIDs:
            msg = "Import contains studentIDs that do not occur in current PowerSchool data: {}".format(",".join(bad_studentIDs))
            raise ValueError(msg)


    def get_instance(self, instance_loader, row):
        try:
            instance = self._meta.model.objects.get(
                patronBarcode=row['patronBarcode']
            )
            return instance
        except ObjectDoesNotExist:
            return None

    class Meta:
        model = LibrarianStudent
        exclude = ['id', 'merged']
