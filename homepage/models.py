from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import uuid


class Department(models.Model):
    """部门模型"""
    name = models.CharField(max_length=100, verbose_name="部门名称")
    description = models.TextField(blank=True, verbose_name="部门描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"


class Applicant(models.Model):
    """新生申请表模型"""
    GRADE_CHOICES = [
        ('freshman', '大一'),
        ('sophomore', '大二'),
        ('junior', '大三'),
        ('senior', '大四'),
        ('graduate', '研究生'),
    ]

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('passed', '通过'),
        ('rejected', '未通过'),
        ('not_scheduled', '未安排'),
        ('scheduled', '已安排'),
        ('completed', '已完成'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="姓名")
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, verbose_name="年级")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="学号")
    major = models.CharField(max_length=100, verbose_name="专业")
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(max_length=11, verbose_name="联系方式")

    # 志愿部门
    first_choice = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name="first_choice_applicants",
        verbose_name="第一志愿部门"
    )
    second_choice = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="second_choice_applicants",
        verbose_name="第二志愿部门"
    )

    # 简历相关
    resume = models.FileField(upload_to='resumes/%Y/%m/%d/', verbose_name="上传的简历PDF")

    # 面试安排
    first_interview_time = models.DateTimeField(null=True, blank=True, verbose_name="第一志愿面试时间")
    second_interview_time = models.DateTimeField(null=True, blank=True, verbose_name="第二志愿面试时间")
    first_interviewer = models.ForeignKey(
        'Interviewer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="first_interviews",
        verbose_name="第一志愿面试官"
    )
    second_interviewer = models.ForeignKey(
        'Interviewer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="second_interviews",
        verbose_name="第二志愿面试官"
    )

    # 面试状态与结果
    resume_screening_result = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="简历筛选结果"
    )
    first_interview_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_scheduled',
        verbose_name="第一志愿面试状态"
    )
    second_interview_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_scheduled',
        verbose_name="第二志愿面试状态"
    )
    first_interview_result = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="第一志愿面试结果"
    )
    second_interview_result = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="第二志愿面试结果"
    )

    # 录取信息
    admission_result = models.BooleanField(default=False, verbose_name="录取结果")
    admitted_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admitted_applicants",
        verbose_name="录取部门"
    )

    # 反馈信息
    feedback = models.TextField(blank=True, verbose_name="反馈意见")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    class Meta:
        verbose_name = "新生申请"
        verbose_name_plural = "新生申请"


class Interviewer(models.Model):
    """面试官模型"""
    name = models.CharField(max_length=100, verbose_name="面试官姓名")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="面试官学号")
    password = models.CharField(max_length=128, verbose_name="面试官密码")
    department_team = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="interviewers",
        verbose_name="面试官部门小组"
    )

    # 工作管理
    resumes_to_screen = models.JSONField(default=list, verbose_name="待筛选简历")  # 存储Applicant ID列表
    pending_interviews = models.IntegerField(default=0, verbose_name="待面试数")

    # 可用面试时间 {datetime_str: max_count}
    available_interview_times = models.JSONField(
        default=dict,
        verbose_name="可用的面试时间及最大人数"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def set_password(self, raw_password):
        """设置密码（加密存储）"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} - {self.department_team.name}"

    class Meta:
        verbose_name = "面试官"
        verbose_name_plural = "面试官"
