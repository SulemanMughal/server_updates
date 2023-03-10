# Built-in
from django.template.defaultfilters import slugify  # new
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html

from .choices import *


User = get_user_model()


class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug_name = models.SlugField(verbose_name=_("Slug"),  max_length=200,  blank=True, null=True, help_text=_(
        "Slugify title of event"), default="", editable=True, unique=True)
    start_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    end_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    description = RichTextField()
    is_approved = models.CharField(
        max_length=2, choices=APPROVED_CHOICES, default="1")
    points = models.IntegerField(blank=True, null=True, default=60)
    course_img = models.ImageField(blank=True, upload_to="courses/")
    course_type = models.CharField(max_length=1,
                                   blank=True, null=True, choices=COURSE_TYPE, default="1")
    number_of_flags = models.IntegerField(default=2, blank=True, null=True)

    def __str__(self):
        return self.name

    # TODO  :   Override Default Save Method
    def save(self, *args, **kwargs):  # new
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        return super().save(*args, **kwargs)

    def is_course_approved(self):
        if self.is_approved == "3":
            return True
        return False

    def is_approved_display(self):
        if self.is_approved == "1":
            return format_html(
                '<span class="badge bg-warning">Draft</span>'
            )
        elif self.is_approved == "2":
            return format_html(
                '<span class="badge bg-primary">Approval Request Sent</span>'
            )
        elif self.is_approved == "3":
            return format_html(
                '<span class="badge bg-success">Approved</span>'
            )
        elif self.is_approved == "4":
            return format_html(
                '<span class="badge bg-danger">Rejected</span>'
            )

    def get_virtual_network(self):
        try:
            return VirtualNetwork.objects.get(course__id=self.id)
        except:
            return None

    def get_admin_url(self):
        try:
            return reverse("admin-courses-details-url", args=[self.id])
        except:
            return "#"

    def get_instructor_url(self):
        try:
            return reverse("instructor-courses-details-url", args=[self.id])
        except:
            return "#"

    def get_student_url(self):
        try:
            return reverse("student-courses-details-url", args=[self.id])
        except:
            return "#"

    # def get_detail_url(self):
    #     try:
    #         if self.instructor.is_student is True:
    #             return self.get_student_url()
    #         elif self.instructor.is_instructor is True:
    #             return self.get_instructor_url()
    #         elif self.instructor.is_admin is True:
    #             return self.get_admin_url()
    #         else:
    #             return "#"
    #     except :
    #         return "#"

    def total_challenges(self):
        try:
            return self.coursechallenge_set.all().count()
        except:
            return 0

    def total_duration(self):
        try:
            return ("%s" % str(self.end_time - self.start_time)[:-3])
        except:
            return ("%s" % str(self.end_time - self.start_time))

    # TODO  : Check Status for an exam
    def course_status(self):
        current_time = timezone.now()
        start_time = self.start_time
        end_time = self.end_time

        # ? New Course (About to Start)
        if current_time < start_time:
            return 1

        # ? In-Progress Course (Already Course has started)
        elif start_time < current_time < end_time:
            return 2

        # ? End Course (Course has been finished)
        elif end_time < current_time:
            return 3

        else:
            return 0

    def get_network_flags(self):
        try:
            return self.number_of_flags
        except:
            return None


class AssignedStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, default="1", blank=True)

    def __str__(self):
        return "{course} - {student}".format(
            course=self.course.name,
            student=self.student.email
        )

    def clean(self):

        if not self.student.is_student:
            raise ValidationError("Only Students are allowed to added.")

    class Meta:
        unique_together = ('course', 'student')

    def get_easy_challenges(self):
        return self.course.coursechallenge_set.filter(levels="1")

    def get_medium_challenges(self):
        return self.course.coursechallenge_set.filter(levels="2")

    def is_all_easy_challenges_submitted(self):
        for q in self.get_easy_challenges():
            try:
                if ChallengeSubmission.objects.filter(
                    challenge__id=q.id,
                    assinged_student__id=self.id,
                    status="SUBMITTED"
                ).count() == 0:
                    return False
            except:
                return False
        return True

    def is_all_medium_challenges_submitted(self):
        for q in self.get_medium_challenges():
            try:
                if ChallengeSubmission.objects.filter(
                    challenge__id=q.id,
                    assinged_student__id=self.id,
                    status="SUBMITTED"
                ).count() == 0:
                    return False
            except:
                return False
        return True


class VirtualNetwork(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = RichTextField()
    operating_system = models.CharField(max_length=100, default=1)
    scenarios = models.CharField(max_length=200, default="1",)
    rating = models.CharField(
        max_length=1, default="1", choices=RATING_CHOICES, blank=True, null=True)
    config_file_url = models.URLField(
        max_length=300, default="", blank=True, null=True)

    # Set fields by admin at the time of approval
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    topology_image = models.ImageField(
        upload_to="topologies/", blank=True, null=True)
    ssh_file = models.FileField(upload_to="sshFiles/", blank=True, null=True)
    instructions = RichTextField(blank=True, null=True, default="")

    is_instance_created = models.BooleanField(
        default=False, blank=True, null=True)

    imageRef = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    min_ram = models.CharField(max_length=200, blank=True, null=True)
    min_disk = models.CharField(max_length=200, blank=True, null=True)

    server_id = models.CharField(max_length=200, blank=True, null=True)

    def clean(self):
        if self.pk is None:
            if self.course.get_virtual_network():
                raise ValidationError(
                    "Virtual Network already exists for this course.")

    def __str__(self):
        return self.name

    def get_operating_system(self):
        try:
            return OPERATING_SYSTEM_CHOICES_TEXT[self.operating_system]
        except:
            return self.operating_system

    def get_scenarios(self):
        try:
            return SCENARIOS_CATEGORYIES_TEXT[self.scenarios]
        except:
            return self.scenarios

    def instructor_network_url(self):
        try:
            return reverse("instructor-machine-detail-url", args=[self.id])
        except:
            return "#"

    def student_network_url(self):
        try:
            return reverse("student-machine-detail-url", args=[self.id])
        except:
            return "#"

    def admin_network_url(self):
        try:
            return reverse("admin-machine-detail-url", args=[self.id])
        except:
            return "#"

    # def network_url(self):
    #     try:
    #         if self.course.instructor.is_instructor is True:
    #             return self.instructor_network_url()
    #         elif self.course.instructor.is_student is True:
    #             return self.student_network_url()
    #         else:
    #             return "#"
    #     except:
    #         return "#"

    # def get_course_url(self):
    #     try:
    #         if self.instructor.is_student is True:
    #             return self.get_student_url()
    #         elif self.instructor.is_instructor is True:
    #             return self.get_instructor_url()
    #         elif self.instructor.is_admin is True:
    #             return self.get_admin_url()
    #         else:
    #             return "#"
    #     except :
    #         return "#"


class CourseChallenge(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    levels = models.CharField(
        max_length=1, default="1", choices=CHALLENGE_LEVELS)
    points = models.IntegerField(blank=True, default=50)
    original_flag = models.CharField(
        max_length=200, blank=True, null=True, default="")

    def __str__(self):
        return "{course} : {title}".format(
            course=self.course,
            title=self.title
        )

    def get_difficulty_level(self):
        try:
            return CHALLENGE_LEVELS_TEXT[self.levels]
        except:
            return None


class ChallengeSubmission(models.Model):
    assinged_student = models.ForeignKey(
        AssignedStudents, on_delete=models.CASCADE)
    challenge = models.ForeignKey(CourseChallenge, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100, choices=CHALLENGE_SUBMISSION_CHOICES, default="PENDING", blank=True, null=True)
    submitted_answer = models.TextField(max_length=200, blank=True, null=True)
    obtained_points = models.IntegerField(blank=True, null=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(blank=True, null=True, default=0)


class NetworkFlag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    flag_id = models.CharField(
        max_length=50, default="", blank=True, null=True)
    points = models.IntegerField(default=50, blank=True, null=True)
    original_answer = models.CharField(
        max_length=200, default="", blank=True, null=True)
    imageRef = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.flag_id
        # if self.flag_id == "Flag 1":
        #     return "User Flag"
        # else:
        #     return "Root Flag"


class NetworkFlagSubmission(models.Model):
    student = models.ForeignKey(AssignedStudents, on_delete=models.CASCADE)
    flag_id = models.CharField(
        max_length=50, blank=True, null=True, default="")
    obtainedPoints = models.IntegerField(default=0, blank=True, null=True)
    submittedAnswer = models.CharField(max_length=100, blank=True, default="")
    attemptUsed = models.IntegerField(default=0, blank=True)
    original_answer = models.CharField(
        max_length=100, default="", blank=True, null=True)
    status = models.CharField(
        max_length=12, choices=FLAG_SUBMISSION_CHOICES, default="PENDING", blank=True)

    def __str__(self):
        return f"{self.student}-{self.flag_id}"

    def get_flag_repr(self):
        try:
            if self.flag_id == "flag_1":
                return "Root Flag"
            else:
                return "User Flag"
        except Exception as e:
            print(e)
            return self.flag_id

    def submit_status(self):
        if self.status == "SUBMITTED":
            return 1
        else:
            return 2
