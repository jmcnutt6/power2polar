from nltk.metrics.distance import edit_distance

from datetime import date, datetime, timedelta
import re

from django.db import models
from django.conf import settings


class PowerSchoolStudent(models.Model):

    def __str__(self):
        return self.nameFirst+" "+self.nameLast

    enrolled = models.BooleanField(default=True)

    nameFirst = models.CharField(max_length=255, blank=True)
    nameLast = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    postalCode = models.CharField(max_length=255, blank=True)
    emailAddress = models.CharField(max_length=255, blank=True)
    parent = models.CharField(max_length=255, blank=True)
    school = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    birthDate = models.CharField(max_length=255, blank=True)
    studentID = models.CharField(unique=True, max_length=255, blank=True)
    race = models.CharField(max_length=255, blank=True)
    grade = models.CharField(max_length=255, blank=True)
    teacher = models.CharField(max_length=255, blank=True)


    def createPolarisStudent(self):
        polaris = PolarisStudent()
        polaris.powerschool = self
        polaris.save()
        polaris.updateFromPowerschool()

class LibrarianStudent(models.Model):

    def __str__(self):
        return self.nameFirst+" "+self.nameLast

    merged = models.BooleanField(default=False)

    patronBarcode = models.CharField(unique=True, max_length=255, blank=True)
    nameFirst = models.CharField(max_length=255, blank=True)
    nameLast = models.CharField(max_length=255, blank=True)
    birthDate = models.CharField(max_length=255, blank=True)
    studentID = models.CharField(unique=True, max_length=255, blank=True)
    grade = models.CharField(max_length=255, blank=True)
    teacher = models.CharField(max_length=255, blank=True)

    def updatePolarisStudent(self):
        studentID = self.studentID
        studentID = (9-len(studentID))*"0"+studentID
        polaris = PolarisStudent.objects.get(powerschool__studentID=studentID)
        polaris.patronBarcode = self.patronBarcode
        polaris.save()

        self.merged = True
        self.save()


class PolarisStudent(models.Model):

    def __str__(self):
        return self.nameFirst+" "+self.nameLast

    exported = models.BooleanField(default=False)
    enrolled = models.BooleanField(default=True)
    renewable = models.BooleanField(default=True)

    powerschool = models.OneToOneField(PowerSchoolStudent, related_name="polaris", null=True)

    nameLast = models.CharField(max_length=255)
    nameFirst = models.CharField(max_length=255)
    gender = models.CharField(max_length=4, blank=True, default="")
    password = models.CharField(max_length=255, blank=True, default="")
    birthDate = models.DateField(null=True)
    userDefinedFeild1 = models.CharField(max_length=255,
                                         blank=True,
                                         default="N/A"
                                         )
    userDefinedFeild5 = models.CharField(max_length=255)
    streetOne = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=64, blank=True, default="")
    state = models.CharField(max_length=2, default="TN")
    postalCode = models.CharField(max_length=5, blank=True, default="")
    emailAddress = models.CharField(max_length=255, blank=True, default="")
    phone1 = models.CharField(max_length=32, blank=True, default="")
    deliveryOptionID = models.CharField(max_length=4, default="3")
    eRecieptOptionID = models.CharField(max_length=4, blank=True, default="")
    patronBarcode = models.CharField(unique=True, max_length=16, blank=True, default="")
    creationDate = models.DateField(null=True)
    registrationDate = models.DateField(null=True)
    expirationDate = models.DateField(null=True)
    addressCheckDate = models.DateField(null=True)
    recordCode = models.CharField(max_length=4, default="7")
    nameMiddle = models.CharField(max_length=4, blank=True, default="")
    nameTitle = models.CharField(max_length=4, blank=True, default="")
    nameSuffix = models.CharField(max_length=4, blank=True, default="")
    patronCodeID = models.CharField(max_length=4, default="32")
    patronBranchID = models.CharField(max_length=4, default="10")
    patronStatisticalCodeID = models.CharField(max_length=4, default="0")
    languageID = models.CharField(max_length=4, default="1")
    permission = models.CharField(max_length=4, blank=True, default="")
    maintainReadingList = models.CharField(max_length=4, default="0")
    formerID = models.CharField(max_length=16, blank=True, default="")
    userDefinedFeild2 = models.CharField(max_length=255,
                                         blank=True,
                                         default=""
                                         )
    userDefinedFeild3 = models.CharField(max_length=255,
                                         blank=True,
                                         default=""
                                         )
    userDefinedFeild4 = models.CharField(max_length=255,
                                         blank=True,
                                         default=""
                                         )
    doNotDelete = models.CharField(max_length=4, default="0")
    excludeFromBills = models.CharField(max_length=4, default="0")
    excludeFromCollection = models.CharField(max_length=4, default="0")
    excludeFromHolds = models.CharField(max_length=4, default="0")
    excludeFromOverdueNotice = models.CharField(max_length=4, default="0")
    usePlainTextEmail = models.CharField(max_length=4, default="0")
    addressLabel = models.CharField(max_length=16, default="~Home")
    addressType = models.CharField(max_length=4, default="2")
    streetTwo = models.CharField(max_length=4, blank=True, default="")
    zipCodePlusFour = models.CharField(max_length=4, blank=True, default="")
    county = models.CharField(max_length=64, default="HAMILTON")
    countryID = models.CharField(max_length=4, default="1")
    altEmailAddress = models.CharField(max_length=4, blank=True, default="")
    phone1CarrierID = models.CharField(max_length=4, default="0")
    phone2 = models.CharField(max_length=4, blank=True, default="")
    phone2CarrierID = models.CharField(max_length=4, default="0")
    phone3 = models.CharField(max_length=4, blank=True, default="")
    phone3CarrierID = models.CharField(max_length=4, default="0")
    faxNumber = models.CharField(max_length=4, blank=True, default="")
    patronRecordID = models.CharField(max_length=4, default="0")
    enableSMS = models.CharField(max_length=4, default="0")
    txtPhoneNumber = models.CharField(max_length=4, default="0")

    def bestCity(self, city):
        city = city.upper()
        min_score = float("inf")
        best_match = None
        cities = settings.CITIES

        if city in cities:
            self.city = city
            return

        for lib_city in cities:
            if lib_city.startswith(city[:4]):
                self.city = lib_city
                return

        for lib_city in cities:
            score = edit_distance(city, lib_city)
            if score < min_score:
                min_score = score
                best_match = lib_city
        print "{} substituted for {} in record for {}".format(best_match,
                                                              city,
                                                              self)
        self.city = best_match

    def updateFromPowerschool(self):
        powerschool = self.powerschool

        instance = PolarisStudent()
        instance.powerschool = powerschool
        instance.enrolled = powerschool.enrolled
        instance.nameFirst = powerschool.nameFirst.upper()
        instance.nameLast = powerschool.nameLast.upper()
        instance.birthDate = datetime.strptime(powerschool.birthDate, "%m/%d/%Y").date()

        if powerschool.gender in ['M', 'F', 'N']:
            instance.gender = powerschool.gender
        phone = re.sub('[^0-9]', '', powerschool.phone)
        if len(phone) == 7:
            phone = '423'+phone
        if len(phone) == 10:
            if phone[:3] == '423':
                instance.phone1 = '{}-{}-{}'.format(phone[0:3],
                                                   phone[3:6],
                                                   phone[6:])
            else:
                instance.phone1 = '1-{}-{}-{}'.format(phone[0:3],
                                                     phone[3:6],
                                                     phone[6:])
        if powerschool.address:
            instance.streetOne = powerschool.address.upper()
        if powerschool.city:
            instance.bestCity(powerschool.city)
        if len(powerschool.state) == 2:
            instance.state = powerschool.state.upper()
        if len(powerschool.postalCode) == 5:
            instance.postalCode = powerschool.postalCode
        if powerschool.emailAddress:
            instance.emailAddress = powerschool.emailAddress
            instance.eRecieptOptionID = "2"
            instance.deliveryOptionID = "2"
        elif not instance.phone1:
            instance.phone1 = "423"
        if powerschool.parent:
            instance.userDefinedFeild1 = powerschool.parent.upper()
        if powerschool.school:
            instance.userDefinedFeild5 = powerschool.school.upper()
        instance.password = powerschool.nameLast

        updatable_fields = ["enrolled",
                            "nameLast",
                            "nameFirst",
                            "gender",
                            "password",
                            "birthDate",
                            "userDefinedFeild1",
                            "userDefinedFeild5",
                            "streetOne",
                            "city",
                            "state",
                            "postalCode",
                            "emailAddress",
                            "phone1",
                            "deliveryOptionID",
                            "eRecieptOptionID"]
        update_fields = []

        for k,v in instance.__dict__.items():
            if k in updatable_fields:
                if self.__dict__[k] != v:
                    self.__dict__[k] = v
                    update_fields.append(k)

        self.save(update_fields=update_fields)
        return update_fields

    def getPolarisTRNList(self, **kwargs):
        attribute_names_TRN_ordered = ["recordCode",
                                    "creationDate",
                                    "nameLast",
                                    "nameFirst",
                                    "nameMiddle",
                                    "nameTitle",
                                    "nameSuffix",
                                    "patronCodeID",
                                    "patronBranchID",
                                    "patronBarcode",
                                    "expirationDate",
                                    "patronStatisticalCodeID",
                                    "gender",
                                    "password",
                                    "languageID",
                                    "registrationDate",
                                    "birthDate",
                                    "permission",
                                    "maintainReadingList",
                                    "formerID",
                                    "userDefinedFeild1",
                                    "userDefinedFeild2",
                                    "userDefinedFeild3",
                                    "userDefinedFeild4",
                                    "userDefinedFeild5",
                                    "doNotDelete",
                                    "excludeFromBills",
                                    "excludeFromCollection",
                                    "excludeFromHolds",
                                    "excludeFromOverdueNotice",
                                    "usePlainTextEmail",
                                    "addressLabel",
                                    "addressType",
                                    "streetOne",
                                    "streetTwo",
                                    "city",
                                    "state",
                                    "postalCode",
                                    "zipCodePlusFour",
                                    "county",
                                    "countryID",
                                    "addressCheckDate",
                                    "emailAddress",
                                    "altEmailAddress",
                                    "phone1",
                                    "phone1CarrierID",
                                    "phone2",
                                    "phone2CarrierID",
                                    "phone3",
                                    "phone3CarrierID",
                                    "faxNumber",
                                    "deliveryOptionID",
                                    "patronRecordID",
                                    "enableSMS",
                                    "eRecieptOptionID",
                                    "txtPhoneNumber"]

        TRN_list = []
        if 'attributes' in kwargs.keys():
            attribute_names = kwargs['attributes']
            for attribute_name in attribute_names_TRN_ordered:
                if attribute_name in attribute_names:
                    attribute = self.__dict__[attribute_name]
                    if isinstance(attribute, date): attribute = attribute.strftime("%Y-%m-%d")
                else:
                    attribute = ""
                TRN_list.append(attribute)

        else:
            for attribute_name in attribute_names_TRN_ordered:
                attribute = self.__dict__[attribute_name]
                if isinstance(attribute, date): attribute = attribute.strftime("%Y-%m-%d")
                TRN_list.append(attribute)

        return TRN_list
