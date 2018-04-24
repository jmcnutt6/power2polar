from datetime import datetime, timedelta
from time import time
import re
import csv

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import LibrarianStudent
from .models import PowerSchoolStudent
from .models import PolarisStudent

def remove_non_ascii(string):
    return re.sub('[^\x00-\x7F]', '', string)

def is_luhn_valid(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def import_powerschool(inputfile):
    PowerSchoolStudent.objects.all().update(enrolled=False)
    updatable_attributes = ["nameFirst",
                            "nameLast",
                            "phone",
                            "address",
                            "city",
                            "state",
                            "postalCode",
                            "emailAddress",
                            "parent",
                            "school",
                            "gender",
                            "birthDate",
                            "studentID",
                            "race",
                            "grade",
                            "teacher"]

    with open(inputfile) as f:
        inputcsv = csv.reader(f,delimiter=",")

        #skip first line (header) of inputfile
        line = inputcsv.next()

        #for each line of inputfile
        for line in inputcsv:
            instance = PowerSchoolStudent()

            for i,k in enumerate(updatable_attributes):
                instance.__dict__[k] = remove_non_ascii(line[i])
            instance.studentID = (9-len(instance.studentID))*"0"+instance.studentID

            try:
                powerschool = PowerSchoolStudent.objects.get(studentID=instance.studentID)
            except ObjectDoesNotExist:
                powerschool = None

            if powerschool:
                update_fields = []
                for k,v in instance.__dict__.items():
                    if k in updatable_attributes:
                        if powerschool.__dict__[k] != v:
                            powerschool.__dict__[k] = v
                            update_fields.append(k)
                if update_fields: 
                    print "Updated: {}".format(powerschool)
                powerschool.save(update_fields=update_fields)

            else:
                powerschool = instance
                powerschool.save()
                print "New: {}".format(powerschool)

            powerschool.enrolled = True
            powerschool.save(update_fields=['enrolled'])
